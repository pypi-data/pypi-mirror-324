from typing import List, Any
import logging, time, json
from jinja2 import Template, TemplateError, StrictUndefined
from at_common_functions.utils.storage import get_storage
from at_common_models.system.prompt import PromptModel
from at_common_functions.utils.openai import get_openai
from babel.numbers import format_currency, format_decimal, format_percent

logger = logging.getLogger(__name__)

async def get_prompt(prompt_name: str) -> PromptModel:
    """Retrieve prompt template from storage."""
    storage = get_storage()
    prompts: List[PromptModel] = await storage.query(
        model_class=PromptModel,
        filters=[PromptModel.name == prompt_name]
    )

    if len(prompts) == 0:
        raise ValueError(f"No prompt found for name: {prompt_name}")
    if len(prompts) > 1:
        raise ValueError(f"Multiple prompts found for name: {prompt_name}, got {len(prompts)}")
    
    return prompts[0]

def setup_jinja_environment():
    """Configure and return Jinja2 environment with custom filters."""
    env = Template.environment_class()
    env.filters['format_currency'] = format_currency
    env.filters['format_number'] = format_decimal
    env.filters['format_decimal'] = format_decimal
    env.filters['format_percent'] = format_percent
    env.undefined = StrictUndefined
    return env

def render_prompts(prompt: PromptModel, env, **kwargs) -> tuple[str, str]:
    """Render system and user prompts using the template."""
    try:
        sys_template = env.from_string(prompt.sys_tpl)
        usr_template = env.from_string(prompt.usr_tpl)
        
        return (
            sys_template.render(**kwargs),
            usr_template.render(**kwargs)
        )
    except TemplateError as e:
        logger.error(f"Failed to render template for prompt {prompt.name}: {str(e)}")
        raise

async def _inference_base(*, model: str, prompt_name: str, output_format: str | None = None, **kwargs: Any) -> Any:
    """Base inference function that handles both text and JSON responses.
    
    Args:
        model: The model identifier
        prompt_name: Name of the prompt template to use
        output_format: If "json", returns parsed JSON. If None, returns raw text
        **kwargs: Additional arguments for prompt rendering
    """
    if not model:
        raise ValueError("Model parameter cannot be empty")

    prompt = await get_prompt(prompt_name)
    env = setup_jinja_environment()
    system_prompt, user_prompt = render_prompts(prompt, env, **kwargs)
    
    logger.info(f"Inference request to model '{model}' for prompt '{prompt_name}':")
    logger.info(f"System prompt: {system_prompt}")
    logger.info(f"User prompt: {user_prompt}")
    
    start_time = time.time()
    
    openai = get_openai()
    chat_kwargs = {
        "system": system_prompt,
        "user": user_prompt,
        "model": model,
        "temperature": prompt.param_temperature,
        "max_tokens": prompt.param_max_tokens
    }
    if output_format == "json":
        chat_kwargs["output_format"] = "json"
    
    response = await openai.chat(**chat_kwargs)
    
    if output_format == "json":
        response = json.loads(response)
    
    elapsed_time = time.time() - start_time
    logger.info(f"Response received in {elapsed_time:.2f} seconds:")
    logger.info(f"Response: {response}")
    
    return response

async def inference_as_text(*, model: str, prompt_name: str, **kwargs: Any) -> str:
    """Get inference response as raw text."""
    response = await _inference_base(model=model, prompt_name=prompt_name, output_format="text", **kwargs)
    if not isinstance(response, str):
        raise TypeError(f"Expected string response, got {type(response)}")
    return response

async def inference_as_json(*, model: str, prompt_name: str, **kwargs: Any) -> dict:
    """Get inference response as parsed JSON."""
    response = await _inference_base(model=model, prompt_name=prompt_name, output_format="json", **kwargs)
    if not isinstance(response, dict):
        raise TypeError(f"Expected dict response, got {type(response)}")
    return response