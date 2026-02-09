"""
SST Protocol - 7-Step Structured Methodology

This module implements the core 7-step Socratic Stress Test protocol
for auditing epistemic reliability of reasoning systems.
"""

from typing import Dict, Any, List, Optional

from sst.core.claim import Claim
from sst.core.classification import Classification
from sst.core.self_test import SelfTest
from sst.prompts import BasicPromptStrategy, DeepAskPromptStrategy, DeepAutoPromptStrategy


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
    
    Modes:
    - basic: Direct questioning approach
    - deep-ask: Maieutic method with human guidance
    - deep-auto: Self-administered automated analysis
    """

    MODES = ("basic", "deep-ask", "deep-auto")

    # Map modes to prompt strategy classes
    PROMPT_STRATEGIES = {
        "basic": BasicPromptStrategy,
        "deep-ask": DeepAskPromptStrategy,
        "deep-auto": DeepAutoPromptStrategy,
    }

    def __init__(self, mode: str = "basic"):
        """
        Initialize the SST Protocol.
        
        Args:
            mode: Operating mode (basic, deep-ask, or deep-auto)
            
        Raises:
            ValueError: If mode is invalid
        """
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode '{mode}'. Choose from {self.MODES}")
        self.mode = mode
        self.steps_completed: List[str] = []
        self.current_claim: Optional[str] = None
        self.result: Dict[str, Any] = {}
        
        # Initialize the appropriate prompt strategy
        self.prompt_strategy = self.PROMPT_STRATEGIES[mode]()
        
        # Initialize analysis components
        self.self_test = SelfTest()
        self.classification = Classification()

    def get_prompt_strategy(self):
        """Get the current prompt strategy instance."""
        return self.prompt_strategy

    # ------------------------------------------------------------------
    # Step 1
    # ------------------------------------------------------------------
    def step1_formulate_statement(self, statement: str) -> dict:
        """
        Clearly articulate and validate the claim structure.
        
        Args:
            statement: The claim to formulate
            
        Returns:
            Step 1 results dictionary
        """
        self.current_claim = statement
        self.steps_completed.append("step1_formulate_statement")
        
        # Analyze statement quality
        is_valid = len(statement.strip()) > 0
        
        # Get mode-specific prompt if needed
        prompt = None
        if hasattr(self.prompt_strategy, 'get_prompt'):
            try:
                prompt = self.prompt_strategy.get_prompt("step1", statement=statement)
            except (KeyError, TypeError):
                pass
        
        return {
            "step": 1,
            "name": "Statement Formulation",
            "statement": statement,
            "is_valid": is_valid,
            "prompt": prompt,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 2
    # ------------------------------------------------------------------
    def step2_extract_assumptions(self) -> dict:
        """
        Identify implicit premises and presuppositions.
        
        Returns:
            Step 2 results dictionary
        """
        self.steps_completed.append("step2_extract_assumptions")
        
        # Use SelfTest for assumption extraction
        assumptions = self.self_test.extract_assumptions([self.current_claim])
        
        # Get mode-specific prompt if needed
        prompt = None
        if hasattr(self.prompt_strategy, 'get_prompt'):
            try:
                prompt = self.prompt_strategy.get_prompt("step2", statement=self.current_claim)
            except (KeyError, TypeError):
                pass
        
        return {
            "step": 2,
            "name": "Assumption Extraction",
            "assumptions": assumptions,
            "assumption_count": len(assumptions),
            "prompt": prompt,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 3
    # ------------------------------------------------------------------
    def step3_identify_sources(self, sources: list) -> dict:
        """
        Link assertions to verifiable evidence.
        
        Args:
            sources: List of source references
            
        Returns:
            Step 3 results dictionary
        """
        self.steps_completed.append("step3_identify_sources")
        
        # Evaluate source quality for deep-auto mode
        source_quality = None
        if self.mode == "deep-auto" and hasattr(self.prompt_strategy, 'evaluate_sources_auto'):
            source_result = self.prompt_strategy.evaluate_sources_auto(sources)
            source_quality = source_result.score
        
        return {
            "step": 3,
            "name": "Source Identification",
            "sources": sources,
            "source_count": len(sources),
            "has_sources": len(sources) > 0,
            "source_quality": source_quality,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 4
    # ------------------------------------------------------------------
    def step4_test_coherence(self) -> dict:
        """
        Check logical consistency and identify contradictions.
        
        Returns:
            Step 4 results dictionary
        """
        self.steps_completed.append("step4_test_coherence")
        
        # Extract assumptions first if not done
        if not self.self_test.assumptions:
            self.self_test.extract_assumptions([self.current_claim])
        
        # Evaluate coherence
        coherence = self.self_test.evaluate_coherence([self.current_claim])
        coherence_score = self.self_test.get_coherence_score()
        
        return {
            "step": 4,
            "name": "Coherence Testing",
            "coherence_results": coherence,
            "coherence_score": coherence_score,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 5
    # ------------------------------------------------------------------
    def step5_classify_claim(self, confidence: float, has_sources: bool) -> dict:
        """
        Assign FACT/HYP/UNK label based on evidence.
        
        Args:
            confidence: Calculated confidence score (0-100)
            has_sources: Whether sources were provided
            
        Returns:
            Step 5 results dictionary
        """
        self.steps_completed.append("step5_classify_claim")
        
        # Get coherence score from self_test if available
        coherence_factor = self.self_test.get_coherence_score() if self.self_test.coherences else 1.0
        
        # Use Classification with coherence integration
        label = self.classification.classify_from_scores(
            confidence=confidence,
            has_sources=has_sources,
            coherence_score=coherence_factor
        )
        
        return {
            "step": 5,
            "name": "Classification",
            "label": label,
            "confidence": confidence,
            "coherence_factor": coherence_factor,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Step 6
    # ------------------------------------------------------------------
    def step6_quantify_confidence(self, sources: list, coherence_score: float) -> float:
        """
        Score the claim credibility from 0 to 100.
        
        Args:
            sources: List of sources
            coherence_score: Coherence score (0-100)
            
        Returns:
            Calculated confidence score
        """
        self.steps_completed.append("step6_quantify_confidence")
        
        # Calculate source contribution (max 50 points)
        source_score = min(len(sources) * 20, 50)
        
        # Combine source and coherence scores
        confidence = (source_score + coherence_score) / 2
        
        return min(confidence, 100)

    # ------------------------------------------------------------------
    # Step 7
    # ------------------------------------------------------------------
    def step7_generate_report(self, all_results: dict) -> dict:
        """
        Generate transparent reasoning chain and full report.
        
        Args:
            all_results: Dictionary containing all step results
            
        Returns:
            Final report dictionary
        """
        self.steps_completed.append("step7_generate_report")
        
        # Generate formatted report based on mode
        formatted_report = None
        if hasattr(self.prompt_strategy, 'generate_report'):
            try:
                formatted_report = self.prompt_strategy.generate_report(
                    statement=self.current_claim,
                    label=all_results.get('step5', {}).get('label', 'UNK'),
                    confidence=all_results.get('step6', {}).get('confidence', 0),
                    sources=all_results.get('step3', {}).get('sources', []),
                    assumptions=all_results.get('step2', {}).get('assumptions', []),
                )
            except (KeyError, TypeError):
                pass
        
        return {
            "step": 7,
            "name": "Reporting",
            "claim": self.current_claim,
            "mode": self.mode,
            "steps_completed": list(self.steps_completed),
            "full_analysis": all_results,
            "formatted_report": formatted_report,
            "status": "completed",
        }

    # ------------------------------------------------------------------
    # Convenience: run the full protocol at once
    # ------------------------------------------------------------------
    def run_full_protocol(self, statement: str, sources: list,
                          coherence_score: float = 75.0) -> dict:
        """
        Execute all 7 steps sequentially and return the report.
        
        Args:
            statement: The claim to evaluate
            sources: List of supporting sources
            coherence_score: Initial coherence score (0-100)
            
        Returns:
            Complete protocol report
        """
        # Reset for new run
        self.steps_completed = []
        self.self_test = SelfTest()
        self.classification = Classification()
        
        # Execute all steps
        r1 = self.step1_formulate_statement(statement)
        r2 = self.step2_extract_assumptions()
        r3 = self.step3_identify_sources(sources)
        r4 = self.step4_test_coherence()
        
        # Calculate confidence
        confidence = self.step6_quantify_confidence(sources, coherence_score)
        
        # Classify
        r5 = self.step5_classify_claim(confidence, len(sources) > 0)

        # Compile results
        all_results = {
            "step1": r1,
            "step2": r2,
            "step3": r3,
            "step4": r4,
            "step5": r5,
            "step6": {"confidence": confidence},
        }

        # Generate final report
        r7 = self.step7_generate_report(all_results)
        self.result = r7
        return self.result

    # ------------------------------------------------------------------
    # Mode-specific methods
    # ------------------------------------------------------------------
    def start_interactive_session(self, statement: str):
        """
        Start an interactive dialogue session (deep-ask mode only).
        
        Args:
            statement: The claim to examine
            
        Returns:
            SocraticDialogueSession instance
            
        Raises:
            ValueError: If not in deep-ask mode
        """
        if self.mode != "deep-ask":
            raise ValueError("Interactive sessions are only available in deep-ask mode")
        
        return self.prompt_strategy.create_dialogue_session(statement)

    def run_auto_analysis(self, statement: str, sources: list,
                          coherence_score: float = 75.0) -> dict:
        """
        Run automated deep analysis (deep-auto mode only).
        
        Args:
            statement: The claim to analyze
            sources: List of sources
            coherence_score: Coherence score (0-100)
            
        Returns:
            Automated analysis results
            
        Raises:
            ValueError: If not in deep-auto mode
        """
        if self.mode != "deep-auto":
            raise ValueError("Auto analysis is only available in deep-auto mode")
        
        # Run the full protocol
        protocol_result = self.run_full_protocol(statement, sources, coherence_score)
        
        # Add deep-auto specific analysis
        if hasattr(self.prompt_strategy, 'run_full_auto_analysis'):
            auto_analysis = self.prompt_strategy.run_full_auto_analysis(
                statement=statement,
                sources=sources,
                coherence_score=coherence_score
            )
            protocol_result['auto_analysis'] = auto_analysis
        
        return protocol_result
