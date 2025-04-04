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
