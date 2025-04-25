# CSCI3120 Project

> Author: Winnie YU 

This project is to construct compiler in any programming language without using any compiler-related libraries.

---

| Part | Version | Info |
|  ----  | ----  | ---- |
| [Part 1: Lexical Analysis](##Part1:LexicalAnalysis) | 1.1 | fulfilling basic token identification, not yet handling real number and signed number(TODO) |
| Part 2: Parsing | 1.0 | can solve it more elegantly with checking everytime whether next token exists or not |
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

TYPE -> double | int | char
```

### DECLA
```
DECLA -> TYPE VAR_LIST;

VAR_LIST -> VAR VAR_LIST'

VAR_LIST' -> , VAR VAR_LIST' | ɛ 

VAR -> id [intc] | id INITIAL

INTITIAL -> = EP | ɛ
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
FOR_ST -> for (ASS_ST LOGC_EP; AFASS_ST){BLOCK_ST}

AFASS_ST -> id = EP
```

### WHILE_ST
```
WHILE_ST -> while(LOGC_EP){BLOCK_ST}
```

### EP
```
EP -> LOGC_EP | MATH_EP | str

MATH_EP -> TD | TD op1 MATH_EP

TD ->  TERM | TERM op2 TD

TERM -> id | intc | real | ( MATH_EP ) 

```
> op1 = { + | - }

> op2 = { * | / }

### LOGC_EP
```
LOGC_EP -> LOGC_ST | LOGC_ST op3 LOGC_ST | ! LOGC_EP

LOGC_ST -> (LOGC_EP) | LOGC_TERM op4 LOGC_TERM 

LOGC_TERM -> TERM | str
```
> op3 = { && | || }

> op4 = { < | <= | > | >= | == | != }

### Accepting Case

#### Case 1:

input:
```
int x = 10, y = 20;
double z ;
char s1 [10] = "hello";

```
tested Grammar: (DECLA)[###DECLA]

### Case 2:

input:
```
int main () {
    int a = 5;
    return a ;
}
```
tested Grammar: (FUNC_DEF)[###START], (BLOCK_ST)[###BLOCK_ST]

### Case 3:

input:
```
int x = 5 + 10 * 3;
int y = (x - 2) / 4;
double addsum ( double var1 , double var 2 ){
   return ( var1 + var2 );
}
```
tested Grammar: (EP)[###EP], (PARAM_LIST)[###PARAM_LIST], (BLOCK_ST)[###BLOCK_ST]

### Case 4:

input:
```
int main () {
    for (x = 0; x < 10; x = x + 1) {
    sum = x + z ;
    }
}
```
tested Grammar: (ASS_ST)[###ASS_ST],(LOGC_EP)[###LOGC_EP],(FOR_ST)[###FOR_ST]

### Case 5:

input:
```
int main () {
    while ( a == b ){
        a = a + 1;
    }
}
```
tested Grammar: (ASS_ST)[###ASS_ST],(LOGC_EP)[###LOGC_EP],(WHILE_ST)[###WHILE_ST]

### Case 6:

input:
```
int func ( int a , int b ) {
    if ( 1 == 2 ){
        return 1 ;
    }
    else {
        return 0 ;
    }

    if ( a > b ){
        b = a ;
    }
}
```
tested Grammar: (IF_ST)[###IF_ST] , (START)[###START]

### Rejected Grammar

### Case 1:

> missing ";" after ass_st

input:

```
int a = 5
```

output log:
```
TOKEN: int, current: 1
ID: a, current: 2
TOKEN: =, current: 3
INTC: 5, current: 4
Passed: intc
Passed: TERM
Passed: TD
INTC: 5, current: 4
Passed: intc
Passed: TERM(logc_term)
Failed to parse OP4: no OP4 found at 4 position
Failed to parse LOGC_ST: no LOGC_TERM found after op4 at 4 position
INTC: 5, current: 4
Passed: intc
Passed: TERM(logc_term)
Failed to parse OP4: no OP4 found at 4 position
Failed to parse LOGC_ST: no LOGC_TERM found after op4 at 4 position
Failed to parse LOGC_EP at 3 position
Failed to parse EP at 3 position
Failed to parse VAR: no EP found after '=' at 3 position
Failed to parse VAR_LIST: no VAR found at 3 position
TOKEN: int, current: 1
Failed to parse EX_DECLA: no valid token found at 1 position
Failed to parse START: no EX_DECLA found at 1 position
Parsing failed, Rejected.

```
### Case 2:

> expected no param for main function

input: 
```
int main (int x , ) {
    return x ;
}
```

output log: 
```
TOKEN: int, current: 1
Failed to parse VAR: no id found at 1 position
Failed to parse VAR_LIST: no VAR found at 1 position
TOKEN: int, current: 1
TOKEN: main, current: 2
TOKEN: (, current: 3
Failed to parse EX_DECLA: no valid token found at 3 position
Failed to parse START: no EX_DECLA found at 3 position
Parsing failed, Rejected.
```

### Case 3:

> missing param in param list

input:
```
int newfunc (int x , ) {
    return x ;
}
```
ouput log:
```
TOKEN: int, current: 1
ID: newfunc, current: 2
Failed to parse [: no valid token found at 2 position
Failed to parse =: no valid token found at 2 position
Passed: ɛ
Passed: id INITIAL
Passed: VAR
Failed to parse ,: no valid token found at 2 position
Passed: VAR_LIST
Failed to parse ;: no valid token found at 2 position
TOKEN: int, current: 1
Passed: TYPE
debug func_def: newfunc
ID: newfunc, current: 2
TOKEN: (, current: 3
TOKEN: int, current: 4
Passed: TYPE, Shift: TYPE
ID: x, current: 5
Passed: TYPE id, Shift: id
Passed: PARAM
TOKEN: ,, current: 6
Failed to parse TYPE: no valid token found at 6 position
Failed to parse PARAM_LIST: no PARAM found after ',' at 6 position
Failed to parse FUNC_DEF: no valid token found at 6 position
Failed to parse EX_DECLA: no valid token found at 6 position
Failed to parse START: no EX_DECLA found at 6 position
Parsing failed, Rejected.
```

### Case 4:

> Incomplete math expression

input:
```
int a = 5 + ;
```

output log:
```
TOKEN: int, current: 1
ID: a, current: 2
Failed to parse [: no valid token found at 2 position
TOKEN: =, current: 3
Failed to parse str: no valid token found at 3 position
Failed to parse id: no valid token found at 3 position
INTC: 5, current: 4
Passed: intc
Passed: TERM
Failed to parse *: no valid token found at 4 position
Failed to parse /: no valid token found at 4 position
Passed: TD
TOKEN: +, current: 5
Passed: +
Failed to parse id: no valid token found at 5 position
Failed to parse intc: no valid token found at 5 position
Failed to parse real: no valid token found at 5 position
Failed to parse (: no valid token found at 5 position
Failed to parse TD at 5 position
Failed to parse MATH_EP at 5 position
Failed to parse (: no valid token found at 3 position
Failed to parse id: no valid token found at 3 position
INTC: 5, current: 4
Passed: intc
Passed: TERM(logc_term)
Failed to parse OP4: no OP4 found at 4 position
Failed to parse LOGC_ST: no LOGC_TERM found after op4 at 4 position
Failed to parse !: no valid token found at 3 position
Failed to parse (: no valid token found at 3 position
Failed to parse id: no valid token found at 3 position
INTC: 5, current: 4
Passed: intc
Passed: TERM(logc_term)
Failed to parse OP4: no OP4 found at 4 position
Failed to parse LOGC_ST: no LOGC_TERM found after op4 at 4 position
Failed to parse LOGC_EP at 3 position
Failed to parse EP at 3 position
Failed to parse VAR: no EP found after '=' at 3 position
Failed to parse VAR_LIST: no VAR found at 3 position
TOKEN: int, current: 1
Passed: TYPE
debug func_def: a
ID: a, current: 2
Failed to parse (: no valid token found at 2 position
Failed to parse FUNC_DEF: no valid token found at 2 position
Failed to parse EX_DECLA: no valid token found at 2 position
Failed to parse START: no EX_DECLA found at 2 position
Parsing failed, Rejected.
```

### Case 5:

> Missing semicolon in for loop

input:
```
int main () {
    for (x = 0; x < 10 x = x + 1) {
    sum = x + z ;
    }
}
```

output log:
```
TOKEN: int, current: 1
Failed to parse id: no valid token found at 1 position
Failed to parse VAR: no id found at 1 position
Failed to parse VAR_LIST: no VAR found at 1 position
TOKEN: int, current: 1
Passed: TYPE
debug func_def: main
TOKEN: main, current: 2
TOKEN: (, current: 3
TOKEN: ), current: 4
TOKEN: {, current: 5
TOKEN: for, current: 6
TOKEN: (, current: 7
ID: x, current: 8
TOKEN: =, current: 9
Failed to parse str: no valid token found at 9 position
Failed to parse id: no valid token found at 9 position
INTC: 0, current: 10
Passed: intc
Passed: TERM
Failed to parse *: no valid token found at 10 position
Failed to parse /: no valid token found at 10 position
Passed: TD
Passed: MATH_EP
TOKEN: ;, current: 11
Passed: id = EP;
Failed to parse (: no valid token found at 11 position
ID: x, current: 12
Passed: id
Passed: TERM(logc_term)
Passed: <
TOKEN: <, current: 13
Failed to parse id: no valid token found at 13 position
INTC: 10, current: 14
Passed: intc
Passed: TERM(logc_term)
Passed: LOGC_TERM op4 LOGC_TERM
Failed to parse &&: no valid token found at 14 position
Failed to parse ||: no valid token found at 14 position
Failed to parse !: no valid token found at 11 position
Failed to parse (: no valid token found at 11 position
ID: x, current: 12
Passed: id
Passed: TERM(logc_term)
Passed: <
TOKEN: <, current: 13
Failed to parse id: no valid token found at 13 position
INTC: 10, current: 14
Passed: intc
Passed: TERM(logc_term)
Passed: LOGC_TERM op4 LOGC_TERM
Passed: LOGC_ST
Failed to parse LOGC_EP: no after set ',' or ')' or ';' found after LOGC_ST at 14 position     
Failed to parse FOR_ST at 14 position
Failed to parse BLOCK_ST: no STATM found at 14 position
Failed to parse FUNC_DEF: no valid token found at 14 position
Failed to parse EX_DECLA: no valid token found at 14 position
Failed to parse START: no EX_DECLA found at 14 position
Parsing failed, Rejected.
```