
class Belief:
    def __init__(self, belief):
        self.belief = belief
        self.plausibilityOrder = 1.0

    def __repr__(self):
        return f'Belief({self.belief}, plausibilityOrder={self.plausibilityOrder})'
