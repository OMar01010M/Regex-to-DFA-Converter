from collections import deque, defaultdict

class State:
    def __init__(self):
        self.transitions = {}  # char → set(State)
        self.epsilon_transitions = set()  # ε-closures
        self.is_end = False

    def add_transition(self, char, state):
        if char not in self.transitions:
            self.transitions[char] = set()
        self.transitions[char].add(state)

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        end.is_end = True

    @staticmethod
    def from_regex(regex):
        stack = []
        i = 0
        while i < len(regex):
            char = regex[i]
            if char == '(':
                stack.append(char)
            elif char == ')':
                parts = []
                while stack[-1] != '(':
                    parts.append(stack.pop())
                    if not stack:
                        raise ValueError("Unmatched parentheses")
                stack.pop()  # Remove '('
                parts.reverse()

                # Split into alternations
                alternations = []
                current_alt = []
                for item in parts:
                    if item == '|':
                        if not current_alt:
                            raise ValueError("Empty alternation")
                        alternations.append(current_alt)
                        current_alt = []
                    else:
                        current_alt.append(item)
                if not current_alt:
                    raise ValueError("Empty alternation")
                alternations.append(current_alt)

                # Process each alternation
                nfas = []
                for alt in alternations:
                    if not alt:
                        raise ValueError("Empty alternation")
                    current_nfa = alt[0]
                    for elem in alt[1:]:
                        current_nfa = NFA.concatenate(current_nfa, elem)
                    nfas.append(current_nfa)

                # Create union of all alternations
                group_nfa = nfas[0]
                for nfa in nfas[1:]:
                    group_nfa = NFA.union(group_nfa, nfa)
                stack.append(group_nfa)
            elif char == '|':
                stack.append(char)
            elif char == '*':
                if not stack:
                    raise ValueError("Nothing to repeat")
                nfa = stack.pop()
                stack.append(NFA.kleene_star(nfa))
            elif char == '\\':  # Escape character
                i += 1
                if i >= len(regex):
                    raise ValueError("Escape at end")
                stack.append(NFA.single_char(regex[i]))
            else:
                stack.append(NFA.single_char(char))
            i += 1

        # Process remaining operators
        if not stack:
            return NFA.single_char('')  # Empty regex
        
        # Handle | operators
        nfa = stack[0]
        i = 1
        while i < len(stack):
            if stack[i] == '|':
                i += 1
                if i >= len(stack):
                    raise ValueError("Missing right operand")
                right = stack[i]
                nfa = NFA.union(nfa, right)
            else:
                nfa = NFA.concatenate(nfa, stack[i])
            i += 1
        return nfa

    @staticmethod
    def single_char(char):
        start = State()
        end = State()
        start.add_transition(char, end)
        return NFA(start, end)

    @staticmethod
    def concatenate(a, b):
        if not isinstance(a, NFA) or not isinstance(b, NFA):
            raise ValueError("Can only concatenate NFAs")
        a.end.is_end = False
        a.end.epsilon_transitions.add(b.start)
        return NFA(a.start, b.end)

    @staticmethod
    def union(a, b):
        if not isinstance(a, NFA) or not isinstance(b, NFA):
            raise ValueError("Can only union NFAs")
        start = State()
        end = State()
        start.epsilon_transitions.add(a.start)
        start.epsilon_transitions.add(b.start)
        a.end.epsilon_transitions.add(end)
        b.end.epsilon_transitions.add(end)
        a.end.is_end = False
        b.end.is_end = False
        return NFA(start, end)

    @staticmethod
    def kleene_star(nfa):
        if not isinstance(nfa, NFA):
            raise ValueError("Can only apply Kleene star to NFA")
        start = State()
        end = State()
        start.epsilon_transitions.add(nfa.start)
        start.epsilon_transitions.add(end)
        nfa.end.epsilon_transitions.add(nfa.start)
        nfa.end.epsilon_transitions.add(end)
        nfa.end.is_end = False
        return NFA(start, end)

def epsilon_closure(state):
    closure = set()
    stack = [state]
    while stack:
        current = stack.pop()
        if current in closure:
            continue
        closure.add(current)
        for neighbor in current.epsilon_transitions:
            if neighbor not in closure:
                stack.append(neighbor)
    return closure

def nfa_to_dfa(nfa):
    initial_closure = frozenset(epsilon_closure(nfa.start))
    dfa_states = {initial_closure: 0}
    dfa_transitions = defaultdict(dict)
    state_id = 1
    queue = deque([initial_closure])
    alphabet = set()

    while queue:
        current = queue.popleft()

        transitions = defaultdict(set)
        for state in current:
            for char, targets in state.transitions.items():
                if char != '':
                    alphabet.add(char)
                    for target in targets:
                        transitions[char].update(epsilon_closure(target))

        for char, targets in transitions.items():
            target_closure = frozenset(targets)
            if target_closure not in dfa_states:
                dfa_states[target_closure] = state_id
                queue.append(target_closure)
                state_id += 1
            dfa_transitions[dfa_states[current]][char] = dfa_states[target_closure]

    accepting = {sid for closure, sid in dfa_states.items() 
                if any(s.is_end for s in closure)}

    return {
        'states': set(dfa_states.values()),
        'alphabet': alphabet,
        'transitions': dict(dfa_transitions),
        'start': 0,
        'accepting': accepting
    }

# Example usage
if __name__ == "__main__":
    regex = "a(b|c)*"
    try:
        nfa = NFA.from_regex(regex)
        dfa = nfa_to_dfa(nfa)
        print("DFA:")
        print(f"States: {dfa['states']}")
        print(f"Alphabet: {dfa['alphabet']}")
        print(f"Start State: {dfa['start']}")
        print(f"Accepting States: {dfa['accepting']}")
        print("Transitions:")
        for state, trans in dfa['transitions'].items():
            for char, next_state in trans.items():
                print(f"  {state} --{char}--> {next_state}")
    except ValueError as e:
        print(f"Error: {e}")