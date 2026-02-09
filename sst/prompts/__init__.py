"""
SST Prompting Strategies Module

This module provides three prompting strategy templates for the
Socratic Stress Test protocol:

- BASIC: Direct questioning approach
- DEEP-ASK: Maieutic method with human guidance
- DEEP-AUTO: Self-administered deep analysis
"""

from sst.prompts.basic import BasicPromptStrategy
from sst.prompts.deep_ask import DeepAskPromptStrategy
from sst.prompts.deep_auto import DeepAutoPromptStrategy

__all__ = [
    "BasicPromptStrategy",
    "DeepAskPromptStrategy",
    "DeepAutoPromptStrategy",
]
