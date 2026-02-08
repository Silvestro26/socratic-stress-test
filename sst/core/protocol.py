"""
SST Protocol - 7-Step Structured Methodology

This module implements the core 7-step Socratic Stress Test protocol
for auditing epistemic reliability of reasoning systems.
"""

from sst.core.claim import Claim
from sst.core.classification import Classification
from sst.core.self_test import SelfTest


class SSTProtocol:
    """
    Implements the 7-step Socratic Stress Test (SST) protocol.

    Steps:
    1. Statement formulation - Clearly articulate the claim
    2. Assumption extraction - Identify implicit premises
    3. Source identification - Link to verifiable evidence
    4. Coherence testing - Check logical consistency
    5. Classification - Assign FACT/HYP/UNK label
    6. Confidence quantification - Score 0-100
    7. Reporting - Generate transparent reasoning chain
    """

    MODES = ("basic", "deep-ask", "deep-auto")

    def __init__(self, mode: str = "basic"):
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode '{mode}'. Choose from {self.MODES}")
        self.mode = mode
        self.steps_completed = []
        self.current_claim = None
        self.result = {}

    # ------------------------------------------------------------------
    # Step 1
    # ------------------------------------------------------------------
    def step1_formulate_statement(self, statement: str) -> dict:
        """Clearly articulate and validate the claim structure."""
        self.current_claim = statement
        self.steps_completed.append("step1_formulate_statement")
        return {
            "step": 1,
            "name": "Statement Formulation",
            "statement": statement,
            "is_valid": len(statement.strip()) > 0,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 2
    # ------------------------------------------------------------------
    def step2_extract_assumptions(self) -> dict:
        """Identify implicit premises and presuppositions."""
        self.steps_completed.append("step2_extract_assumptions")
        st = SelfTest()
        assumptions = st.extract_assumptions([self.current_claim])
        return {
            "step": 2,
            "name": "Assumption Extraction",
            "assumptions": assumptions,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 3
    # ------------------------------------------------------------------
    def step3_identify_sources(self, sources: list) -> dict:
        """Link assertions to verifiable evidence."""
        self.steps_completed.append("step3_identify_sources")
        return {
            "step": 3,
            "name": "Source Identification",
            "sources": sources,
            "source_count": len(sources),
            "has_sources": len(sources) > 0,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 4
    # ------------------------------------------------------------------
    def step4_test_coherence(self) -> dict:
        """Check logical consistency and identify contradictions."""
        self.steps_completed.append("step4_test_coherence")
        st = SelfTest()
        coherence = st.evaluate_coherence([self.current_claim])
        return {
            "step": 4,
            "name": "Coherence Testing",
            "coherence_results": coherence,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 5
    # ------------------------------------------------------------------
    def step5_classify_claim(self, confidence: float, has_sources: bool) -> dict:
        """Assign FACT/HYP/UNK label based on evidence."""
        self.steps_completed.append("step5_classify_claim")
        clf = Classification()
        if confidence >= 85 and has_sources:
            clf.set_state("FACT")
        elif confidence >= 50:
            clf.set_state("HYP")
        else:
            clf.set_state("UNK")
        return {
            "step": 5,
            "name": "Classification",
            "label": clf.current_state,
            "confidence": confidence,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 6
    # ------------------------------------------------------------------
    def step6_quantify_confidence(self, sources: list, coherence_score: float) -> float:
        """Score the claim credibility from 0 to 100."""
        self.steps_completed.append("step6_quantify_confidence")
        source_score = min(len(sources) * 20, 50)
        confidence = (source_score + coherence_score) / 2
        return min(confidence, 100)

    # ------------------------------------------------------------------
    # Step 7
    # ------------------------------------------------------------------
    def step7_generate_report(self, all_results: dict) -> dict:
        """Generate transparent reasoning chain and full report."""
        self.steps_completed.append("step7_generate_report")
        return {
            "step": 7,
            "name": "Reporting",
            "claim": self.current_claim,
            "mode": self.mode,
            "steps_completed": list(self.steps_completed),
            "full_analysis": all_results,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Convenience: run the full protocol at once
    # ------------------------------------------------------------------
    def run_full_protocol(self, statement: str, sources: list,
                          coherence_score: float = 75.0) -> dict:
        """Execute all 7 steps sequentially and return the report."""
        r1 = self.step1_formulate_statement(statement)
        r2 = self.step2_extract_assumptions()
        r3 = self.step3_identify_sources(sources)
        r4 = self.step4_test_coherence()
        confidence = self.step6_quantify_confidence(sources, coherence_score)
        r5 = self.step5_classify_claim(confidence, len(sources) > 0)

        all_results = {
            "step1": r1,
            "step2": r2,
            "step3": r3,
            "step4": r4,
            "step5": r5,
            "step6": {"confidence": confidence},
        }

        r7 = self.step7_generate_report(all_results)
        self.result = r7
        return self.result
