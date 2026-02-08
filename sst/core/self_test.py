class SelfTest:
    def __init__(self):
        self.assumptions = []
        self.unknowns = []
        self.coherences = []
        self.priorities = []

    def extract_assumptions(self, data):
        # Logic for extracting assumptions from the given data
        self.assumptions = [item for item in data if self.is_assumption(item)]
        return self.assumptions

    def identify_unknowns(self, data):
        # Logic for identifying unknowns
        self.unknowns = [item for item in data if self.is_unknown(item)]
        return self.unknowns

    def evaluate_coherence(self, data):
        # Logic for coherence evaluation of extracted assumptions
        for assumption in self.assumptions:
            coherence_score = self.calculate_coherence(assumption, data)
            self.coherences.append((assumption, coherence_score))
        return self.coherences

    def establish_priorities(self, criteria):
        # Logic for establishing priorities based on criteria
        self.priorities = sorted(self.assumptions, key=lambda x: criteria.get(x, 0))
        return self.priorities

    def propose_questions(self):
        # Logic for proposing questions based on assumptions and unknowns
        questions = []
        for assumption in self.assumptions:
            questions.append(f"What if {assumption}?\n")
        return questions

    def is_assumption(self, item):
        # Placeholder for assumption-checking logic
        return True

    def is_unknown(self, item):
        # Placeholder for unknown-checking logic
        return True

    def calculate_coherence(self, assumption, data):
        # Placeholder for coherence calculation logic
        return 1.0
