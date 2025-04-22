class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def advance(self):
        if self.current < len(self.tokens):
            self.current += 1
        return self.previous()

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    # bool Match(TOKEN tok)
    def match(self, tok):
        token = self.peek()
        if not token:
            return False
        if tok == "id" and token[1] == 0:
            self.current += 1
            print(f"ID: {token[0]}, current: {self.current}")
            return True
        if tok == "int" and token[1] == 1:
            self.current += 1
            print(f"INT: {token[0]}, current: {self.current}")
            return True
        if tok == "double" and token[1] == 1:
            self.current += 1
            print(f"DOUBLE: {token[0]}, current: {self.current}")
            return True
        if tok == "intc" and token[1] == 1:
            self.current += 1
            print(f"INTC: {token[0]}, current: {self.current}")
            return True
        if tok == "str" and token[1] == 2:
            self.current += 1
            print(f"STRING: {token[0]}, current: {self.current}")
            return True
        if token[0] == tok:
            self.current += 1
            print(f"TOKEN: {token[0]}, current: {self.current}")
            return True
        return False

    # non-terminals
    # bool START()
    # START -> EX_DECLA | START EX_DECLA
    def start(self):
        tmp = self.current
        if self.ex_decla():
            print("Passed: EX_DECLA")
            return True
        self.current = tmp # reset
        if self.start() and self.ex_decla():
            print("Passed: START EX_DECLA")
            return True
        self.current = tmp # reset
        return False
        
    # bool EX_DECLA()
    # EX_DECLA -> FUNC_DEF | DECLA
    def ex_decla(self):
        tmp = self.current
        if self.func_def():
            print("Passed: FUNC_DEF")
            return True
        self.current = tmp # reset
        if self.decla():
            print("Passed: DECLA")
            return True
        self.current = tmp # reset
        return False

    # bool FUNC_DEF()
    # FUNC_DEF -> TYPE id(PARAM_LIST){BLOCK_ST}
    def func_def(self):
        tmp = self.current
        if self.type() and self.match("id") and self.match("(") and self.param_list() and self.match("{") and self.block_st() and self.match("}"):
            print("Passed: TYPE id(PARAM_LIST){BLOCK_ST}")
            return True
        self.current = tmp # reset
        if self.type() and self.match("main") and self.match("(") and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
            print("Passed: TYPE main(){BLOCK_ST}")
            return True
        self.current = tmp # reset
        return False

    # bool TYPE()
    # TYPE -> double | int | str
    def type(self):
        tmp = self.current
        if self.match("double"):
            print("Passed: double")
            return True
        self.current = tmp # reset
        if self.match("int"):
            print("Passed: int")
            return True
        self.current = tmp # reset
        if self.match("str"):
            print("Passed: str")
            return True
        self.current = tmp # reset
        return False
        
    # bool DECLA()
    # DECLA -> TYPE VAR_LIST;
    def decla(self):
        tmp = self.current
        if self.type() and self.var_list() and self.match(";"):
            print("Passed: TYPE VAR_LIST;")
            return True
        self.current = tmp # reset
        return False

    # bool VAR_LIST() 
    # VAR_LIST -> VAR VAR_LIST' # LL(1) // not sure 
    # VAR_LIST' -> , VAR VAR_LIST' | ɛ # LL(1)
    def var_list(self):
        if self.var():
            print("Passed: VAR")
            while self.match(","):
                if self.var():
                    print("Passed: , VAR")
                else:
                    print(f"Failed to parse VAR_LIST: no VAR found after ',' at {self.current} position, current token: {self.peek()}")
                    return False
            print("Passed: VAR_LIST")
            return True        
        print(f"Failed to parse VAR_LIST: no VAR found at {self.current} position, current token: {self.peek()}")
        return False

    # bool VAR() 
    # VAR -> id INITIAL | id [intc] # LL(2)
    # INTITIAL -> = EP | ɛ # LL(1)
    def var(self):
        if self.match("id"):
            tmp = self.current
            if self.match("["):
                if self.match("intc"):
                    if self.match("]"):
                        print("Passed: id [intc]")
                        return True
                    print(f"Failed to parse VAR: no ']' found after intc at {self.current} position, current token: {self.peek()}")
                    return False
                print(f"Failed to parse VAR: no intc found after '[' at {self.current} position, current token: {self.peek()}")
                return False
            self.current = tmp
            if self.match("="):
                if self.ep():
                    print("Passed: = EP")
                    return True
                print(f"Failed to parse VAR: no EP found after '=' at {self.current} position, current token: {self.peek()}")
                return False
            self.current = tmp
            print("Passed: ɛ")
            print("Passed: id INITIAL")
            return True
        print(f"Failed to parse VAR: no id found at {self.current} position, current token: {self.peek()}")
        return False

    # bool PARAM_LIST()
    # PARAM_LIST -> ɛ | PARAM | PARAM_LIST , PARAM
    def param_list(self):
        tmp = self.current
        if self.param():
            print("Passed: PARAM")
            return True
        self.current = tmp # reset
        if self.param_list() and self.match(",") and self.param():
            print("Passed: PARAM_LIST , PARAM")
            return True
        self.current = tmp # reset
        return False
    
    # bool PARAM()
    # PARAM -> TYPE id
    def param(self):
        tmp = self.current
        if self.type() and self.match("id"):
            print("Passed: TYPE id")
            return True
        self.current = tmp # reset
        return False

    # bool BLOCK_ST()
    # BLOCK_ST -> STATM | BLOCK_ST STATM
    def block_st(self):
        tmp = self.current
        if self.statm():
            print("Passed: STATM")
            return True
        self.current = tmp # reset
        if self.block_st() and self.statm():
            print("Passed: BLOCK_ST STATM")
            return True
        self.current = tmp # reset
        return False

    # bool STATM()
    # STATM -> DECLA | ASS_ST | IF_ST | FOR_ST | WHILE_ST | RETURN_ST
    def statm(self):
        tmp = self.current
        if self.decla():
            print("Passed: DECLA")
            return True
        self.current = tmp # reset
        if self.ass_st():
            print("Passed: ASS_ST")
            return True
        self.current = tmp # reset
        if self.if_st():
            print("Passed: IF_ST")
            return True
        self.current = tmp # reset
        if self.for_st():
            print("Passed: FOR_ST")
            return True
        self.current = tmp # reset
        if self.while_st():
            print("Passed: WHILE_ST")
            return True
        self.current = tmp # reset
        if self.return_st():
            print("Passed: RETURN_ST")
            return True
        self.current = tmp # reset
        return False

    # bool RETURN_ST()
    # RETURN_ST -> return EP;
    def return_st(self):
        tmp = self.current
        if self.match("return") and self.ep() and self.match(";"):
            print("Passed: return EP;")
            return True
        self.current = tmp # reset
        return False

    # bool ASS_ST()
    # ASS_ST -> id = EP;
    def ass_st(self):
        tmp = self.current
        if self.match("id") and self.match("=") and self.ep() and self.match(";"):
            print("Passed: id = EP;")
            return True
        self.current = tmp # reset
        return False

    # bool IF_ST()
    # IF_ST -> if (LOGC_EP){BLOCK_ST} ELSE_ST
    def if_st(self):
        tmp = self.current
        if self.match("if") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st() and self.match("}") and self.else_st():
            print("Passed: if (LOGC_EP){BLOCK_ST} ELSE_ST")
            return True
        self.current = tmp # reset
        return False

    # bool ELSE_ST()
    # ELSE_ST -> ɛ | else {BLOCK_ST}
    def else_st(self):
        tmp = self.current
        if self.match("else") and self.match("{") and self.block_st() and self.match("}"):
            print("Passed: else {BLOCK_ST}")
            return True
        self.current = tmp # reset
        print("Passed: ɛ(else)")
        return True

    # bool FOR_ST()
    # FOR_ST -> for (ASS_ST LOGC_EP; ASS_ST){BLOCK_ST}
    def for_st(self):
        tmp = self.current
        if self.match("for") and self.match("(") and self.ass_st() and self.logc_ep() and self.match(";") and self.ass_st() and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
            print("Passed: for (ASS_ST LOGC_EP; ASS_ST){BLOCK_ST}")
            return True
        self.current = tmp # reset
        return False

    # bool WHILE_ST()
    # WHILE_ST -> while(LOGC_EP){BLOCK_ST}
    def while_st(self):
        tmp = self.current
        if self.match("while") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
            print("Passed: while(LOGC_EP){BLOCK_ST}")
            return True
        self.current = tmp # reset
        return False

    # bool EP()
    # EP -> LOGC_EP | MATH_EP | str
    def ep(self):
        tmp = self.current
        if self.logc_ep():
            print("Passed: LOGC_EP")
            return True
        self.current = tmp # reset
        if self.math_ep():
            print("Passed: MATH_EP")
            return True
        self.current = tmp # reset
        if self.match("str"):
            print("Passed: str")
            return True
        self.current = tmp # reset
        return False

    # bool MATH_EP()
    # MATH_EP -> TD | MATH_EP op1 TD 
    def math_ep(self):
        tmp = self.current
        if self.td():
            print("Passed: TD")
            return True
        self.current = tmp # reset
        if self.math_ep() and self.op1() and self.td():
            print("Passed: MATH_EP op1 TD")
            return True
        self.current = tmp # reset
        return False

    # bool TD()
    # TD ->  TERM | TD op2 TERM
    def td(self):
        tmp = self.current
        if self.term():
            print("Passed: TERM")
            return True
        self.current = tmp # reset
        if self.td() and self.op2() and self.term():
            print("Passed: TD op2 TERM")
            return True
        self.current = tmp # reset
        return False

    # bool TERM()
    # TERM -> id | intc | real | ( MATH_EP )
    def term(self):
        tmp = self.current
        if self.match("id"):
            print("Passed: id")
            return True
        self.current = tmp # reset
        if self.match("intc"):
            print("Passed: intc")
            return True
        self.current = tmp # reset
        if self.match("real"):
            print("Passed: real")
            return True
        self.current = tmp # reset
        if self.match("(") and self.math_ep() and self.match(")"):
            print("Passed: ( MATH_EP )")
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_EP()
    # LOGC_EP -> LOGC_ST op3 LOGC_ST | ! LOGC_EP | LOGC_ST
    def logc_ep(self):
        tmp = self.current
        if self.logc_st() and self.op3() and self.logc_st():
            print("Passed: LOGC_ST op3 LOGC_ST")
            return True
        self.current = tmp # reset
        if self.match("!") and self.logc_ep():
            print("Passed: ! LOGC_EP")
            return True
        self.current = tmp # reset
        if self.logc_st():
            print("Passed: LOGC_ST")
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_ST()
    # LOGC_ST -> (LOGC_EP) | MATH_EP op4 MATH_EP | LOGC_TERM op4a LOC_TERM
    def logc_st(self):
        tmp = self.current
        if self.match("(") and self.logc_ep() and self.match(")"): # parenthesis for case of inner comparison
            print("Passed: (LOGC_EP)")
            return True
        self.current = tmp # reset
        if self.math_ep() and self.op4() and self.math_ep(): # math comparison
            print("Passed: MATH_EP op4 MATH_EP")
            return True
        self.current = tmp # reset
        if self.logc_term() and self.op4a() and self.logc_term(): # string comparison
            print("Passed: LOGC_TERM op4a LOGC_TERM")
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_TERM()
    # LOGC_TERM -> id | str
    def logc_term(self):
        tmp = self.current
        if self.match("id"):
            print("Passed: id(logc_term)")
            return True
        self.current = tmp # reset
        if self.match("str"):
            print("Passed: str(logc_term)")
            return True
        self.current = tmp # reset
        return False

    # terminals
    # bool OP1()
    # op1 = { + | - }
    def op1(self):
        tmp = self.current
        if self.match("+"):
            print("Passed: +")
            return True
        self.current = tmp # reset
        if self.match("-"):
            print("Passed: -")
            return True
        self.current = tmp # reset
        return False
        
    # bool OP2()
    # op2 = { * | / }
    def op2(self):
        tmp = self.current
        if self.match("*"):
            print("Passed: *")
            return True
        self.current = tmp # reset
        if self.match("/"):
            print("Passed: /")
            return True
        self.current = tmp # reset
        return False

    # bool OP3()
    # op3 = { && | || }
    def op3(self):
        tmp = self.current
        if self.match("&&"):
            print("Passed: &&")
            return True
        self.current = tmp # reset
        if self.match("||"):
            print("Passed: ||")
            return True
        self.current = tmp # reset
        return False

    # bool OP4()
    # op4 = { < | <= | > | >= | == | != }
    def op4(self):
        tmp = self.current
        if self.match("<"):
            print("Passed: <")
            return True
        self.current = tmp # reset
        if self.match("<="):
            print("Passed: <=")
            return True
        self.current = tmp # reset
        if self.match(">"):
            print("Passed: >")
            return True
        self.current = tmp # reset
        if self.match(">="):
            print("Passed: >=")
            return True
        self.current = tmp # reset
        if self.match("=="):
            print("Passed: ==")
            return True
        self.current = tmp # reset
        if self.match("!="):
            print("Passed: !=")
            return True
        self.current = tmp # reset
        return False

    # bool OP4A()
    # op4a = { == | != }
    def op4a(self):
        tmp = self.current
        if self.match("=="):
            print("Passed: ==")
            return True
        self.current = tmp # reset
        if self.match("!="):
            print("Passed: !=")
            return True
        self.current = tmp # reset
        return False

def transform_file(input_filename):
    try:
        with open(input_file, "r") as file:
            content = file.read()

        # Transform the token format: replace '<' with '(' and '>' with ')'
        content = content.replace("<", "(").replace(">", ")")

        # Extract token tuples using eval
        tokens = eval(f"[{content}]")  # Safely convert to a list of tuples
        return tokens
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return []
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # input_file = "test.txt"  # Replace with your actual input file name
    # tokens = transform_file(input_file)
    # parser = Parser(tokens)  # Pass the token list to the Parser
    # start_parsing = parser.start()
    # if start_parsing == True:
    #     print("Parsing successful, Accepted.")
    # else:
    #     print("Parsing failed, Rejected.")
    parser = Parser([( "test1" ,0) , ("[", 56), ("test2",0)])
    parser2 = Parser ([])
    start_parsing = parser.var()
    if start_parsing == True:
        print("Parsing successful, Accepted.")
    else:
        print("Parsing failed, Rejected.")