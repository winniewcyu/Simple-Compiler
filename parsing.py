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
        if self.peek() and self.peek() == tok:
            self.current += 1 
            return True
        return False

    # non-terminals
    # bool START()
    # START -> EX_DECLA | START EX_DECLA
    def start(self):
        tmp = self.current
        if self.ex_decla():
            return True
        self.current = tmp # reset
        if self.start() and self.ex_decla():
            return True
        self.current = tmp # reset
        return False
        
    # bool EX_DECLA()
    # EX_DECLA -> FUNC_DEF | DECLA
    def ex_decla(self):
        tmp = self.current
        if self.func_def():
            return True
        self.current = tmp # reset
        if self.decla():
            return True
        self.current = tmp # reset
        return False

    # bool FUNC_DEF()
    # FUNC_DEF -> TYPE id(PARAM_LIST){BLOCK_ST}
    def func_def(self):
        tmp = self.current
        if self.type() and self.match("id") and self.match("(") and self.param_list() and self.match("{") and self.block_st():
            return True
        self.current = tmp # reset
        return False

    # bool TYPE()
    # TYPE -> double | int | char
    def type(self):
        tmp = self.current
        if self.match("double"):
            return True
        self.current = tmp # reset
        if self.match("int"):
            return True
        self.current = tmp # reset
        if self.match("char"):
            return True
        self.current = tmp # reset
        return False
        
    # bool DECLA()
    # DECLA -> TYPE VAR_LIST;
    def decla(self):
        tmp = self.current
        if self.type() and self.var_list() and self.match(";"):
            return True
        self.current = tmp # reset
        return False

    # bool VAR_LIST()
    # VAR_LIST -> VAR | VAR_LIST , VAR
    def var_list(self):
        tmp = self.current
        if self.var():
            return True
        self.current = tmp # reset
        if self.var_list() and self.match(",") and self.var():
            return True
        self.current = tmp # reset
        return False

    # bool VAR()
    # VAR -> id INITIAL | id [intc]
    def var(self):
        tmp = self.current
        if self.match("id") and self.initial():
            return True
        self.current = tmp # reset
        if self.match("id") and self.match("[") and self.match("intc") and self.match("]"):
            return True
        self.current = tmp # reset
        return False

    # bool INITIAL()
    # INTITIAL -> = EP | ɛ
    def initial(self):
        tmp = self.current
        if self.match("=") and self.ep():
            return True
        self.current = tmp # reset
        return True
    
    # bool PARAM_LIST()
    # PARAM_LIST -> ɛ | PARAM | PARAM_LIST , PARAM
    def param_list(self):
        tmp = self.current
        if self.param():
            return True
        self.current = tmp # reset
        if self.param_list() and self.match(",") and self.param():
            return True
        self.current = tmp # reset
        return False
    
    # bool PARAM()
    # PARAM -> TYPE id
    def param(self):
        tmp = self.current
        if self.type() and self.match("id"):
            return True
        self.current = tmp # reset
        return False

    # bool BLOCK_ST()
    # BLOCK_ST -> STATM | BLOCK_ST STATM
    def block_st(self):
        tmp = self.current
        if self.statm():
            return True
        self.current = tmp # reset
        if self.block_st() and self.statm():
            return True
        self.current = tmp # reset
        return False

    # bool STATM()
    # STATM -> DECLA | ASS_ST | IF_ST | FOR_ST | WHILE_ST | RETURN_ST
    def statm(self):
        tmp = self.current
        if self.decla():
            return True
        self.current = tmp # reset
        if self.ass_st():
            return True
        self.current = tmp # reset
        if self.if_st():
            return True
        self.current = tmp # reset
        if self.for_st():
            return True
        self.current = tmp # reset
        if self.while_st():
            return True
        self.current = tmp # reset
        if self.return_st():
            return True
        self.current = tmp # reset
        return False

    # bool RETURN_ST()
    # RETURN_ST -> return EP;
    def return_st(self):
        tmp = self.current
        if self.match("return") and self.ep() and self.match(";"):
            return True
        self.current = tmp # reset
        return False

    # bool ASS_ST()
    # ASS_ST -> id = EP;
    def ass_st(self):
        tmp = self.current
        if self.match("id") and self.match("=") and self.ep() and self.match(";"):
            return True
        self.current = tmp # reset
        return False

    # bool IF_ST()
    # IF_ST -> if (LOGC_EP){BLOCK_ST} ELSE_ST
    def if_st(self):
        tmp = self.current
        if self.match("if") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st() and self.match("}") and self.else_st():
            return True
        self.current = tmp # reset
        return False

    # bool ELSE_ST()
    # ELSE_ST -> ɛ | else {BLOCK_ST}
    def else_st(self):
        tmp = self.current
        if self.match("else") and self.match("{") and self.block_st() and self.match("}"):
            return True
        self.current = tmp # reset
        return True

    # bool FOR_ST()
    # FOR_ST -> for (ASS_ST LOGC_EP; ASS_ST){BLOCK_ST}
    def for_st(self):
        tmp = self.current
        if self.match("for") and self.match("(") and self.ass_st() and self.logc_ep() and self.match(";") and self.ass_st() and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
            return True
        self.current = tmp # reset
        return False

    # bool WHILE_ST()
    # WHILE_ST -> while(LOGC_EP){BLOCK_ST}
    def while_st(self):
        tmp = self.current
        if self.match("while") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_EP()
    # EP -> LOGC_EP | MATH_EP | str
    def logc_ep(self):
        tmp = self.current
        if self.logc_ep():
            return True
        self.current = tmp # reset
        if self.math_ep():
            return True
        self.current = tmp # reset
        if self.match("str"):
            return True
        self.current = tmp # reset
        return False

    # bool MATH_EP()
    # MATH_EP -> MATH_EP op1 TD | TD
    def math_ep(self):
        tmp = self.current
        if self.math_ep() and self.op1() and self.td():
            return True
        self.current = tmp # reset
        if self.td():
            return True
        self.current = tmp # reset
        return False

    # bool TD()
    # TD -> TD op2 TERM | TERM
    def td(self):
        tmp = self.current
        if self.td() and self.op2() and self.term():
            return True
        self.current = tmp # reset
        if self.term():
            return True
        self.current = tmp # reset
        return False

    # bool TERM()
    # TERM -> ( MATH_EP ) | id | intc | real
    def term(self):
        tmp = self.current
        if self.match("(") and self.math_ep() and self.match(")"):
            return True
        self.current = tmp # reset
        if self.match("id"):
            return True
        self.current = tmp # reset
        if self.match("intc"):
            return True
        self.current = tmp # reset
        if self.match("real"):
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_EP()
    # LOGC_EP -> LOGC_EP op3 LOGC_ST | ! LOGC_EP | LOGC_ST
    def logc_ep(self):
        tmp = self.current
        if self.logc_ep() and self.op3() and self.logc_st():
            return True
        self.current = tmp # reset
        if self.match("!") and self.logc_ep():
            return True
        self.current = tmp # reset
        if self.logc_st():
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_ST()
    # LOGC_ST -> (LOGC_EP) | MATH_EP op4 MATH_EP | LOGC_TERM op4a LOC_TERM
    def logc_st(self):
        tmp = self.current
        if self.match("(") and self.logc_ep() and self.match(")"): # parenthesis for case of inner comparison
            return True
        self.current = tmp # reset
        if self.math_ep() and self.op4() and self.math_ep(): # math comparison
            return True
        self.current = tmp # reset
        if self.logc_term() and self.op4a() and self.logc_term(): # string comparison
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_TERM()
    # LOGC_TERM -> id | str
    def logc_term(self):
        tmp = self.current
        if self.match("id"):
            return True
        self.current = tmp # reset
        if self.match("str"):
            return True
        self.current = tmp # reset
        return False

    # terminals
    # bool OP1()
    # op1 = { + | - }
    def op1(self):
        tmp = self.current
        if self.match("+"):
            return True
        self.current = tmp # reset
        if self.match("-"):
            return True
        self.current = tmp # reset
        return False
        
    # bool OP2()
    # op2 = { * | / }
    def op2(self):
        tmp = self.current
        if self.match("*"):
            return True
        self.current = tmp # reset
        if self.match("/"):
            return True
        self.current = tmp # reset
        return False

    # bool OP3()
    # op3 = { && | || }
    def op3(self):
        tmp = self.current
        if self.match("&&"):
            return True
        self.current = tmp # reset
        if self.match("||"):
            return True
        self.current = tmp # reset
        return False

    # bool OP4()
    # op4 = { < | <= | > | >= | == | != }
    def op4(self):
        tmp = self.current
        if self.match("<"):
            return True
        self.current = tmp # reset
        if self.match("<="):
            return True
        self.current = tmp # reset
        if self.match(">"):
            return True
        self.current = tmp # reset
        if self.match(">="):
            return True
        self.current = tmp # reset
        if self.match("=="):
            return True
        self.current = tmp # reset
        if self.match("!="):
            return True
        self.current = tmp # reset
        return False

    # bool OP4A()
    # op4a = { == | != }
    def op4a(self):
        tmp = self.current
        if self.match("=="):
            return True
        self.current = tmp # reset
        if self.match("!="):
            return True
        self.current = tmp # reset
        return False
    