"""
BASIC Prompting Strategy

Direct questioning approach for straightforward claim evaluation.
This strategy uses simple, direct prompts to extract information
and classify claims without deep philosophical probing.
"""

from typing import Dict, List, Optional


class BasicPromptStrategy:
    """
    BASIC mode prompting strategy.
    
    Uses direct questions to evaluate claims:
    - Simple formulation requests
    - Direct source queries
    - Straightforward classification criteria
    """

    STRATEGY_NAME = "basic"
    DESCRIPTION = "Direct questioning for straightforward claim evaluation"

    # ------------------------------------------------------------------
    # Step 1: Statement Formulation
    # ------------------------------------------------------------------
    STEP1_TEMPLATE = """
Please clearly state the claim you want to evaluate.

Claim: {statement}

Is this claim:
1. Clearly formulated? (Yes/No)
2. Specific enough to verify? (Yes/No)
3. Contains measurable/testable assertions? (Yes/No)
"""

    # ------------------------------------------------------------------
    # Step 2: Assumption Extraction
    # ------------------------------------------------------------------
    STEP2_TEMPLATE = """
For the claim: "{statement}"

List the implicit assumptions:
1. What must be true for this claim to hold?
2. What background knowledge is assumed?
3. What definitions are taken for granted?
"""

    # ------------------------------------------------------------------
    # Step 3: Source Identification
    # ------------------------------------------------------------------
    STEP3_TEMPLATE = """
For the claim: "{statement}"

Provide sources that support or refute this claim:
- Academic papers
- Official reports
- Verified databases
- Expert testimony

Current sources provided: {sources}
"""

    # ------------------------------------------------------------------
    # Step 4: Coherence Testing
    # ------------------------------------------------------------------
    STEP4_TEMPLATE = """
For the claim: "{statement}"

Check for logical consistency:
1. Does the claim contradict itself?
2. Does it conflict with well-established facts?
3. Are there internal logical flaws?
"""

    # ------------------------------------------------------------------
    # Step 5: Classification
    # ------------------------------------------------------------------
    STEP5_TEMPLATE = """
Based on the analysis of: "{statement}"

Classify as:
- FACT: High confidence (≥85%) with verified sources
- HYP: Medium confidence (50-84%) or unverified
- UNK: Low confidence (<50%) or insufficient evidence

Current confidence: {confidence}%
Has verified sources: {has_sources}
"""

    # ------------------------------------------------------------------
    # Step 6: Confidence Quantification
    # ------------------------------------------------------------------
    STEP6_TEMPLATE = """
Quantify confidence for: "{statement}"

Factors:
- Source quality score: {source_score}/50
- Coherence score: {coherence_score}/100
- Combined confidence: {confidence}%
"""

    # ------------------------------------------------------------------
    # Step 7: Reporting
    # ------------------------------------------------------------------
    STEP7_TEMPLATE = """
=== SOCRATIC STRESS TEST REPORT (BASIC MODE) ===

Claim: {statement}
Classification: {label}
Confidence: {confidence}%

Sources ({source_count}):
{sources_list}

Summary:
{summary}
"""

    def __init__(self):
        """Initialize the BasicPromptStrategy."""
        self.templates = {
            "step1": self.STEP1_TEMPLATE,
            "step2": self.STEP2_TEMPLATE,
            "step3": self.STEP3_TEMPLATE,
            "step4": self.STEP4_TEMPLATE,
            "step5": self.STEP5_TEMPLATE,
            "step6": self.STEP6_TEMPLATE,
            "step7": self.STEP7_TEMPLATE,
        }

    def get_prompt(self, step: str, **kwargs) -> str:
        """
        Generate a prompt for the specified step.
        
        Args:
            step: The step identifier (e.g., "step1", "step2")
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted prompt string
        """
        template = self.templates.get(step)
        if template is None:
            raise ValueError(f"Unknown step: {step}")
        return template.format(**kwargs)

    def format_sources_list(self, sources: List[str]) -> str:
        """Format a list of sources for display."""
        if not sources:
            return "  (No sources provided)"
        return "\n".join(f"  - {source}" for source in sources)

    def generate_report(
        self,
        statement: str,
        label: str,
        confidence: float,
        sources: List[str],
        summary: Optional[str] = None,
    ) -> str:
        """
        Generate the final report using the STEP7 template.
        
        Args:
            statement: The evaluated claim
            label: Classification result (FACT/HYP/UNK)
            confidence: Confidence score (0-100)
            sources: List of sources
            summary: Optional summary text
            
        Returns:
            Formatted report string
        """
        sources_list = self.format_sources_list(sources)
        summary = summary or f"Claim classified as {label} with {confidence:.1f}% confidence."
        
        return self.get_prompt(
            "step7",
            statement=statement,
            label=label,
            confidence=confidence,
            source_count=len(sources),
            sources_list=sources_list,
            summary=summary,
        )
