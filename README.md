# Regex to DFA Converter

This project converts a given regular expression (Regex) into a Non-deterministic Finite Automaton (NFA) and then transforms the NFA into a Deterministic Finite Automaton (DFA). The implementation is done in Python.

## Features

- **Regular Expression Parsing**: Parses basic regular expressions including concatenation, alternation (`|`), and Kleene star (`*`).
- **NFA Construction**: Constructs an NFA from the parsed regex.
- **NFA to DFA Conversion**: Converts the NFA into a DFA using the subset construction algorithm.
- **Epsilon Closures**: Computes epsilon closures to handle ε-transitions in the NFA.
- **Graph Representation**: Stores DFA states and transitions in a dictionary format.

## Usage

### Running the Script
To run the script, simply execute:

```bash
python main.py

Example
For the regex:
a(b|c)*

The script generates the following DFA:
DFA:
States: {0, 1, 2, 3}
Alphabet: {'a', 'b', 'c'}
Start State: 0
Accepting States: {3}
Transitions:
  0 --a--> 1
  1 --b--> 2
  1 --c--> 2
  2 --b--> 2
  2 --c--> 2
  2 --ε--> 3

Features:
- Converts a regex into an NFA.

- Transforms the NFA into a DFA.

- Supports basic regex operators:

1. | (OR)

2. * (Kleene star)

3. Concatenation.

Future Improvements:

- Support for + (one or more occurrences) and ? (optional).

- Optimize DFA by minimizing states.

- Add graphical visualization.

License
This project is open-source and available under the MIT License.

Author
OMar Mo









