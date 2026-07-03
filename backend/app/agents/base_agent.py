"""
base_agent.py — Shared Base Class for All Agents
=================================================
Defines the abstract interface that every agent in the pipeline must implement.
Ensures a consistent call signature and lifecycle across Sentinel, Analyst,
Policy Agent, Engagement Strategy Agent, Memory Agent, Coordinator, Caller,
Transcript Analyzer, and Router.

Design notes:
- All agents are stateless by default; state is passed in via the LangGraph
  shared state object (see app.graph.state.PipelineState).
- Agents may optionally hold lightweight config (LLM client ref, tool refs)
  injected at construction time.
- The `run()` method is the single entry point called by LangGraph node wrappers.
"""

from __future__ import annotations

import abc
from typing import Any

from app.graph.state import PipelineState
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(abc.ABC):
    """
    Abstract base class for all pipeline agents.

    Every concrete agent must implement:
        - `run(state: PipelineState) -> PipelineState`

    Optionally override:
        - `validate_input(state)`   — pre-run input checks
        - `validate_output(state)`  — post-run output checks
        - `on_error(exc, state)`    — custom error handling
    """

    name: str = "BaseAgent"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """
        Args:
            config: Optional agent-specific configuration dict
                    (e.g., LLM client, tool handles, thresholds).
        """
        self.config = config or {}
        self._logger = get_logger(self.__class__.__name__)

    @abc.abstractmethod
    def run(self, state: PipelineState) -> PipelineState:
        """
        Execute the agent's primary logic.

        Receives the current shared pipeline state, performs its task,
        and returns the (potentially mutated) state.

        Args:
            state: The current LangGraph pipeline state.

        Returns:
            Updated pipeline state after this agent's processing.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def validate_input(self, state: PipelineState) -> None:
        """
        Optional pre-run validation hook.
        Raise ValueError if the state is missing required fields for this agent.

        TODO: Implement per-agent required-field checks.
        """
        pass

    def validate_output(self, state: PipelineState) -> None:
        """
        Optional post-run validation hook.
        Raise ValueError if the agent's output is malformed.

        TODO: Implement per-agent output schema checks.
        """
        pass

    def on_error(self, exc: Exception, state: PipelineState) -> PipelineState:
        """
        Called by the Coordinator when an unhandled exception occurs during `run()`.
        Default behaviour: log the error and return state with error metadata attached.

        TODO: Implement per-agent recovery strategies (retry, skip, escalate).
        """
        self._logger.error(f"[{self.name}] Unhandled error: {exc}", exc_info=True)
        return state

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
