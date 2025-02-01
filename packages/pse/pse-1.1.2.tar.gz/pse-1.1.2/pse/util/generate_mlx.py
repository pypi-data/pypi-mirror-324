import logging
from dataclasses import dataclass

import mlx.core as mx
import mlx.nn as nn
from mlx_lm.sample_utils import categorical_sampling

from pse.structure.engine import StructuringEngine

logger = logging.getLogger(__name__)


@dataclass
class GenerateStepResult:
    token: mx.array
    logits: mx.array
    token_ids: list[int]
    time_to_generate_mask: float | None
    time_to_next_token: float | None
    total_time: float


@dataclass
class CompletedGeneration:
    output: str
    average_mask_latency: float
    average_time_to_get_next_token: float
    average_total_time: float

def sample(
    prompt: str | mx.array,
    model: nn.Module,
    engine: StructuringEngine,
    temp: float = 0.5,
) -> GenerateStepResult:
    """
    A generator producing token ids based on the given prompt from the model.

    Args:
        prompt (mx.array): The input prompt.
        model (nn.Module): The model to use for generation.
        engine (StructuringEngine): The engine to use for generation.
        temp (float): The temperature for sampling, if 0.0 the argmax is used.
          Default: ``1.0``.
    returns:
        Tuple[mx.array, mx.array]: A tuple of one token and a vector of log probabilities.
    """
    import timeit

    start_total = timeit.default_timer()

    if isinstance(prompt, str):
        messages = [{"role": "user", "content": prompt}]
        encoded_prompt = engine.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True
        )
        prompt = mx.array(encoded_prompt)

    # Generate logits
    logits = model(prompt[None])
    logits = logits[:, -1, :]
    assert isinstance(logits, mx.array)
    mx.async_eval(logits)

    # Time the generation of the logit bias mask
    start_logits = timeit.default_timer()
    logits = engine(logits[0, :])
    end_logits = timeit.default_timer()
    logprobs = logits - mx.logsumexp(logits, keepdims=True)

    def __sample(logprobs: mx.array, **kwargs) -> mx.array:
        temp = float(kwargs.get("temperature", 1.0))
        token: mx.array = (
            categorical_sampling(logprobs, temp)
            if temp > 0.0
            else mx.argmax(logprobs, axis=-1)
        )
        return token


    # Time the process of sampling the next token
    start_token = timeit.default_timer()
    token_ids = engine.sample(logprobs, __sample, temperature=temp)
    end_token = timeit.default_timer()

    return GenerateStepResult(
        mx.array(token_ids, dtype=prompt.dtype),
        logits,
        token_ids,
        end_logits - start_logits,
        end_token - start_token,
        end_token - start_total,
    )


def generate(
    prompt: str,
    model: nn.Module,
    engine: StructuringEngine,
    prefill: str | None = None,
) -> CompletedGeneration:
    messages = [{"role": "user", "content": prompt}]
    encoded_prompt = mx.array(
        engine.tokenizer.apply_chat_template(
            conversation=messages,
            add_generation_prompt=True,
        )
    )

    if prefill:
        encoded_prompt = mx.concatenate(
            [
                encoded_prompt,
                mx.array(engine.tokenizer.encode(prefill)),
            ]
        )

    logger.info(engine.tokenizer.decode(encoded_prompt.tolist()))
    encoded_prompt = mx.array(encoded_prompt)
    generation_results: list[GenerateStepResult] = []
    while not engine.has_reached_accept_state:
        try:
            result = sample(encoded_prompt, model, engine)
            encoded_prompt = mx.concatenate([encoded_prompt, result.token])
            generation_results.append(result)
            decoded_tokens = engine.tokenizer.decode(result.token_ids)
            print("\033[1;33m", end="")
            print(decoded_tokens, end="", flush=True)
            print("\033[0m", end="")
        except Exception as e:
            logger.warning(f"Token rejected: {e}")
            break

    output = engine.tokenizer.decode(
        [token_id for result in generation_results for token_id in result.token_ids]
    )
    if prefill:
        output = prefill + output

    mask_latencies = [
        mask_time
        for result in generation_results
        if (mask_time := result.time_to_generate_mask) is not None
    ]
    average_mask_latency = (
        sum(mask_latencies) / len(mask_latencies) if mask_latencies else 0.0
    )
    time_to_next_tokens = [
        time_to_next_token
        for result in generation_results
        if (time_to_next_token := result.time_to_next_token) is not None
    ]
    average_time_to_next_token = (
        sum(time_to_next_tokens) / len(time_to_next_tokens)
        if time_to_next_tokens
        else 0.0
    )
    total_times = [result.total_time for result in generation_results]
    average_total_time = sum(total_times) / len(total_times) if total_times else 0.0

    # Log performance metrics
    logger.info(
        f"Average time to generate logit bias mask: "
        f"{average_time_to_next_token:.6f} seconds"
    )
    logger.info(
        f"Average time to get next token: " f"{average_time_to_next_token:.6f} seconds"
    )
    logger.info(f"Average total time: {average_total_time:.6f} seconds")

    return CompletedGeneration(
        output,
        average_mask_latency,
        average_time_to_next_token,
        average_total_time,
    )
