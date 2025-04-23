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

---

## Part 2: Parsing

Grammar Parsing algo(Recursive descent parse, LL(1) parse, LR(0)/SLR(1) parse)

### START
```
START -> EX_DECLA | EX_DECLA START

EX_DECLA -> FUNC_DEF | DECLA

FUNC_DEF -> TYPE id(PARAM_LIST){BLOCK_ST} | TYPE main(){BLOCK_ST}

TYPE -> double | int | str
```

### PARAM_LIST
```
PARAM_LIST -> ɛ | PARAM | PARAM, PARAM_LIST

PARAM -> TYPE id
```

### BLOCK_ST
```
BLOCK_ST -> STATM | STATM BLOCK_ST

STATM -> DECLA | ASS_ST | IF_ST | FOR_ST | WHILE_ST | RETURN_ST

RETURN_ST -> return EP;
```

### DECLA
```
DECLA -> TYPE VAR_LIST;

VAR_LIST -> VAR | VAR_LIST , VAR

VAR -> id [intc] | id INITIAL

INTITIAL -> = EP | ɛ
```

### ASS_ST
```
ASS_ST -> id = EP;
```

### IF_ST
```
IF_ST -> if (LOGC_EP){BLOCK_ST} ELSE_ST

ELSE_ST -> ɛ | else {BLOCK_ST}
```

### FOR_ST
```
FOR_ST -> for (ASS_ST LOGC_EP; ASS_ST){BLOCK_ST}
```

### WHILE_ST
```
WHILE_ST -> while(LOGC_EP){BLOCK_ST}
```

### EP
```
EP -> LOGC_EP | MATH_EP | str

MATH_EP -> TD op1 MATH_EP | TD

TD ->  TERM | TERM op2 TD

TERM -> id | intc | real | ( MATH_EP )

```
> op1 = { + | - }

> op2 = { * | / }

### LOGC_EP
```
LOGC_EP -> LOGC_EP op3 LOGC_ST | ! LOGC_EP | LOGC_ST

LOGC_ST -> (LOGC_EP) | MATH_EP op4 MATH_EP | LOGC_TERM op4a LOC_TERM

LOGC_TERM -> id | str
```
> op3 = { && | || }

> op4 = { < | <= | > | >= | == | != }

> op4a = { == | != }