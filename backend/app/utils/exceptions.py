"""
exceptions.py — Custom Exception Classes
========================================
Defines domain-specific exception hierarchy for pipeline orchestration,
policy violations, and integration failures.
"""


class SBIPipelineException(Exception):
    """Base class for all custom pipeline exceptions."""
    pass


class PolicyViolationError(SBIPipelineException):
    """Raised when an engagement hypothesis fails mandatory compliance checks."""
    pass


class AgentExecutionError(SBIPipelineException):
    """Raised when an agent node fails unrecoverably during graph execution."""
    pass


class CustomerNotFoundError(SBIPipelineException):
    """Raised when customer profile cannot be retrieved from DB or MemoryAgent."""
    pass
