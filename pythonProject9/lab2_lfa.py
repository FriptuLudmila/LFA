class FiniteAutomaton:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'a', 'b', 'c'}
        self.transitions = {
            'q0': {'a': 'q1', 'b': 'q2'},
            'q1': {'a': 'q3', 'b': 'q2'},
            'q2': {'c': ['q0', 'q3']},
        }
        self.start_state = 'q0'
        self.accept_states = {'q3'}


    def to_regular_grammar(self):
        grammar = {}
        for state in self.states:
            rules = []
            for symbol, destinations in self.transitions.get(state, {}).items():
                if not isinstance(destinations, list):
                    destinations = [destinations]
                for destination in destinations:
                    if destination in self.accept_states:
                        rules.append(symbol)
                    else:
                        rules.append(f'{symbol}{destination}')
            grammar[state] = rules
        return grammar

    def is_deterministic(self):
        for transitions in self.transitions.values():
            for destinations in transitions.values():
                if isinstance(destinations, list) and len(destinations) > 1:
                    return False  # Nondeterministic if any symbol leads to more than one state
        return True


fa = FiniteAutomaton()
grammar = fa.to_regular_grammar()


for state, rules in grammar.items():
    if rules:  # Only print the state if it has at least one rule
        print(f"{state} --> {'|'.join(rules)}")

print("Is deterministic:", fa.is_deterministic())

