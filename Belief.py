
class Belief:
    def __init__(self, belief,  plausibilityOrder):
        self.belief = belief
        self.plausibilityOrder = plausibilityOrder

    def __repr__(self):
        return f'Belief({self.belief}, plausibilityOrder={self.plausibilityOrder})'
