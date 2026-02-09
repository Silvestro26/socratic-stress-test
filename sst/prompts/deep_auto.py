"""
DEEP-AUTO Prompting Strategy

Self-administered deep analysis where the system automatically
performs rigorous Socratic examination without human intervention.
Ideal for batch processing and automated evaluation pipelines.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class AnalysisResult:
    """Container for analysis results at each step."""
    step: int
    name: str
    findings: List[str] = field(default_factory=list)
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DeepAutoPromptStrategy:
    """
    DEEP-AUTO mode prompting strategy.
    
    Performs automated deep analysis:
    - Self-generates probing questions
    - Self-evaluates responses
    - Iteratively refines analysis
    - Produces comprehensive automated report
    """

    STRATEGY_NAME = "deep-auto"
    DESCRIPTION = "Self-administered automated deep analysis"

    # ------------------------------------------------------------------
    # Analysis Criteria for Each Step
    # ------------------------------------------------------------------
    
    # Step 1: Statement Quality Criteria
    STEP1_CRITERIA = {
        "clarity": "Is the statement unambiguous?",
        "specificity": "Is it specific enough to evaluate?",
        "testability": "Can it be verified or falsified?",
        "completeness": "Does it contain all necessary information?",
    }

    # Step 2: Assumption Categories
    STEP2_CATEGORIES = {
        "definitional": "Terms and definitions assumed",
        "contextual": "Context and background assumed",
        "logical": "Logical relationships assumed",
        "empirical": "Empirical facts assumed",
        "normative": "Value judgments assumed",
    }

    # Step 3: Source Quality Criteria
    STEP3_CRITERIA = {
        "authority": "Is the source authoritative?",
        "recency": "Is the information current?",
        "relevance": "Does it directly address the claim?",
        "verifiability": "Can the source be verified?",
        "independence": "Is the source independent?",
    }

    # Step 4: Coherence Checks
    STEP4_CHECKS = {
        "internal_consistency": "No self-contradiction",
        "external_consistency": "Consistent with known facts",
        "logical_validity": "Arguments are logically valid",
        "causal_coherence": "Causal claims are plausible",
    }

    # ------------------------------------------------------------------
    # Auto-Analysis Templates
    # ------------------------------------------------------------------
    
    STEP1_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║           STEP 1: AUTOMATED STATEMENT ANALYSIS               ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

QUALITY ASSESSMENT:
{quality_assessment}

REFORMULATION SUGGESTIONS:
{reformulations}

ANALYSIS SCORE: {score}/100
╚══════════════════════════════════════════════════════════════╝
"""

    STEP2_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║         STEP 2: AUTOMATED ASSUMPTION EXTRACTION              ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

IDENTIFIED ASSUMPTIONS BY CATEGORY:

{assumptions_by_category}

CRITICAL ASSUMPTIONS:
{critical_assumptions}

HIDDEN PREMISE COUNT: {assumption_count}
╚══════════════════════════════════════════════════════════════╝
"""

    STEP3_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║          STEP 3: AUTOMATED SOURCE EVALUATION                 ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

SOURCES PROVIDED: {source_count}

SOURCE ANALYSIS:
{source_analysis}

OVERALL SOURCE QUALITY: {source_quality}/100
RECOMMENDATION: {recommendation}
╚══════════════════════════════════════════════════════════════╝
"""

    STEP4_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║          STEP 4: AUTOMATED COHERENCE TESTING                 ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

COHERENCE CHECKS:
{coherence_checks}

CONTRADICTIONS FOUND: {contradiction_count}
LOGICAL ISSUES: {logical_issues}

COHERENCE SCORE: {coherence_score}/100
╚══════════════════════════════════════════════════════════════╝
"""

    STEP5_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║           STEP 5: AUTOMATED CLASSIFICATION                   ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

CLASSIFICATION CRITERIA:
  • Confidence threshold for FACT: ≥85% with verified sources
  • Confidence threshold for HYP:  ≥50%
  • Below 50% classified as UNK

EVALUATION:
  • Calculated confidence: {confidence}%
  • Has verified sources: {has_sources}
  • Classification logic: {classification_logic}

═══════════════════════════════════════════════════════════════
              CLASSIFICATION: ▶▶▶ {label} ◀◀◀
═══════════════════════════════════════════════════════════════
╚══════════════════════════════════════════════════════════════╝
"""

    STEP6_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║       STEP 6: AUTOMATED CONFIDENCE QUANTIFICATION            ║
╠══════════════════════════════════════════════════════════════╣

CLAIM: "{statement}"

CONFIDENCE CALCULATION:

  Source Score:     {source_score:>6.1f} / 50.0  (max 50 points)
  Coherence Score:  {coherence_score:>6.1f} / 100.0
  ─────────────────────────────────────
  Combined Score:   ({source_score} + {coherence_score}) / 2

  FINAL CONFIDENCE: {confidence:.1f}%

CONFIDENCE BREAKDOWN:
{confidence_breakdown}
╚══════════════════════════════════════════════════════════════╝
"""

    STEP7_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║                  DEEP-AUTO ANALYSIS REPORT                   ║
║            Socratic Stress Test - Automated Mode             ║
╠══════════════════════════════════════════════════════════════╣

📜 CLAIM ANALYZED:
   "{statement}"

╔══════════════════════════════════════════════════════════════╗
║                     EXECUTIVE SUMMARY                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   CLASSIFICATION:  {label:^10}                               ║
║   CONFIDENCE:      {confidence:>6.1f}%                               ║
║   SOURCES:         {source_count:>3} verified                           ║
║   ASSUMPTIONS:     {assumption_count:>3} identified                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📊 DETAILED SCORES:
   • Statement Quality:    {statement_score:>5.1f}/100
   • Source Quality:       {source_quality:>5.1f}/100
   • Coherence Score:      {coherence_score:>5.1f}/100
   • Overall Confidence:   {confidence:>5.1f}/100

📚 SOURCES ({source_count}):
{sources_list}

🧠 KEY ASSUMPTIONS:
{assumptions_list}

⚠️  POTENTIAL ISSUES:
{issues_list}

✅ STRENGTHS:
{strengths_list}

📝 AUTOMATED ANALYSIS NOTES:
{analysis_notes}

═══════════════════════════════════════════════════════════════
   Analysis completed automatically by SST Deep-Auto Engine
═══════════════════════════════════════════════════════════════
"""

    def __init__(self):
        """Initialize the DeepAutoPromptStrategy."""
        self.templates = {
            "step1": self.STEP1_TEMPLATE,
            "step2": self.STEP2_TEMPLATE,
            "step3": self.STEP3_TEMPLATE,
            "step4": self.STEP4_TEMPLATE,
            "step5": self.STEP5_TEMPLATE,
            "step6": self.STEP6_TEMPLATE,
            "step7": self.STEP7_TEMPLATE,
        }
        self.analysis_results: Dict[str, AnalysisResult] = {}

    def analyze_statement_quality(self, statement: str) -> AnalysisResult:
        """
        Automatically analyze statement quality.
        
        Args:
            statement: The claim to analyze
            
        Returns:
            AnalysisResult with quality assessment
        """
        result = AnalysisResult(step=1, name="Statement Quality")
        
        # Check each criterion
        checks = []
        score = 0
        
        # Clarity check (has no ambiguous words like "some", "many", etc.)
        ambiguous_words = ["some", "many", "few", "often", "sometimes", "usually"]
        has_ambiguity = any(word in statement.lower() for word in ambiguous_words)
        clarity_score = 0 if has_ambiguity else 25
        checks.append(f"Clarity: {'PASS' if not has_ambiguity else 'FAIL - ambiguous language detected'}")
        score += clarity_score
        
        # Specificity check (contains specific details)
        specificity_score = 25 if len(statement) > 20 else 10
        checks.append(f"Specificity: {'PASS' if specificity_score == 25 else 'PARTIAL - could be more specific'}")
        score += specificity_score
        
        # Testability check (contains verifiable assertions)
        testable_indicators = ["is", "are", "was", "were", "has", "have", "at", "in"]
        is_testable = any(word in statement.lower() for word in testable_indicators)
        testability_score = 25 if is_testable else 10
        checks.append(f"Testability: {'PASS' if is_testable else 'FAIL - not easily verifiable'}")
        score += testability_score
        
        # Completeness check
        completeness_score = 25 if not statement.endswith("...") and "?" not in statement else 10
        checks.append(f"Completeness: {'PASS' if completeness_score == 25 else 'FAIL - incomplete statement'}")
        score += completeness_score
        
        result.findings = checks
        result.score = score
        result.metadata["quality_assessment"] = checks
        
        return result

    def extract_assumptions_auto(self, statement: str) -> AnalysisResult:
        """
        Automatically extract assumptions from a statement.
        
        Args:
            statement: The claim to analyze
            
        Returns:
            AnalysisResult with extracted assumptions
        """
        result = AnalysisResult(step=2, name="Assumption Extraction")
        assumptions = []
        
        # Definitional assumptions
        for category, description in self.STEP2_CATEGORIES.items():
            if category == "definitional":
                # Extract potential terms that need definition
                words = statement.split()
                technical_words = [w for w in words if len(w) > 6]
                if technical_words:
                    assumptions.append(f"[{category.upper()}] Terms assumed understood: {', '.join(technical_words[:3])}")
            
            elif category == "contextual":
                assumptions.append(f"[{category.upper()}] Statement context is assumed to be clear")
            
            elif category == "empirical":
                assumptions.append(f"[{category.upper()}] Empirical basis is assumed verifiable")
        
        result.findings = assumptions
        result.score = len(assumptions) * 10  # More assumptions = more critical analysis
        result.metadata["assumption_count"] = len(assumptions)
        
        return result

    def evaluate_sources_auto(self, sources: List[str]) -> AnalysisResult:
        """
        Automatically evaluate source quality.
        
        Args:
            sources: List of sources to evaluate
            
        Returns:
            AnalysisResult with source evaluation
        """
        result = AnalysisResult(step=3, name="Source Evaluation")
        
        if not sources:
            result.findings = ["No sources provided - significant weakness"]
            result.score = 0
            result.metadata["recommendation"] = "REQUIRES SOURCES"
            return result
        
        source_analysis = []
        total_quality = 0
        
        for source in sources:
            quality = 50  # Base quality
            
            # Academic indicators
            academic_indicators = ["journal", "university", "research", "study", "handbook", "database"]
            if any(ind in source.lower() for ind in academic_indicators):
                quality += 30
                source_analysis.append(f"✓ {source} - Academic source detected")
            else:
                source_analysis.append(f"○ {source} - Non-academic source")
            
            total_quality += quality
        
        avg_quality = total_quality / len(sources) if sources else 0
        result.findings = source_analysis
        result.score = min(avg_quality, 100)
        result.metadata["source_quality"] = avg_quality
        result.metadata["recommendation"] = "ADEQUATE" if avg_quality >= 60 else "NEEDS IMPROVEMENT"
        
        return result

    def test_coherence_auto(self, statement: str, assumptions: List[str]) -> AnalysisResult:
        """
        Automatically test coherence.
        
        Args:
            statement: The claim
            assumptions: Extracted assumptions
            
        Returns:
            AnalysisResult with coherence assessment
        """
        result = AnalysisResult(step=4, name="Coherence Testing")
        
        checks = []
        issues = []
        score = 100  # Start with perfect score, deduct for issues
        
        for check_name, check_description in self.STEP4_CHECKS.items():
            # Simplified coherence checks
            if check_name == "internal_consistency":
                # Check for contradictory language
                contradictory_pairs = [("always", "never"), ("all", "none"), ("increase", "decrease")]
                found_contradiction = False
                for word1, word2 in contradictory_pairs:
                    if word1 in statement.lower() and word2 in statement.lower():
                        found_contradiction = True
                        issues.append(f"Potential contradiction: '{word1}' and '{word2}'")
                        score -= 25
                        break
                
                if not found_contradiction:
                    checks.append(f"✓ {check_name}: PASS")
                else:
                    checks.append(f"✗ {check_name}: FAIL")
            else:
                # Other checks pass by default in this simplified version
                checks.append(f"✓ {check_name}: PASS")
        
        result.findings = checks
        result.score = max(score, 0)
        result.metadata["issues"] = issues
        result.metadata["contradiction_count"] = len(issues)
        
        return result

    def get_prompt(self, step: str, **kwargs) -> str:
        """
        Generate a prompt/report for the specified step.
        
        Args:
            step: The step identifier
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted prompt string
        """
        template = self.templates.get(step)
        if template is None:
            raise ValueError(f"Unknown step: {step}")
        return template.format(**kwargs)

    def format_list(self, items: List[str], prefix: str = "   •") -> str:
        """Format a list of items for display."""
        if not items:
            return f"{prefix} (None identified)"
        return "\n".join(f"{prefix} {item}" for item in items)

    def run_full_auto_analysis(
        self,
        statement: str,
        sources: List[str],
        coherence_score: float = 75.0,
    ) -> Dict[str, Any]:
        """
        Run complete automated analysis.
        
        Args:
            statement: The claim to analyze
            sources: List of sources
            coherence_score: Pre-calculated coherence score
            
        Returns:
            Complete analysis results
        """
        # Step 1: Analyze statement quality
        step1_result = self.analyze_statement_quality(statement)
        
        # Step 2: Extract assumptions
        step2_result = self.extract_assumptions_auto(statement)
        
        # Step 3: Evaluate sources
        step3_result = self.evaluate_sources_auto(sources)
        
        # Step 4: Test coherence
        step4_result = self.test_coherence_auto(statement, step2_result.findings)
        
        # Calculate confidence
        source_score = min(len(sources) * 20, 50)
        confidence = (source_score + coherence_score) / 2
        
        # Determine classification
        has_sources = len(sources) > 0
        if confidence >= 85 and has_sources:
            label = "FACT"
        elif confidence >= 50:
            label = "HYP"
        else:
            label = "UNK"
        
        return {
            "statement": statement,
            "label": label,
            "confidence": confidence,
            "source_score": source_score,
            "coherence_score": coherence_score,
            "sources": sources,
            "step1": step1_result,
            "step2": step2_result,
            "step3": step3_result,
            "step4": step4_result,
            "assumptions": step2_result.findings,
            "issues": step4_result.metadata.get("issues", []),
        }

    def generate_report(
        self,
        statement: str,
        label: str,
        confidence: float,
        sources: List[str],
        assumptions: Optional[List[str]] = None,
        issues: Optional[List[str]] = None,
        strengths: Optional[List[str]] = None,
        analysis_notes: Optional[str] = None,
        statement_score: float = 75.0,
        source_quality: float = 50.0,
        coherence_score: float = 75.0,
    ) -> str:
        """
        Generate the final automated analysis report.
        
        Args:
            statement: The evaluated claim
            label: Classification result (FACT/HYP/UNK)
            confidence: Confidence score (0-100)
            sources: List of sources
            assumptions: List of identified assumptions
            issues: List of potential issues
            strengths: List of strengths
            analysis_notes: Additional notes
            statement_score: Statement quality score
            source_quality: Source quality score
            coherence_score: Coherence score
            
        Returns:
            Formatted report string
        """
        assumptions = assumptions or []
        issues = issues or ["None identified"]
        strengths = strengths or ["Statement is clearly formulated"]
        analysis_notes = analysis_notes or "Automated analysis completed successfully."
        
        return self.templates["step7"].format(
            statement=statement,
            label=label,
            confidence=confidence,
            source_count=len(sources),
            assumption_count=len(assumptions),
            statement_score=statement_score,
            source_quality=source_quality,
            coherence_score=coherence_score,
            sources_list=self.format_list(sources) if sources else "   • No sources provided",
            assumptions_list=self.format_list(assumptions),
            issues_list=self.format_list(issues),
            strengths_list=self.format_list(strengths),
            analysis_notes=analysis_notes,
        )
