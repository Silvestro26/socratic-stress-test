"""
Classification Module - Epistemic State Management

Manages the three-state classification system (FACT/HYP/UNK)
with integrated downgrade logic based on evidence quality.
"""

from typing import Optional, Dict, Any
from sst.core.self_test import SelfTest


class Classification:
    """
    Manages epistemic classification states for claims.
    
    States:
    - FACT (1): High confidence, verified claim
    - HYP (0): Hypothesis, plausible but unverified
    - UNK (-1): Unknown, insufficient evidence
    
    Supports automatic and manual state transitions with
    integrated SelfTest coherence evaluation.
    """

    # State definitions with numeric values for comparison
    STATES = {
        'FACT': 1,   # Highest confidence
        'HYP': 0,    # Medium confidence
        'UNK': -1    # Lowest confidence / unknown
    }

    # Downgrade chain: FACT -> HYP -> UNK
    DOWNGRADE_MAP = {
        'FACT': 'HYP',
        'HYP': 'UNK',
        'UNK': 'UNK',  # Cannot downgrade further
    }

    # Upgrade chain: UNK -> HYP -> FACT
    UPGRADE_MAP = {
        'UNK': 'HYP',
        'HYP': 'FACT',
        'FACT': 'FACT',  # Cannot upgrade further
    }

    def __init__(self):
        """Initialize Classification with no state set."""
        self.states = self.STATES.copy()
        self.current_state: Optional[str] = None
        self.state_history: list = []
        self.downgrade_reasons: list = []

    def set_state(self, state: str) -> None:
        """
        Set the classification state.
        
        Args:
            state: Must be one of FACT, HYP, or UNK
            
        Raises:
            ValueError: If state is not valid
        """
        if state not in self.states:
            raise ValueError(f"Invalid state. Must be one of: {', '.join(self.states.keys())}.")
        
        # Record state change in history
        if self.current_state is not None:
            self.state_history.append({
                'from': self.current_state,
                'to': state,
                'reason': 'manual_set'
            })
        
        self.current_state = state

    def downgrade_state(self, reason: Optional[str] = None) -> str:
        """
        Downgrade the current state by one level.
        
        FACT -> HYP -> UNK (cannot go lower)
        
        Args:
            reason: Optional reason for the downgrade
            
        Returns:
            The new state after downgrade
            
        Raises:
            ValueError: If current state is not set
        """
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        
        old_state = self.current_state
        self.current_state = self.DOWNGRADE_MAP[self.current_state]
        
        # Record the downgrade
        if old_state != self.current_state:
            self.state_history.append({
                'from': old_state,
                'to': self.current_state,
                'reason': reason or 'downgrade'
            })
            if reason:
                self.downgrade_reasons.append(reason)
        
        return self.current_state

    def upgrade_state(self, reason: Optional[str] = None) -> str:
        """
        Upgrade the current state by one level.
        
        UNK -> HYP -> FACT (cannot go higher)
        
        Args:
            reason: Optional reason for the upgrade
            
        Returns:
            The new state after upgrade
            
        Raises:
            ValueError: If current state is not set
        """
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        
        old_state = self.current_state
        self.current_state = self.UPGRADE_MAP[self.current_state]
        
        # Record the upgrade
        if old_state != self.current_state:
            self.state_history.append({
                'from': old_state,
                'to': self.current_state,
                'reason': reason or 'upgrade'
            })
        
        return self.current_state

    def is_fact(self) -> bool:
        """Check if current state is FACT."""
        return self.current_state == 'FACT'

    def is_hyp(self) -> bool:
        """Check if current state is HYP."""
        return self.current_state == 'HYP'

    def is_unk(self) -> bool:
        """Check if current state is UNK."""
        return self.current_state == 'UNK'

    def get_state_value(self) -> int:
        """
        Get the numeric value of the current state.
        
        Returns:
            1 for FACT, 0 for HYP, -1 for UNK
            
        Raises:
            ValueError: If state is not set
        """
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        return self.states[self.current_state]

    def evaluate_with_self_test(
        self,
        statement: str,
        sources: list,
        initial_confidence: float = 75.0
    ) -> Dict[str, Any]:
        """
        Perform integrated evaluation using SelfTest.
        
        This method:
        1. Analyzes the statement for assumptions and coherence
        2. Sets initial classification based on confidence
        3. Applies automatic downgrades based on analysis
        
        Args:
            statement: The claim to evaluate
            sources: List of supporting sources
            initial_confidence: Starting confidence score (0-100)
            
        Returns:
            Dictionary with evaluation results
        """
        st = SelfTest()
        analysis = st.analyze_statement(statement)
        
        # Calculate adjusted confidence
        coherence_factor = analysis['coherence_score']  # 0.0 to 1.0
        adjusted_confidence = initial_confidence * coherence_factor
        
        # Determine initial state based on adjusted confidence and sources
        has_sources = len(sources) > 0
        
        if adjusted_confidence >= 85 and has_sources:
            self.set_state('FACT')
        elif adjusted_confidence >= 50:
            self.set_state('HYP')
        else:
            self.set_state('UNK')
        
        # Apply automatic downgrades based on analysis
        
        # Downgrade if high uncertainty detected
        if analysis['has_uncertainty']:
            self.downgrade_state("Contains uncertainty indicators")
        
        # Downgrade if no sources for a FACT claim
        if self.is_fact() and not has_sources:
            self.downgrade_state("FACT claim lacks sources")
        
        # Downgrade if low coherence
        if coherence_factor < 0.5:
            self.downgrade_state("Low coherence score")
        
        return {
            'statement': statement,
            'initial_confidence': initial_confidence,
            'adjusted_confidence': adjusted_confidence,
            'coherence_factor': coherence_factor,
            'final_state': self.current_state,
            'state_history': self.state_history.copy(),
            'downgrade_reasons': self.downgrade_reasons.copy(),
            'analysis': analysis,
        }

    def classify_from_scores(
        self,
        confidence: float,
        has_sources: bool,
        coherence_score: float = 1.0
    ) -> str:
        """
        Classify based on numeric scores.
        
        Args:
            confidence: Confidence score (0-100)
            has_sources: Whether sources are provided
            coherence_score: Coherence factor (0.0-1.0)
            
        Returns:
            Classification label (FACT/HYP/UNK)
        """
        # Adjust confidence by coherence
        effective_confidence = confidence * coherence_score
        
        if effective_confidence >= 85 and has_sources:
            self.set_state('FACT')
        elif effective_confidence >= 50:
            self.set_state('HYP')
        else:
            self.set_state('UNK')
        
        return self.current_state

    def get_state_description(self) -> str:
        """
        Get a human-readable description of the current state.
        
        Returns:
            Description string
        """
        descriptions = {
            'FACT': "Verified fact with high confidence",
            'HYP': "Hypothesis - plausible but needs verification",
            'UNK': "Unknown - insufficient evidence to classify",
            None: "Not yet classified",
        }
        return descriptions.get(self.current_state, "Invalid state")

    def to_dict(self) -> Dict[str, Any]:
        """
        Export classification state as dictionary.
        
        Returns:
            Dictionary with state information
        """
        return {
            'current_state': self.current_state,
            'state_value': self.get_state_value() if self.current_state else None,
            'description': self.get_state_description(),
            'state_history': self.state_history,
            'downgrade_reasons': self.downgrade_reasons,
        }