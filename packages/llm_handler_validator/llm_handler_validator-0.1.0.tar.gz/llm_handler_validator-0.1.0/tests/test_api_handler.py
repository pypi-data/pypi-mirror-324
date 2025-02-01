"""
Tests for the UnifiedLLMHandler class in llmhandler.
This file now covers:
  - Structured (typed) responses (single and multiple prompts)
  - Unstructured (free-text) responses when response_type is omitted or None
  - Provider-specific tests for Anthropic, DeepSeek, Gemini, and OpenRouter
  - Batch mode tests for structured responses (placed last)
  - Additional tests for:
      a) Batch mode used with unstructured output (should raise error)
      b) Explicitly passing a non-Pydantic type (str) as response_type
"""

import pytest
import asyncio
import inspect
from unittest.mock import patch, MagicMock, AsyncMock
from typing import List

from llmhandler.api_handler import UnifiedLLMHandler
from llmhandler._internal_models import (
    BatchMetadata,
    BatchResult,
    SimpleResponse,
    MathResponse,
    PersonResponse,
    UnifiedResponse,
)
from pydantic_ai.exceptions import UserError


# --- Structured tests ---

@pytest.mark.asyncio
async def test_single_prompt_structured():
    """Test a single prompt with a typed response."""
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        # Return a valid Pydantic object
        mock_run.return_value.data = SimpleResponse(content="Hello structured", confidence=0.95)
        result = await handler.process(
            prompts="Hello world structured",
            model="openai:gpt-4o",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert isinstance(result.data, SimpleResponse)
    assert result.data.content == "Hello structured"


@pytest.mark.asyncio
async def test_multiple_prompts_structured():
    """Test multiple prompts with a typed response."""
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    responses = [
        SimpleResponse(content="Resp A", confidence=0.9),
        SimpleResponse(content="Resp B", confidence=0.9),
    ]
    async def side_effect(prompt: str):
        mock_obj = MagicMock()
        idx = 0 if "A" in prompt else 1
        mock_obj.data = responses[idx]
        return mock_obj
    with patch("llmhandler.api_handler.Agent.run", side_effect=side_effect):
        prompts = ["Prompt A", "Prompt B"]
        result = await handler.process(
            prompts=prompts,
            model="openai:gpt-4o-mini",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert isinstance(result.data, list)
    assert len(result.data) == 2
    for resp, expected in zip(result.data, ["Resp A", "Resp B"]):
        assert isinstance(resp, SimpleResponse)
        assert resp.content == expected


@pytest.mark.asyncio
async def test_invalid_provider():
    """
    Ensure that an invalid (missing prefix) model string raises a UserError.
    """
    handler = UnifiedLLMHandler()
    with pytest.raises(UserError):
        await handler.process(
            prompts="Test prompt",
            model="gpt-4o-mini",  # missing "provider:" => should raise
            response_type=SimpleResponse
        )


@pytest.mark.asyncio
async def test_empty_prompts():
    """
    Ensure empty string prompt raises a UserError.
    """
    handler = UnifiedLLMHandler()
    with pytest.raises(UserError):
        await handler.process(
            prompts="",
            model="openai:gpt-4o",  # allowed
            response_type=SimpleResponse
        )


# --- Unstructured tests (free-text) ---

@pytest.mark.asyncio
async def test_single_prompt_unstructured_explicit_none():
    """
    Test processing a single prompt with unstructured response
    when response_type is explicitly set to None.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = "Free text response"
        result = await handler.process(
            prompts="What is your favorite color?",
            model="openai:gpt-4o-mini",
            response_type=None
        )
    assert isinstance(result, str)
    assert "Free text" in result


@pytest.mark.asyncio
async def test_single_prompt_unstructured_omitted():
    """
    Test processing a single prompt with unstructured response
    when response_type is omitted.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = "Raw free text output"
        result = await handler.process(
            prompts="Tell me a fun fact.",
            model="openai:gpt-4o-mini"
            # response_type omitted → unstructured output
        )
    assert isinstance(result, str)
    assert "free text" in result.lower()


@pytest.mark.asyncio
async def test_multiple_prompts_unstructured():
    """
    Test processing multiple prompts with unstructured responses.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    async def side_effect(prompt: str):
        mock_obj = MagicMock()
        mock_obj.data = f"Response for {prompt}"
        return mock_obj
    with patch("llmhandler.api_handler.Agent.run", side_effect=side_effect):
        prompts = ["Prompt one", "Prompt two"]
        result = await handler.process(
            prompts=prompts,
            model="openai:gpt-4o-mini",
            response_type=None  # unstructured
        )
    assert isinstance(result, list)
    assert all(isinstance(r, str) for r in result)
    assert "Prompt one" in result[0]


# --- Explicit non-Pydantic type usage ---

@pytest.mark.asyncio
async def test_single_prompt_with_str_as_response_type():
    """
    Test that if the user explicitly passes 'str' as the response_type,
    the handler returns unstructured free text.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = "Raw text response"
        result = await handler.process(
            prompts="What is the meaning of life?",
            model="openai:gpt-4o-mini",
            response_type=str  # Explicitly passing str should be treated as unstructured
        )
    assert isinstance(result, str)
    assert "Raw text" in result


# --- Provider-specific structured tests ---

@pytest.mark.asyncio
async def test_structured_anthropic():
    """Test a structured response with Anthropic provider."""
    handler = UnifiedLLMHandler(anthropic_api_key="fake_anthropic_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = SimpleResponse(content="Anthropic result", confidence=0.95)
        result = await handler.process(
            prompts="Tell me something interesting.",
            model="anthropic:claude-3-5-sonnet-20241022",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert result.data.content == "Anthropic result"


@pytest.mark.asyncio
async def test_structured_deepseek():
    """Test a structured response with DeepSeek provider."""
    handler = UnifiedLLMHandler(deepseek_api_key="fake_deepseek_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = SimpleResponse(content="DeepSeek result", confidence=0.95)
        result = await handler.process(
            prompts="Explain quantum physics simply.",
            model="deepseek:deepseek-chat",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert result.data.content == "DeepSeek result"


@pytest.mark.asyncio
async def test_structured_gemini():
    """Test a structured response with Gemini provider."""
    handler = UnifiedLLMHandler(gemini_api_key="fake_gemini_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = SimpleResponse(content="Gemini result", confidence=0.95)
        result = await handler.process(
            prompts="Compose a haiku about nature.",
            model="gemini:gemini-1.5-flash",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert result.data.content == "Gemini result"


@pytest.mark.asyncio
async def test_structured_openrouter():
    """Test a structured response with OpenRouter (routing to Anthropic)."""
    handler = UnifiedLLMHandler(openrouter_api_key="fake_openrouter_key")
    with patch("llmhandler.api_handler.Agent.run") as mock_run:
        mock_run.return_value.data = SimpleResponse(content="OpenRouter result", confidence=0.9)
        result = await handler.process(
            prompts="List uses for AI in gardening.",
            model="openrouter:anthropic/claude-3-5-haiku-20241022",
            response_type=SimpleResponse
        )
    assert result.success is True
    assert result.data.content == "OpenRouter result"


# --- Batch Mode tests (placed last) ---

@pytest.mark.asyncio
async def test_batch_mode_structured():
    """
    Test batch mode with a typed response.
    This uses mocked network calls to simulate file upload and batch processing.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with patch("llmhandler.api_handler.Agent") as mock_agent_cls:
        mock_agent_inst = MagicMock()
        mock_model_client = MagicMock()
        mock_model_client.files.create = AsyncMock()
        mock_model_client.batches.create = AsyncMock()
        mock_model_client.batches.retrieve = AsyncMock()
        mock_model_client.files.content = AsyncMock()
        mock_model_client.files.create.return_value.id = "fake_file_id"
        mock_model_client.batches.create.return_value.id = "fake_batch_id"
        mock_model_client.batches.retrieve.side_effect = [
            MagicMock(status="in_progress", output_file_id="fake_out_file"),
            MagicMock(status="completed", output_file_id="fake_out_file")
        ]
        mock_model_client.files.content.return_value.content = (
            b'{"response":{"body":{"choices":[{"message":{"content":"Batch result A"}}]}}}\n'
            b'{"response":{"body":{"choices":[{"message":{"content":"Batch result B"}}]}}}\n'
        )
        mock_agent_inst.model.model_name = "gpt-4o"
        mock_agent_inst.model.client = mock_model_client
        mock_agent_cls.return_value = mock_agent_inst

        result = await handler.process(
            prompts=["BatchPromptA", "BatchPromptB"],
            model="openai:gpt-4o",
            response_type=SimpleResponse,
            batch_mode=True,
        )

    assert result.success is True
    assert isinstance(result.data, BatchResult)
    assert len(result.data.results) == 2
    assert result.data.results[0]["response"].content == "Batch result A"
    assert result.data.results[1]["response"].content == "Batch result B"


@pytest.mark.asyncio
async def test_batch_mode_unstructured_raises_error():
    """
    Test that attempting to use batch mode with unstructured output (no Pydantic model)
    raises a UserError.
    """
    handler = UnifiedLLMHandler(openai_api_key="fake_openai_key")
    with pytest.raises(UserError):
        await handler.process(
            prompts=["BatchPromptX", "BatchPromptY"],
            model="openai:gpt-4o-mini",
            response_type=None,  # unstructured output
            batch_mode=True
        )
