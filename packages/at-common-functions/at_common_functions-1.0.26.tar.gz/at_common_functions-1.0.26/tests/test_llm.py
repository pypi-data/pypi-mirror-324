import pytest, os
from unittest.mock import MagicMock, patch, AsyncMock
from at_common_functions.llm import inference_as_text, inference_as_json
from at_common_models.system.prompt import PromptModel
from at_common_functions.utils.storage import init_storage, StorageSettings
from at_common_functions.utils.openai import init_openai, OpenAISettings
import logging
import pytest_asyncio
from jinja2 import TemplateError
import jinja2
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_storage():
    storage = MagicMock()
    
    # Sample test prompt
    prompt = PromptModel(
        name="test_prompt",
        sys_tpl="You are a helpful assistant that {{ action }}",
        usr_tpl="Please {{ task }}",
        param_temperature=0.0,
        param_max_tokens=100
    )
    
    async def mock_query(model_class, filters):
        return [prompt]
    
    storage.query = mock_query
    return storage

@pytest_asyncio.fixture
async def setup_services(required_env_vars):
    # Initialize storage service
    storage_settings = StorageSettings(
        host="localhost",
        port=3306,
        user="test",
        password="test",
        database="test"
    )
    init_storage(storage_settings)
    
    # Initialize OpenAI service
    openai_settings = OpenAISettings(
        organization=required_env_vars["OPENAI_ORG_ID"],
        api_key=required_env_vars["OPENAI_API_KEY"],
        proxy=os.getenv("OPENAI_PROXY_URL", "")
    )
    init_openai(openai_settings)

@pytest.mark.asyncio
async def test_inference_success(setup_services, mock_storage):
    # Mock the get_storage function to return our mock_storage
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        response = await inference_as_text(
            model="gpt-3.5-turbo",
            prompt_name="test_prompt",
            action="provides simple answers",
            task="say hello"
        )
        
        logger.info(f"Response received: {response}")
        assert isinstance(response, str)
        assert len(response) > 0

@pytest.mark.asyncio
async def test_inference_no_prompt(mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        # Override the mock_query to return empty list as a coroutine
        mock_storage.query = AsyncMock(return_value=[])
        
        with pytest.raises(ValueError, match="No prompt found for name"):
            await inference_as_text(
                model="gpt-3.5-turbo",
                prompt_name="nonexistent_prompt"
            )

@pytest.mark.asyncio
async def test_inference_empty_model(mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        with pytest.raises(ValueError, match="Model parameter cannot be empty"):
            await inference_as_text(
                model="",
                prompt_name="test_prompt"
            )

@pytest.mark.asyncio
async def test_inference_missing_template_variable(setup_services, mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage

        # The template requires 'action' and 'task', but we're not providing 'action'
        with pytest.raises(jinja2.exceptions.UndefinedError):
            await inference_as_text(
                model="gpt-3.5-turbo",
                prompt_name="test_prompt",
                task="say hello"  # Missing 'action' parameter
            )

@pytest.mark.asyncio
async def test_inference_complex_template_variables(mock_storage):
    # Create a mock storage with a more complex template
    complex_prompt = PromptModel(
        name="complex_prompt",
        sys_tpl="You are an {{ role }} specialized in {{ specialty }}",
        usr_tpl="Create a {{ length }} {{ document_type }} about {{ topic }}",
        param_temperature=0.0,
        param_max_tokens=100
    )
    
    mock_storage.query = AsyncMock(return_value=[complex_prompt])
    
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        response = await inference_as_text(
            model="gpt-3.5-turbo",
            prompt_name="complex_prompt",
            role="professional writer",
            specialty="technical documentation",
            length="short",
            document_type="guide",
            topic="Python testing"
        )
        
        assert isinstance(response, str)
        assert len(response) > 0

@pytest.mark.asyncio
async def test_inference_invalid_template_syntax(mock_storage):
    # Create a mock storage with invalid template syntax
    invalid_prompt = PromptModel(
        name="invalid_prompt",
        sys_tpl="You are a {{ role } with invalid syntax",  # Note the missing closing brace
        usr_tpl="Normal template {{ task }}",
        param_temperature=0.0,
        param_max_tokens=100
    )
    
    mock_storage.query = AsyncMock(return_value=[invalid_prompt])
    
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        with pytest.raises(TemplateError):
            await inference_as_text(
                model="gpt-3.5-turbo",
                prompt_name="invalid_prompt",
                role="assistant",
                task="help me"
            )

@pytest.mark.asyncio
async def test_inference_with_number_formatting(mock_storage):
    # Create a mock storage with number formatting template
    formatting_prompt = PromptModel(
        name="formatting_prompt",
        sys_tpl="You are a financial assistant",
        usr_tpl="Format these numbers: {{ value|format_decimal }}, {{ percent|format_percent }}, {{ money|format_currency('USD') }}",
        param_temperature=0.0,
        param_max_tokens=100
    )
    
    mock_storage.query = AsyncMock(return_value=[formatting_prompt])
    
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        response = await inference_as_text(
            model="gpt-3.5-turbo",
            prompt_name="formatting_prompt",
            value=1234.5678,
            percent=0.1234,
            money=1234.56
        )
        
        assert isinstance(response, str)
        assert len(response) > 0

@pytest.mark.asyncio
async def test_inference_with_strict_undefined_variables(mock_storage):
    # Test that undefined variables raise an error due to StrictUndefined
    strict_prompt = PromptModel(
        name="strict_prompt",
        sys_tpl="System with {{ required_var }}",
        usr_tpl="User with {{ another_var }}",
        param_temperature=0.0,
        param_max_tokens=100
    )
    
    mock_storage.query = AsyncMock(return_value=[strict_prompt])
    
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage:
        mock_get_storage.return_value = mock_storage
        
        with pytest.raises(jinja2.exceptions.UndefinedError):
            await inference_as_text(
                model="gpt-3.5-turbo",
                prompt_name="strict_prompt",
                # Not providing required_var or another_var
            )

@pytest.mark.asyncio
async def test_inference_as_json_success(setup_services, mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage, \
         patch('at_common_functions.llm.impls.inference.get_openai') as mock_get_openai:
        mock_get_storage.return_value = mock_storage
        
        # Mock OpenAI response
        mock_openai = AsyncMock()
        mock_openai.chat = AsyncMock(return_value='{"message": "Hello!", "status": "success"}')
        mock_get_openai.return_value = mock_openai
        
        response = await inference_as_json(
            model="gpt-3.5-turbo",
            prompt_name="test_prompt",
            action="provides JSON responses",
            task="say hello"
        )
        
        assert isinstance(response, dict)
        assert "message" in response
        assert "status" in response

@pytest.mark.asyncio
async def test_inference_as_json_invalid_json(setup_services, mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage, \
         patch('at_common_functions.llm.impls.inference.get_openai') as mock_get_openai:
        mock_get_storage.return_value = mock_storage
        
        # Mock OpenAI response with invalid JSON
        mock_openai = AsyncMock()
        mock_openai.chat = AsyncMock(return_value='Invalid JSON response')
        mock_get_openai.return_value = mock_openai
        
        with pytest.raises(json.JSONDecodeError):
            await inference_as_json(
                model="gpt-3.5-turbo",
                prompt_name="test_prompt",
                action="provides JSON responses",
                task="say hello"
            )

@pytest.mark.asyncio
async def test_inference_as_json_non_dict_response(setup_services, mock_storage):
    with patch('at_common_functions.llm.impls.inference.get_storage') as mock_get_storage, \
         patch('at_common_functions.llm.impls.inference.get_openai') as mock_get_openai:
        mock_get_storage.return_value = mock_storage
        
        # Mock OpenAI response with JSON array instead of object
        mock_openai = AsyncMock()
        mock_openai.chat = AsyncMock(return_value='[1, 2, 3]')
        mock_get_openai.return_value = mock_openai
        
        with pytest.raises(TypeError, match="Expected dict response"):
            await inference_as_json(
                model="gpt-3.5-turbo",
                prompt_name="test_prompt",
                action="provides JSON responses",
                task="say hello"
            )