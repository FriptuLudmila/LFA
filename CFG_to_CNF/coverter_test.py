class CFG:
    def __init__(self, start_symbol, productions):
        self.start_symbol = start_symbol
        self.productions = {nt: set(map(tuple, p)) for nt, p in productions.items()}

    def remove_null_productions(self):
        nullable = set()
        for non_terminal, rhs in self.productions.items():
            for symbols in rhs:
                if symbols == ('ε',):
                    nullable.add(non_terminal)

        changed = True
        while changed:
            changed = False
            for non_terminal, rhs in self.productions.items():
                for symbols in rhs:
                    if all(symbol in nullable for symbol in symbols) and non_terminal not in nullable:
                        nullable.add(non_terminal)
                        changed = True

        new_productions = {}
        for non_terminal, rhs in self.productions.items():
            new_set = set()
            for symbols in rhs:
                if symbols != ('ε',) or (non_terminal == self.start_symbol and len(rhs) == 1):
                    new_set.add(symbols)
            new_productions[non_terminal] = new_set

        for non_terminal, rhs in new_productions.items():
            expanded_productions = set()
            for symbols in rhs:
                subsets = self._generate_subsets(symbols, nullable)
                expanded_productions.update(subsets)
            new_productions[non_terminal] = expanded_productions
        self.productions = new_productions
        print("After removing null productions:")
        self.display_productions()

    def remove_unit_productions(self):
        import collections
        unit_productions = collections.defaultdict(set)
        non_unit_productions = collections.defaultdict(set)

        for non_terminal, prods in self.productions.items():
            for prod in prods:
                if len(prod) == 1 and prod[0].isupper():
                    unit_productions[non_terminal].add(prod[0])
                else:
                    non_unit_productions[non_terminal].add(prod)

        changes = True
        while changes:
            changes = False
            for non_terminal in list(unit_productions.keys()):
                current_reach = unit_productions[non_terminal]
                for target in list(current_reach):
                    new_reach = unit_productions[target]
                    if not new_reach.issubset(current_reach):
                        unit_productions[non_terminal].update(new_reach)
                        changes = True

        for non_terminal in unit_productions:
            for target in unit_productions[non_terminal]:
                non_unit_productions[non_terminal].update(non_unit_productions[target])

        self.productions = non_unit_productions
        print("After removing unit productions:")
        self.display_productions()

    def remove_inaccessible_symbols(self):
        accessible = set()
        stack = [self.start_symbol]
        accessible.add(self.start_symbol)

        while stack:
            current = stack.pop()
            for production in self.productions.get(current, []):
                for symbol in production:
                    if symbol.isupper() and symbol not in accessible:  # Assuming non-terminals are uppercase
                        accessible.add(symbol)
                        stack.append(symbol)

        self.productions = {nt: prods for nt, prods in self.productions.items() if nt in accessible}
        print("After removing inaccessible symbols:")
        self.display_productions()

    def convert_to_cnf(self):
        new_productions = {nt: set() for nt in self.productions}
        new_non_terminals = {}
        terminal_map = {}
        new_nt_counter = 1  # Counter for new non-terminals

        # Step 1: Replace terminals in multi-symbol productions
        for non_terminal, prods in self.productions.items():
            for prod in prods:
                if len(prod) > 1:
                    new_prod = []
                    for symbol in prod:
                        if symbol.islower():  # Assuming terminals are lowercase
                            if symbol not in terminal_map:
                                new_nt = f'<Z{new_nt_counter}>'
                                terminal_map[symbol] = new_nt
                                new_productions[new_nt] = {(symbol,)}
                                new_nt_counter += 1
                            new_prod.append(terminal_map[symbol])
                        else:
                            new_prod.append(symbol)
                    new_productions[non_terminal].add(tuple(new_prod))
                else:
                    new_productions[non_terminal].add(prod)

        # Step 2: Reduce RHS to two symbols
        pair_map = {}
        final_productions = {nt: set() for nt in new_productions}
        for non_terminal, prods in new_productions.items():
            for prod in prods:
                while len(prod) > 2:
                    A, B, *rest = prod
                    pair = (A, B)
                    if pair not in pair_map:
                        new_nt = f'<Z{new_nt_counter}>'
                        pair_map[pair] = new_nt
                        final_productions[new_nt] = {pair}
                        new_nt_counter += 1
                    new_prod_nt = pair_map[pair]
                    prod = (new_prod_nt,) + tuple(rest)
                final_productions[non_terminal].add(prod)
        self.productions = final_productions
        print("After converting to Chomsky Normal Form:")
        self.display_productions()

    def _generate_subsets(self, symbols, nullable):
        from itertools import combinations
        result = set()
        indexes = [i for i, symbol in enumerate(symbols) if symbol in nullable]
        for r in range(len(indexes) + 1):
            for combo in combinations(indexes, r):
                new_prod = list(symbols)
                for idx in combo:
                    new_prod[idx] = 'ε'
                filtered_prod = tuple(s for s in new_prod if s != 'ε')
                if filtered_prod:
                    result.add(filtered_prod)
        return result

    def display_productions(self):
        for non_terminal, productions in self.productions.items():
            print(f"{non_terminal} ->")
            for prod in productions:
                print("   ", " ".join(prod))


# Example grammar
productions = {
    'S': [['d', 'B'], ['A', 'B']],
    'A': [['d'], ['d', 'S'], ['ε'], ['a', 'A', 'a', 'A', 'b']],
    'B': [['a'], ['a', 'S'], ['A']],
    'D': [['A', 'b', 'a']]
}
grammar = CFG('S', productions)
grammar.remove_null_productions()
grammar.remove_unit_productions()
grammar.remove_inaccessible_symbols()
grammar.convert_to_cnf()
