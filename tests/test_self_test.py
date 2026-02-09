"""
Tests for the SelfTest class.
"""

import pytest
from sst.core.self_test import SelfTest


class TestSelfTest:
    """Test suite for the SelfTest class."""

    def test_self_test_init(self):
        """Test SelfTest initialization."""
        st = SelfTest()
        assert st.assumptions == []
        assert st.unknowns == []
        assert st.coherences == []
        assert st.priorities == []

    def test_extract_assumptions(self):
        """Test assumption extraction from data."""
        st = SelfTest()
        data = ["Assumption 1", "Assumption 2", "Assumption 3"]
        result = st.extract_assumptions(data)
        # With default is_assumption returning True, all items are assumptions
        assert len(result) == 3
        assert st.assumptions == data

    def test_extract_assumptions_empty(self):
        """Test assumption extraction with empty data."""
        st = SelfTest()
        result = st.extract_assumptions([])
        assert result == []
        assert st.assumptions == []

    def test_identify_unknowns(self):
        """Test unknown identification."""
        st = SelfTest()
        data = ["Unknown 1", "Unknown 2"]
        result = st.identify_unknowns(data)
        # With default is_unknown returning True, all items are unknowns
        assert len(result) == 2
        assert st.unknowns == data

    def test_evaluate_coherence(self):
        """Test coherence evaluation."""
        st = SelfTest()
        st.extract_assumptions(["Premise A", "Premise B"])
        data = ["Context data"]
        result = st.evaluate_coherence(data)
        # Each assumption should have a coherence score
        assert len(result) == 2
        for assumption, score in result:
            assert score == 1.0  # Default placeholder returns 1.0

    def test_evaluate_coherence_empty_assumptions(self):
        """Test coherence evaluation with no assumptions."""
        st = SelfTest()
        result = st.evaluate_coherence(["Data"])
        assert result == []

    def test_establish_priorities(self):
        """Test priority establishment."""
        st = SelfTest()
        st.assumptions = ["Low", "High", "Medium"]
        criteria = {"Low": 1, "Medium": 5, "High": 10}
        result = st.establish_priorities(criteria)
        # Should be sorted by criteria values (descending - higher priority first)
        assert result[0] == "High"
        assert result[-1] == "Low"

    def test_propose_questions(self):
        """Test question generation from assumptions."""
        st = SelfTest()
        st.assumptions = ["the earth is flat", "gravity exists"]
        questions = st.propose_questions()
        # New implementation generates multiple questions per assumption
        assert len(questions) >= 2
        # Check that questions are generated
        assert any("the earth is flat" in q for q in questions)
        assert any("gravity exists" in q for q in questions)

    def test_propose_questions_empty(self):
        """Test question generation with no assumptions."""
        st = SelfTest()
        questions = st.propose_questions()
        assert questions == []

    def test_is_assumption_default(self):
        """Test is_assumption behavior with real logic."""
        st = SelfTest()
        # Statements with "is", "are", etc. are detected as assumptions
        assert st.is_assumption("Water is wet") is True
        assert st.is_assumption("The sky is blue") is True
        # Empty strings return False
        assert st.is_assumption("") is False

    def test_is_unknown_default(self):
        """Test is_unknown behavior with real logic."""
        st = SelfTest()
        # Statements with uncertainty indicators
        assert st.is_unknown("This might be true") is True
        assert st.is_unknown("Perhaps we should consider") is True
        # Questions indicate unknowns
        assert st.is_unknown("What is this?") is True
        # Definitive statements without uncertainty
        assert st.is_unknown("Water is wet") is False

    def test_calculate_coherence_default(self):
        """Test default calculate_coherence behavior."""
        st = SelfTest()
        # Default implementation returns 1.0
        score = st.calculate_coherence("assumption", ["data"])
        assert score == 1.0

    def test_full_workflow(self):
        """Test complete SelfTest workflow."""
        st = SelfTest()

        # Step 1: Extract assumptions (statements with assumptive language)
        data = ["Water is wet", "The sky is blue", "Gravity exists"]
        assumptions = st.extract_assumptions(data)
        assert len(assumptions) == 3

        # Step 2: Identify unknowns
        unknowns = st.identify_unknowns(["This might be unknown"])
        assert len(unknowns) == 1

        # Step 3: Evaluate coherence
        coherence = st.evaluate_coherence(data)
        assert len(coherence) == 3

        # Step 4: Establish priorities (descending order - higher first)
        criteria = {"Water is wet": 3, "The sky is blue": 1, "Gravity exists": 2}
        priorities = st.establish_priorities(criteria)
        assert priorities[0] == "Water is wet"  # Highest priority value first

        # Step 5: Propose questions
        questions = st.propose_questions()
        assert len(questions) >= 3  # At least one question per assumption
