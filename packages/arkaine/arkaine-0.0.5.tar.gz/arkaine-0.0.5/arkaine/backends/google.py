from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from arkaine.agent import Prompt
from arkaine.backends.base import BaseBackend
from arkaine.backends.common import simple_tool_results_to_prompts
from arkaine.llms.google import Google as GoogleLLM
from arkaine.tools.tool import Context, Tool
from arkaine.tools.types import ToolArguments, ToolResults
from arkaine.utils.templater import PromptTemplate


class Google(BaseBackend):
    def __init__(
        self,
        tools: List[Tool] = [],
        template: PromptTemplate = PromptTemplate.default(),
        max_simultaneous_tools: int = -1,
        api_key: Optional[str] = None,
        model: str = "gemini-pro",
        max_tokens: int = 1024,
        initial_state: Dict[str, Any] = {},
    ):
        pass
