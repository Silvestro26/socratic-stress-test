"""
Tests for the Prompting Strategies module.
"""

import pytest
from sst.prompts import BasicPromptStrategy, DeepAskPromptStrategy, DeepAutoPromptStrategy


class TestBasicPromptStrategy:
    """Test suite for BasicPromptStrategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = BasicPromptStrategy()
        assert strategy.STRATEGY_NAME == "basic"
        assert len(strategy.templates) == 7

    def test_get_prompt_step1(self):
        """Test Step 1 prompt generation."""
        strategy = BasicPromptStrategy()
        prompt = strategy.get_prompt("step1", statement="Test claim")
        assert "Test claim" in prompt
        assert "Clearly formulated" in prompt

    def test_get_prompt_invalid_step(self):
        """Test that invalid step raises ValueError."""
        strategy = BasicPromptStrategy()
        with pytest.raises(ValueError):
            strategy.get_prompt("step99", statement="Test")

    def test_format_sources_list_with_sources(self):
        """Test source formatting with sources."""
        strategy = BasicPromptStrategy()
        sources = ["Source A", "Source B"]
        result = strategy.format_sources_list(sources)
        assert "Source A" in result
        assert "Source B" in result

    def test_format_sources_list_empty(self):
        """Test source formatting without sources."""
        strategy = BasicPromptStrategy()
        result = strategy.format_sources_list([])
        assert "No sources provided" in result

    def test_generate_report(self):
        """Test report generation."""
        strategy = BasicPromptStrategy()
        report = strategy.generate_report(
            statement="Water boils at 100°C",
            label="FACT",
            confidence=90.0,
            sources=["CRC Handbook"],
        )
        assert "Water boils at 100°C" in report
        assert "FACT" in report
        assert "90" in report
        assert "CRC Handbook" in report


class TestDeepAskPromptStrategy:
    """Test suite for DeepAskPromptStrategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = DeepAskPromptStrategy()
        assert strategy.STRATEGY_NAME == "deep-ask"
        assert len(strategy.questions_registry) > 0

    def test_get_questions(self):
        """Test question retrieval."""
        strategy = DeepAskPromptStrategy()
        questions = strategy.get_questions("step1")
        assert len(questions) > 0
        assert "What exactly do you mean" in questions[0]

    def test_format_questions(self):
        """Test question formatting."""
        strategy = DeepAskPromptStrategy()
        questions = ["Question 1", "Question 2"]
        result = strategy.format_questions(questions)
        assert "1. Question 1" in result
        assert "2. Question 2" in result

    def test_get_prompt_with_auto_questions(self):
        """Test prompt generation with auto-injected questions."""
        strategy = DeepAskPromptStrategy()
        prompt = strategy.get_prompt("step1", statement="Test claim")
        assert "Test claim" in prompt
        assert "What exactly do you mean" in prompt

    def test_create_dialogue_session(self):
        """Test dialogue session creation."""
        strategy = DeepAskPromptStrategy()
        session = strategy.create_dialogue_session("Test claim")
        assert session.statement == "Test claim"
        assert session.current_step == 1
        assert not session.is_complete()

    def test_dialogue_session_progression(self):
        """Test dialogue session step progression."""
        strategy = DeepAskPromptStrategy()
        session = strategy.create_dialogue_session("Test claim")
        
        # Start at step 1
        assert session.current_step == 1
        
        # Submit response and advance
        is_complete, _ = session.submit_response("My response")
        assert session.current_step == 2
        assert not is_complete

    def test_generate_report(self):
        """Test Socratic dialogue report generation."""
        strategy = DeepAskPromptStrategy()
        report = strategy.generate_report(
            statement="Test claim",
            label="HYP",
            confidence=60.0,
            sources=["Source 1"],
            assumptions=["Assumption A"],
            questions=["Unresolved question?"],
        )
        assert "Test claim" in report
        assert "HYP" in report
        assert "60.0" in report
        assert "Assumption A" in report
        assert "Socrates" in report


class TestDeepAutoPromptStrategy:
    """Test suite for DeepAutoPromptStrategy."""

    def test_initialization(self):
        """Test strategy initialization."""
        strategy = DeepAutoPromptStrategy()
        assert strategy.STRATEGY_NAME == "deep-auto"
        assert len(strategy.templates) == 7

    def test_analyze_statement_quality(self):
        """Test automated statement quality analysis."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.analyze_statement_quality("Water boils at 100 degrees Celsius")
        
        assert result.step == 1
        assert result.name == "Statement Quality"
        assert result.score > 0
        assert len(result.findings) > 0

    def test_analyze_statement_with_ambiguity(self):
        """Test statement analysis detects ambiguous language."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.analyze_statement_quality("Some people say this is true")
        
        # Should detect "some" as ambiguous
        assert any("ambiguous" in finding.lower() or "fail" in finding.lower() 
                   for finding in result.findings)

    def test_extract_assumptions_auto(self):
        """Test automated assumption extraction."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.extract_assumptions_auto("Complex thermodynamic processes occur")
        
        assert result.step == 2
        assert len(result.findings) > 0
        assert "assumption_count" in result.metadata

    def test_evaluate_sources_auto_with_sources(self):
        """Test source evaluation with academic sources."""
        strategy = DeepAutoPromptStrategy()
        sources = ["Nature Journal Publication", "University Research Study"]
        result = strategy.evaluate_sources_auto(sources)
        
        assert result.step == 3
        assert result.score > 50  # Academic sources should score higher
        assert "Academic source detected" in str(result.findings)

    def test_evaluate_sources_auto_empty(self):
        """Test source evaluation without sources."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.evaluate_sources_auto([])
        
        assert result.score == 0
        assert "REQUIRES SOURCES" in result.metadata["recommendation"]

    def test_test_coherence_auto(self):
        """Test automated coherence testing."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.test_coherence_auto("Test statement", ["Assumption 1"])
        
        assert result.step == 4
        assert result.score <= 100
        assert "contradiction_count" in result.metadata

    def test_run_full_auto_analysis(self):
        """Test complete automated analysis pipeline."""
        strategy = DeepAutoPromptStrategy()
        results = strategy.run_full_auto_analysis(
            statement="Water boils at 100 degrees Celsius at sea level",
            sources=["CRC Handbook of Chemistry"],
            coherence_score=90.0,
        )
        
        assert "statement" in results
        assert "label" in results
        assert "confidence" in results
        assert results["label"] in ["FACT", "HYP", "UNK"]

    def test_generate_report(self):
        """Test automated report generation."""
        strategy = DeepAutoPromptStrategy()
        report = strategy.generate_report(
            statement="Test claim",
            label="FACT",
            confidence=85.0,
            sources=["Academic Source"],
            assumptions=["Key assumption"],
            issues=["Minor issue"],
            strengths=["Strong evidence"],
        )
        
        assert "Test claim" in report
        assert "FACT" in report
        assert "85.0" in report
        assert "Academic Source" in report
        assert "EXECUTIVE SUMMARY" in report

    def test_format_list(self):
        """Test list formatting utility."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.format_list(["Item 1", "Item 2"])
        assert "Item 1" in result
        assert "Item 2" in result

    def test_format_list_empty(self):
        """Test list formatting with empty list."""
        strategy = DeepAutoPromptStrategy()
        result = strategy.format_list([])
        assert "None identified" in result
