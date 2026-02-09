"""
DEEP-ASK Prompting Strategy (Maieutic Method)

Human-guided Socratic questioning approach where the system asks
probing questions and the human provides answers, mimicking the
classical Socratic dialogue technique.
"""

from typing import Dict, List, Optional, Tuple


class DeepAskPromptStrategy:
    """
    DEEP-ASK mode prompting strategy.
    
    Uses the Maieutic method (Socratic midwifery) where:
    - The system poses probing questions
    - The human reflects and provides answers
    - Through dialogue, hidden assumptions emerge
    - Truth is "delivered" through questioning
    """

    STRATEGY_NAME = "deep-ask"
    DESCRIPTION = "Maieutic questioning with human guidance"

    # ------------------------------------------------------------------
    # Step 1: Statement Formulation - Clarification Dialogue
    # ------------------------------------------------------------------
    STEP1_QUESTIONS = [
        "What exactly do you mean by this claim?",
        "Can you express this in different words?",
        "What would it look like if this claim were true?",
        "What would it look like if this claim were false?",
        "Is there any ambiguity in your formulation?",
    ]

    STEP1_TEMPLATE = """
🔍 STEP 1: STATEMENT CLARIFICATION

You have stated: "{statement}"

Let us examine this claim together. Please reflect on the following:

{questions}

Take your time to consider each question before proceeding.
"""

    # ------------------------------------------------------------------
    # Step 2: Assumption Extraction - Socratic Probing
    # ------------------------------------------------------------------
    STEP2_QUESTIONS = [
        "What must you already believe for this to be true?",
        "What hidden premises support this claim?",
        "What concepts are you taking for granted?",
        "Could someone disagree with your foundational assumptions?",
        "Are there cultural or contextual assumptions embedded here?",
    ]

    STEP2_TEMPLATE = """
🧠 STEP 2: ASSUMPTION EXCAVATION

Regarding your claim: "{statement}"

Every belief rests on hidden foundations. Let us uncover them:

{questions}

Socrates taught that wisdom begins with acknowledging what we assume.
"""

    # ------------------------------------------------------------------
    # Step 3: Source Identification - Evidence Dialogue
    # ------------------------------------------------------------------
    STEP3_QUESTIONS = [
        "How do you know this to be true?",
        "What evidence would change your mind?",
        "Who else has verified this claim?",
        "Could your sources be mistaken?",
        "Is there a primary source for this knowledge?",
    ]

    STEP3_TEMPLATE = """
📚 STEP 3: SOURCE EXAMINATION

For the claim: "{statement}"

Current sources: {sources}

Knowledge must be traced to its origins:

{questions}

"True knowledge exists in knowing that you know nothing." - Socrates
"""

    # ------------------------------------------------------------------
    # Step 4: Coherence Testing - Logical Examination
    # ------------------------------------------------------------------
    STEP4_QUESTIONS = [
        "Does this claim contradict anything you already know?",
        "What would be the consequences if this were true?",
        "Can you think of a counterexample?",
        "Does this align with related established facts?",
        "Is there a simpler explanation?",
    ]

    STEP4_TEMPLATE = """
⚖️ STEP 4: COHERENCE EXAMINATION

Testing the claim: "{statement}"

Truth must be consistent with itself and with reality:

{questions}

Examine carefully - the unexamined life is not worth living.
"""

    # ------------------------------------------------------------------
    # Step 5: Classification - Judgment Dialogue
    # ------------------------------------------------------------------
    STEP5_TEMPLATE = """
🏷️ STEP 5: CLASSIFICATION DELIBERATION

After our examination of: "{statement}"

Based on our dialogue:
- Confidence level: {confidence}%
- Sources verified: {has_sources}

The claim appears to be: {label}

Do you agree with this classification? 
What would need to change for a different classification?
"""

    # ------------------------------------------------------------------
    # Step 6: Confidence - Certainty Reflection
    # ------------------------------------------------------------------
    STEP6_QUESTIONS = [
        "On a scale of 0-100, how certain are you?",
        "What would increase your certainty?",
        "What doubts remain?",
        "Is absolute certainty possible here?",
    ]

    STEP6_TEMPLATE = """
📊 STEP 6: CONFIDENCE REFLECTION

For the claim: "{statement}"

Let us quantify our certainty:
- Source contribution: {source_score}/50 points
- Coherence assessment: {coherence_score}/100 points
- Combined confidence: {confidence}%

{questions}

Remember: True wisdom is knowing the limits of one's knowledge.
"""

    # ------------------------------------------------------------------
    # Step 7: Final Report
    # ------------------------------------------------------------------
    STEP7_TEMPLATE = """
═══════════════════════════════════════════════════════════════
          SOCRATIC STRESS TEST REPORT (DEEP-ASK MODE)
═══════════════════════════════════════════════════════════════

📜 CLAIM EXAMINED:
   "{statement}"

🏷️ CLASSIFICATION: {label}
📊 CONFIDENCE: {confidence}%

📚 SOURCES CONSULTED ({source_count}):
{sources_list}

🧠 KEY ASSUMPTIONS IDENTIFIED:
{assumptions_list}

❓ QUESTIONS RAISED:
{questions_list}

📝 DIALOGUE SUMMARY:
{summary}

═══════════════════════════════════════════════════════════════
   "The only true wisdom is in knowing you know nothing."
                                              - Socrates
═══════════════════════════════════════════════════════════════
"""

    def __init__(self):
        """Initialize the DeepAskPromptStrategy."""
        self.questions_registry = {
            "step1": self.STEP1_QUESTIONS,
            "step2": self.STEP2_QUESTIONS,
            "step3": self.STEP3_QUESTIONS,
            "step4": self.STEP4_QUESTIONS,
            "step6": self.STEP6_QUESTIONS,
        }
        self.templates = {
            "step1": self.STEP1_TEMPLATE,
            "step2": self.STEP2_TEMPLATE,
            "step3": self.STEP3_TEMPLATE,
            "step4": self.STEP4_TEMPLATE,
            "step5": self.STEP5_TEMPLATE,
            "step6": self.STEP6_TEMPLATE,
            "step7": self.STEP7_TEMPLATE,
        }

    def format_questions(self, questions: List[str]) -> str:
        """Format questions as a numbered list."""
        return "\n".join(f"  {i+1}. {q}" for i, q in enumerate(questions))

    def get_questions(self, step: str) -> List[str]:
        """Get the list of questions for a specific step."""
        return self.questions_registry.get(step, [])

    def get_prompt(self, step: str, **kwargs) -> str:
        """
        Generate a prompt for the specified step.
        
        Args:
            step: The step identifier
            **kwargs: Variables to fill in the template
            
        Returns:
            Formatted prompt string
        """
        template = self.templates.get(step)
        if template is None:
            raise ValueError(f"Unknown step: {step}")

        # Auto-inject questions if step has them
        if step in self.questions_registry and "questions" not in kwargs:
            kwargs["questions"] = self.format_questions(self.questions_registry[step])

        return template.format(**kwargs)

    def format_sources_list(self, sources: List[str]) -> str:
        """Format a list of sources for display."""
        if not sources:
            return "   (No sources provided - a significant concern)"
        return "\n".join(f"   • {source}" for source in sources)

    def format_assumptions_list(self, assumptions: List[str]) -> str:
        """Format a list of assumptions for display."""
        if not assumptions:
            return "   (No explicit assumptions identified)"
        return "\n".join(f"   → {assumption}" for assumption in assumptions)

    def format_questions_list(self, questions: List[str]) -> str:
        """Format a list of questions raised for display."""
        if not questions:
            return "   (No unresolved questions)"
        return "\n".join(f"   ? {question}" for question in questions)

    def generate_report(
        self,
        statement: str,
        label: str,
        confidence: float,
        sources: List[str],
        assumptions: Optional[List[str]] = None,
        questions: Optional[List[str]] = None,
        summary: Optional[str] = None,
    ) -> str:
        """
        Generate the final Socratic dialogue report.
        
        Args:
            statement: The evaluated claim
            label: Classification result (FACT/HYP/UNK)
            confidence: Confidence score (0-100)
            sources: List of sources
            assumptions: List of identified assumptions
            questions: List of unresolved questions
            summary: Dialogue summary
            
        Returns:
            Formatted report string
        """
        return self.templates["step7"].format(
            statement=statement,
            label=label,
            confidence=f"{confidence:.1f}",
            source_count=len(sources),
            sources_list=self.format_sources_list(sources),
            assumptions_list=self.format_assumptions_list(assumptions or []),
            questions_list=self.format_questions_list(questions or []),
            summary=summary or "Dialogue completed through Socratic questioning.",
        )

    def create_dialogue_session(
        self, statement: str
    ) -> "SocraticDialogueSession":
        """
        Create an interactive dialogue session.
        
        Args:
            statement: The claim to examine
            
        Returns:
            A SocraticDialogueSession object
        """
        return SocraticDialogueSession(self, statement)


class SocraticDialogueSession:
    """
    An interactive Socratic dialogue session.
    
    Guides the user through the questioning process step by step.
    """

    def __init__(self, strategy: DeepAskPromptStrategy, statement: str):
        self.strategy = strategy
        self.statement = statement
        self.current_step = 1
        self.responses: Dict[str, List[str]] = {}
        self.completed = False

    def get_current_prompt(self) -> str:
        """Get the prompt for the current step."""
        step_key = f"step{self.current_step}"
        return self.strategy.get_prompt(step_key, statement=self.statement)

    def get_current_questions(self) -> List[str]:
        """Get the questions for the current step."""
        step_key = f"step{self.current_step}"
        return self.strategy.get_questions(step_key)

    def submit_response(self, response: str) -> Tuple[bool, str]:
        """
        Submit a response for the current step.
        
        Args:
            response: The user's response
            
        Returns:
            Tuple of (is_complete, next_prompt_or_report)
        """
        step_key = f"step{self.current_step}"
        
        if step_key not in self.responses:
            self.responses[step_key] = []
        self.responses[step_key].append(response)

        if self.current_step < 7:
            self.current_step += 1
            return (False, self.get_current_prompt())
        else:
            self.completed = True
            return (True, "Dialogue complete. Generating report...")

    def is_complete(self) -> bool:
        """Check if the dialogue is complete."""
        return self.completed
