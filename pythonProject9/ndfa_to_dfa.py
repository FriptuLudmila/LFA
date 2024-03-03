from graphviz import Digraph


class NDFA:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.input_symbols = {'a', 'b', 'c'}
        self.transitions = {
            'q0': {'a': {'q1'}, 'b': {'q2'}},
            'q1': {'a': {'q3'}, 'b': {'q2'}},
            'q2': {'c': {'q0', 'q3'}},
            'q3': {}
        }
        self.start_state = 'q0'
        self.accept_states = {'q3'}


class DFA:
    def __init__(self):
        self.states = set()
        self.input_symbols = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def from_ndfa(self, ndfa):
        self.input_symbols = ndfa.input_symbols
        unprocessed_states = [frozenset([ndfa.start_state])]
        self.start_state = frozenset([ndfa.start_state])

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            if not current_state in self.states:
                self.states.add(current_state)
                for input_symbol in ndfa.input_symbols:
                    next_state = frozenset(
                        [s for state in current_state for s in ndfa.transitions.get(state, {}).get(input_symbol, [])])
                    if next_state:
                        self.transitions[current_state, input_symbol] = next_state
                        unprocessed_states.append(next_state)

        self.accept_states = {state for state in self.states if ndfa.accept_states.intersection(state)}

    def draw(self, filename='dfa_diagram'):
        dfa_graph = Digraph(comment='The DFA')

        # Helper function to format state names
        def format_state_name(state):

            return ','.join(state) if state else '{}'

        # Add nodes for all states with default shape 'circle'
        for state in self.states:
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            label = format_state_name(state)
            dfa_graph.node(label, shape=shape)

        # Add edges for transitions
        for (src_state, input_symbol), dst_state in self.transitions.items():
            src_label = format_state_name(src_state)
            dst_label = format_state_name(dst_state)
            dfa_graph.edge(src_label, dst_label, label=input_symbol)

        # Special handling to denote the start state with an additional invisible edge
        dfa_graph.attr('node', shape='plaintext', style='invisible')
        start_label = format_state_name(self.start_state)
        dfa_graph.node('start', style='invisible')
        dfa_graph.edge('start', start_label, style='dashed')

        # graph
        dfa_graph.render(filename, view=True, format='png')


ndfa = NDFA()
dfa = DFA()
# Populate the DFA from the NDFA
dfa.from_ndfa(ndfa)


dfa.draw('dfa_diagram')
#print transitions

print("DFA States:", dfa.states)
print("DFA Transitions:", dfa.transitions)
print("DFA Start State:", dfa.start_state)
print("DFA Accept States:", dfa.accept_states)
