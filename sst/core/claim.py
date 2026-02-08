class Claim:
    def __init__(self, statement: str, label: str, confidence: float, sources: list):
        self.statement = statement
        self.label = label
        self.confidence = confidence
        self.sources = sources

    def __repr__(self):
        return f"Claim(statement={self.statement}, label={self.label}, confidence={self.confidence}, sources={self.sources})"