class Classification:
    def __init__(self):
        self.states = {
            'FACT': 1,
            'HYP': 0,
            'UNK': -1
        }
        self.current_state = None
    
    def set_state(self, state):
        if state in self.states:
            self.current_state = state
        else:
            raise ValueError("Invalid state. Must be one of: FACT, HYP, UNK.")
    
    def downgrade_state(self):
        if self.current_state is None:
            raise ValueError("Current state is not set.")
        
        # Implement downgrade logic
        if self.current_state == 'FACT':
            self.current_state = 'HYP'
        elif self.current_state == 'HYP':
            self.current_state = 'UNK'
        # UNK is already the lowest state, no downgrade possible
    
    def is_fact(self):
        return self.current_state == 'FACT'
    
    def is_hyp(self):
        return self.current_state == 'HYP'
    
    def is_unk(self):
        return self.current_state == 'UNK'