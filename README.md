# Regex-to-DFA-Converter
This project implements a complete pipeline for converting regular expressions to Deterministic Finite Automata (DFA) in Python. The conversion follows these steps:
1.Parse the regular expression (regex) 
2.Convert to Non-deterministic Finite Automaton (NFA) using Thompson's Construction 
3.Transform NFA to DFA using Subset Construction

##Features
1.Supports basic regex operations:

-Concatenation (ab)

-Alternation (a|b)

-Kleene star (a*)

-Parentheses for grouping ((ab)*)

-Escape sequences (\* for literal '*')

2.Detailed error reporting for invalid regex patterns

3.Clear visualization of the resulting DFA

##Installation
No external dependencies required. Just ensure you have Python 3.6+ installed.
 ```bash
git clone https://github.com/yourusername/regex-to-dfa.git
