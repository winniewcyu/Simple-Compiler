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
double z;
char s1[10] = "hello";

```
tested Grammar: (DECLA)[###DECLA]

### Case 2:

input:
```
int main() {
    int a = 5;
    return a;
}
```
tested Grammar: (FUNC_DEF)[###START], (BLOCK_ST)[###BLOCK_ST]

### Case 3:

input:
```
int x = 5 + 10 * 3;
int y = (x - 2) / 4;
```
tested Grammar: (EP)[###EP]

### Case 4:

input:
```
int main() {
    for (x = 0; x < 10; x = x + 1) {
    sum = x + z;
    }
}
```
tested Grammar: (ASS_ST)[###ASS_ST],(LOGC_EP)[###LOGC_EP],(FOR_ST)[###FOR_ST]

### Case 5:

input:
```
int main() {
    while ( a == b ){
        a = a + 1;
    }
}
```
tested Grammar: (ASS_ST)[###ASS_ST],(LOGC_EP)[###LOGC_EP],(WHILE_ST)[###WHILE_ST]

### Case 6:

input:
```
int main() {
    if ( 1 == 2 ){
        return 1 ;
    }
    else{
        return 0 ;
    }

    if ( a > b ){
        b = a;
    }
}
```
tested Grammar: (IF_ST)[###IF_ST]