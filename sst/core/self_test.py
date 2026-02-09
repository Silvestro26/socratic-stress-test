"""
SelfTest Module - Epistemic Self-Examination

Implements the Socratic self-examination process for evaluating
claims, extracting assumptions, and testing coherence.
"""

import re
from typing import List, Tuple, Dict, Any, Optional


class SelfTest:
    """
    Performs epistemic self-examination on claims and statements.
    
    This class implements the core Socratic methodology for:
    - Extracting implicit assumptions from statements
    - Identifying unknown or uncertain elements
    - Evaluating logical coherence
    - Proposing clarifying questions
    """

    # Indicators of assumptive language
    ASSUMPTION_INDICATORS = [
        "is", "are", "was", "were", "will", "must", "should",
        "always", "never", "all", "none", "every", "no one",
        "obviously", "clearly", "certainly", "definitely",
    ]

    # Indicators of uncertainty/unknown
    UNCERTAINTY_INDICATORS = [
        "might", "may", "could", "perhaps", "possibly", "probably",
        "seems", "appears", "suggests", "indicates", "uncertain",
        "unknown", "unclear", "ambiguous", "questionable",
    ]

    # Hedging words that reduce coherence
    HEDGING_WORDS = [
        "some", "many", "few", "often", "sometimes", "usually",
        "generally", "typically", "tends to", "in some cases",
    ]

    # Contradictory word pairs
    CONTRADICTORY_PAIRS = [
        ("always", "never"),
        ("all", "none"),
        ("increase", "decrease"),
        ("more", "less"),
        ("true", "false"),
        ("yes", "no"),
    ]

    def __init__(self):
        """Initialize SelfTest with empty collections."""
        self.assumptions: List[str] = []
        self.unknowns: List[str] = []
        self.coherences: List[Tuple[str, float]] = []
        self.priorities: List[str] = []
        self._analysis_cache: Dict[str, Any] = {}

    def extract_assumptions(self, data: List[str]) -> List[str]:
        """
        Extract implicit assumptions from given data.
        
        Args:
            data: List of statements to analyze
            
        Returns:
            List of identified assumptions
        """
        self.assumptions = [item for item in data if self.is_assumption(item)]
        return self.assumptions

    def identify_unknowns(self, data: List[str]) -> List[str]:
        """
        Identify unknown or uncertain elements in data.
        
        Args:
            data: List of statements to analyze
            
        Returns:
            List of items containing uncertainty
        """
        self.unknowns = [item for item in data if self.is_unknown(item)]
        return self.unknowns

    def evaluate_coherence(self, data: List[str]) -> List[Tuple[str, float]]:
        """
        Evaluate logical coherence of extracted assumptions.
        
        Args:
            data: Context data for coherence evaluation
            
        Returns:
            List of (assumption, coherence_score) tuples
        """
        self.coherences = []
        for assumption in self.assumptions:
            coherence_score = self.calculate_coherence(assumption, data)
            self.coherences.append((assumption, coherence_score))
        return self.coherences

    def establish_priorities(self, criteria: Dict[str, float]) -> List[str]:
        """
        Establish priority order for assumptions based on criteria.
        
        Args:
            criteria: Dictionary mapping assumptions to priority scores
            
        Returns:
            Sorted list of assumptions by priority
        """
        self.priorities = sorted(
            self.assumptions,
            key=lambda x: criteria.get(x, 0),
            reverse=True  # Higher priority first
        )
        return self.priorities

    def propose_questions(self) -> List[str]:
        """
        Generate Socratic questions based on assumptions and unknowns.
        
        Returns:
            List of probing questions
        """
        questions = []
        
        # Questions about assumptions
        for assumption in self.assumptions:
            questions.append(f"What if {assumption}?\n")
            questions.append(f"How do we know that {assumption}?\n")
        
        # Questions about unknowns
        for unknown in self.unknowns:
            questions.append(f"What would clarify {unknown}?\n")
        
        return questions

    def is_assumption(self, item: str) -> bool:
        """
        Determine if an item contains assumptive language.
        
        An assumption is detected when:
        - Contains definitive language (is, are, must, always)
        - Makes universal claims (all, every, none)
        - States something as obvious/certain
        
        Args:
            item: Statement to analyze
            
        Returns:
            True if item appears to contain assumptions
        """
        if not item or not isinstance(item, str):
            return False
        
        item_lower = item.lower()
        
        # Check for assumption indicators
        for indicator in self.ASSUMPTION_INDICATORS:
            # Use word boundary matching
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, item_lower):
                return True
        
        # Statements that look like facts are assumptions unless proven
        # (Short statements with periods are often declarative)
        if len(item) > 5 and not any(char in item for char in "?!"):
            return True
        
        return False

    def is_unknown(self, item: str) -> bool:
        """
        Determine if an item contains uncertainty indicators.
        
        Args:
            item: Statement to analyze
            
        Returns:
            True if item appears to contain uncertainty
        """
        if not item or not isinstance(item, str):
            return False
        
        item_lower = item.lower()
        
        # Check for uncertainty indicators
        for indicator in self.UNCERTAINTY_INDICATORS:
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, item_lower):
                return True
        
        # Questions indicate unknowns
        if "?" in item:
            return True
        
        return False

    def calculate_coherence(self, assumption: str, data: List[str]) -> float:
        """
        Calculate coherence score for an assumption in context.
        
        Coherence is evaluated based on:
        - Internal consistency (no self-contradiction)
        - Specificity (less hedging = more coherent)
        - Consistency with context data
        
        Args:
            assumption: The assumption to evaluate
            data: Context data for consistency checking
            
        Returns:
            Coherence score from 0.0 to 1.0
        """
        if not assumption:
            return 0.0
        
        score = 1.0  # Start with perfect coherence
        assumption_lower = assumption.lower()
        
        # Penalty for hedging words (reduces certainty)
        hedging_count = sum(
            1 for word in self.HEDGING_WORDS
            if re.search(r'\b' + re.escape(word) + r'\b', assumption_lower)
        )
        score -= hedging_count * 0.1  # -10% per hedging word
        
        # Penalty for internal contradictions
        for word1, word2 in self.CONTRADICTORY_PAIRS:
            if word1 in assumption_lower and word2 in assumption_lower:
                score -= 0.3  # Major penalty for contradiction
        
        # Bonus for specificity (longer, detailed statements)
        if len(assumption) > 50:
            score += 0.1
        
        # Check consistency with context data
        if data:
            context_text = " ".join(data).lower()
            # Penalty if assumption contradicts context
            for word1, word2 in self.CONTRADICTORY_PAIRS:
                if word1 in assumption_lower and word2 in context_text:
                    score -= 0.2
        
        # Clamp score between 0 and 1
        return max(0.0, min(1.0, score))

    def analyze_statement(self, statement: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a single statement.
        
        Args:
            statement: The statement to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Extract and analyze
        self.extract_assumptions([statement])
        self.identify_unknowns([statement])
        coherence_results = self.evaluate_coherence([statement])
        questions = self.propose_questions()
        
        # Calculate overall coherence score
        if coherence_results:
            avg_coherence = sum(score for _, score in coherence_results) / len(coherence_results)
        else:
            avg_coherence = 0.5  # Default for no assumptions
        
        return {
            "statement": statement,
            "is_assumption": self.is_assumption(statement),
            "has_uncertainty": self.is_unknown(statement),
            "assumptions": self.assumptions,
            "unknowns": self.unknowns,
            "coherence_score": avg_coherence,
            "coherence_details": coherence_results,
            "proposed_questions": questions,
        }

    def get_coherence_score(self) -> float:
        """
        Get the average coherence score from the last evaluation.
        
        Returns:
            Average coherence score (0.0 to 1.0)
        """
        if not self.coherences:
            return 0.5  # Default neutral score
        return sum(score for _, score in self.coherences) / len(self.coherences)
