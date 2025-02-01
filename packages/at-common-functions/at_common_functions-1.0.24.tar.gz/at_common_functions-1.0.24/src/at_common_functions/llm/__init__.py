from at_common_functions.llm.impls.inference import inference_as_json as _inference_as_json, inference_as_text as _inference_as_text
from at_common_workflow import export
from typing import Any

@export
async def inference_as_text(*, model: str, prompt_name: str, **kwargs: Any) -> str:
    return await _inference_as_text(model=model, prompt_name=prompt_name, **kwargs)

@export
async def inference_as_json(*, model: str, prompt_name: str, **kwargs: Any) -> dict:
    return await _inference_as_json(model=model, prompt_name=prompt_name, **kwargs)