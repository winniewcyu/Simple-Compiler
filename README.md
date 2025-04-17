# CSCI3120 Project

> Author: Winnie YU 

This project is to construct compiler in any programming language without using any compiler-related libraries.

---

| Part | Version | Info |
|  ----  | ----  | ---- |
| [Part 1: Lexical Analysis](##Part1:LexicalAnalysis) | 1.0 | fulfilling basic token identification, not yet handling real number and signed number(TODO), not yet include all possible keywords/operators/punctuation(doubt if possible)|
| Part 2: Parsing | - | - |
| Part 3: Semantic Analysis | - | - |

---

## Part 1: Lexical Analysis

_Task:_ Break down an input source file into tokens and write the processed tokens to a file in the format  `<"token string", token type number>, ...`

> _Identified Tokens Types (6):_ keywords, identifiers, operators, punctuation, integers, strings
