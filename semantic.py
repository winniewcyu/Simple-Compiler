import re # regex
from symbol_table import SymbolTable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.sem_stack = []
        self.temp_count = 0
        self.label_count = 0

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def write_quad_to_file(self, operation, operand1, operand2, result):
        with open("quad.txt", "a") as f:
            if operand1 == None:
                operand1 = " "
            if operand2 == None:
                operand2 = " "
            print(f"({operation}, {operand1}, {operand2}, {result})")
            f.write(f"({operation}, {operand1}, {operand2}, {result})\n")
    
    def write_label_to_file(self, label):
        with open("quad.txt", "a") as f:
            print(f"{label}:")
            f.write(f"{label}:\n")
    
    def push(self, tok):
        self.sem_stack.append(tok)
        
    def geq_plus(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("+", parm1, parm2, result)
        self.push(result)
    
    def geq_minus(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("-", parm1, parm2, result)
        self.push(result)
        
    def geq_mul(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("*", parm1, parm2, result)
        self.push(result)
        
    def geq_div(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("/", parm1, parm2, result)
        self.push(result)
        
    def geq_equal(self):
        param = self.sem_stack.pop()
        result = self.sem_stack.pop()
        self.write_quad_to_file("=", param, None, result)
        
    def geq_equal_equal(self):
        param2 = self.sem_stack.pop()
        param1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("==", param1, param2, result)
        self.push(result)
        
    def geq_not_equal(self):
        param2 = self.sem_stack.pop()
        param1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("!=", param1, param2, result)
        self.push(result)
        
    def geq_less_than(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("<", parm1, parm2, result)
        self.push(result)
        
    def geq_greater_than(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file(">", parm1, parm2, result)
        self.push(result)
        
    def geq_less_than_equal(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("<=", parm1, parm2, result)
        self.push(result)
        
    def geq_greater_than_equal(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file(">=", parm1, parm2, result)
        self.push(result)
        
    def geq_and(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("&&", parm1, parm2, result)
        self.push(result)
        
    def geq_or(self):
        parm2 = self.sem_stack.pop()
        parm1 = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("||", parm1, parm2, result)
        self.push(result)
        
    def geq_not(self):
        param = self.sem_stack.pop()
        result = f"t{self.temp_count}"
        self.temp_count += 1
        self.write_quad_to_file("!", param, None, result)
        self.push(result)
        
    def geq_if_c(self):
        param = self.sem_stack.pop()
        true_result = f"L{self.label_count}"
        self.label_count += 1
        false_result = f"L{self.label_count}"
        self.label_count += 1
        self.write_quad_to_file("if", param, None, true_result)
        self.write_quad_to_file("goto", None, None, false_result)
        self.write_label_to_file(true_result)
        return false_result
    
    def geq_if_bt(self, false_result):
        exit_result = f"L{self.label_count}"
        self.label_count += 1
        self.write_quad_to_file("goto", None, None, exit_result)
        self.write_label_to_file(false_result)
        return exit_result
    
    def geq_if_bf(self, exit_result): 
        self.write_label_to_file(exit_result)
        
    def geq_while_start(self):
        condition_label = f"L{self.label_count}"
        self.label_count += 1
        self.write_label_to_file(condition_label)
        return condition_label
    
    def geq_while_c(self, condition_label):
        param = self.sem_stack.pop()
        true_result = f"L{self.label_count}"
        self.label_count += 1
        false_result = f"L{self.label_count}"
        self.label_count += 1
        self.write_quad_to_file("if", param, None, true_result)
        self.write_quad_to_file("goto", None, None, false_result)
        self.write_label_to_file(true_result)
        return false_result
    def geq_while_bt(self, condition_label, false_result):
        self.write_quad_to_file("goto", None, None, condition_label)
        self.write_label_to_file(false_result)
        
    def geq_for_start(self):
        condition_label = f"L{self.label_count}"
        self.label_count += 1
        self.write_label_to_file(condition_label)
        return condition_label
    
    def geq_for_c2(self, condition_label):
        param = self.sem_stack.pop()
        change_label = f"L{self.label_count}"
        self.label_count += 1
        true_result = f"L{self.label_count}"
        self.label_count += 1
        false_result = f"L{self.label_count}"
        self.label_count += 1
        self.write_quad_to_file("if", param, None, true_result)
        self.write_quad_to_file("goto", None, None, false_result)
        self.write_label_to_file(change_label)
        return change_label, true_result, false_result
    
    def geq_for_c3(self, true_result, condition_label):
        self.write_quad_to_file("goto", None, None, condition_label)
        self.write_label_to_file(true_result)
    
    def geq_for_bt(self, change_label, false_result):
        self.write_quad_to_file("goto", None, None, change_label)
        self.write_label_to_file(false_result)

    # bool Match(TOKEN tok) 
    # check identifier and string
    # LL(1)
    def match(self, tok):
        token = self.peek()
        if not token:
            return False
        if tok == "id" and token[1] == 0:
            self.current += 1
            return True
        if tok == "intc" and token[1] == 1:
            self.current += 1
            return True
        if tok == "str" and token[1] == 2:
            self.current += 1
            return True
        if token[0] == tok:
            self.current += 1
            return True
        return False

    # non-terminals
    # bool START()
    # START -> EX_DECLA | EX_DECLA START
    # Recursive Descent
    def start(self):
        if not self.ex_decla():
            return False
        if self.peek():
            if self.start():
                return True
            return False
        return True
        
    # bool EX_DECLA()
    # EX_DECLA -> FUNC_DEF | DECLA
    # Recursive Descent
    def ex_decla(self):
        token = self.peek()
        if not token:
            return False
        if token[0] in ["double", "int", "char"]:
            tmp = self.current
            if self.decla():
                return True
            self.current = tmp # reset
            if self.func_def():
                return True
        return False

    # bool FUNC_DEF()
    # FUNC_DEF -> TYPE id(PARAM_LIST){BLOCK_ST} | TYPE main(){BLOCK_ST}
    # LL(1)
    def func_def(self):
        if not self.type():
            return False
        token = self.peek()
        if not token:
            return False
        if token[0] == "main":
            if self.match("main") and self.match("(") and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
                return True
        elif self.match("id"):
            if self.match("(") and self.param_list() and self.match(")") and self.match("{") and self.block_st() and self.match("}"):
                return True
        return False

    # bool TYPE()
    # TYPE -> double | int | char 
    # LL(1) / LR(0) reduce
    def type(self):
        token = self.peek()
        if not token:
            return False
        if token[0] == "double":
            return self.match("double")
        if token[0] == "int":
            return self.match("int")
        if token[0] == "char":
            return self.match("char")
        return False
        
    # bool DECLA()
    # DECLA -> TYPE VAR_LIST;
    # Recursive Descent
    def decla(self):
        if self.type():
            if self.var_list():
                if self.match(";"):
                    return True
        return False

    # bool VAR_LIST() 
    # VAR_LIST -> VAR VAR_LIST'
    # VAR_LIST' -> , VAR VAR_LIST' | ɛ 
    # Recursive Descent
    def var_list(self):
        if self.var():
            while self.match(","):
                if not self.var():
                    return False
            return True        
        return False

    # bool VAR() 
    # VAR -> id [intc] | id INITIAL 
    # INTITIAL -> = EP | ɛ 
    # Recursive Descent
    def var(self):
        if self.match("id"):
            self.push(self.tokens[self.current-1][0])
            tmp = self.current
            if self.match("["):
                if self.match("intc"):
                    if self.match("]"):
                        return True
                    return False
                return False
            self.current = tmp
            if self.match("="):
                if self.ep():
                    self.geq_equal()
                    return True
                return False
            self.current = tmp
            return True
        return False

    # bool PARAM_LIST()
    # PARAM_LIST -> ɛ | PARAM | PARAM, PARAM_LIST
    # Recursive Descent
    def param_list(self):
        token = self.peek()
        if token and token[0] == ")":
            return True
        if not self.param():
            return False
        while self.match(","):
            if not self.param():
                return False
        return True
    
    # bool PARAM()
    # PARAM -> TYPE id
    # LR(0) shift
    def param(self):
        if self.type():
            if self.match("id"):
                return True
        return False

    # bool BLOCK_ST()
    # BLOCK_ST -> STATM | STATM BLOCK_ST
    # Recursive Descent
    def block_st(self):
        if not self.statm():
            return False    
        if self.peek()[0] == "}":
            return True
        if self.block_st():
            return True
        return False

    # bool STATM()
    # STATM -> DECLA | ASS_ST | IF_ST | FOR_ST | WHILE_ST | RETURN_ST 
    # LR(0) shift
    def statm(self):
        token = self.peek()
        if not token:
            return False
        if token[0] in ["double", "int", "str"]:
            return self.decla()
        if token[1] == 0:
            return self.ass_st()
        if token[0] == "if":
            return self.if_st()
        if token[0] == "for":
            return self.for_st()
        if token[0] == "while":
            return self.while_st()
        if token[0] == "return":
            return self.return_st()
        return False

    # bool RETURN_ST()
    # RETURN_ST -> return EP; 
    # recursive descent
    def return_st(self):
        if self.match("return") and self.ep() and self.match(";"):
            return True
        return False

    # bool ASS_ST()
    # ASS_ST -> id = EP; 
    # recursive descent
    def ass_st(self):
        if self.match("id"):
            self.push(self.tokens[self.current-1][0])
            if self.match("=") and self.ep() and self.match(";"):
                self.geq_equal()
                return True
        return False

    # bool IF_ST()
    # IF_ST -> if (LOGC_EP){BLOCK_ST} ELSE_ST 
    # recursive descent
    def if_st(self):
        if self.match("if") and self.match("(") and self.logc_ep() and self.match(")"):
            label = self.geq_if_c()
            if self.match("{") and self.block_st() and self.match("}"):
                label = self.geq_if_bt(label)
                if self.else_st():
                    self.geq_if_bf(label)
                    return True
        return False

    # bool ELSE_ST()
    # ELSE_ST -> ɛ | else {BLOCK_ST} 
    # recursive descent
    def else_st(self):
        tmp = self.current
        if self.match("else") and self.match("{") and self.block_st() and self.match("}"):
            return True
        self.current = tmp
        return True

    # bool FOR_ST()
    # FOR_ST -> for (ASS_ST LOGC_EP; AFASS_ST){BLOCK_ST} 
    # recursive descent
    def for_st(self):
        if self.match("for") and self.match("(") and self.ass_st():
            condition_label = self.geq_for_start()
            if self.logc_ep() and self.match(";"):
                change_label, true_result, false_result = self.geq_for_c2(condition_label)
                if self.afass_st() and self.match(")"):
                    self.geq_for_c3(true_result, condition_label)
                    if self.match("{") and self.block_st() and self.match("}"):
                        self.geq_for_bt(change_label, false_result)
                        return True
        
        return False

    # bool AFASS_ST()
    # AFASS_ST -> id = EP
    # recursive descent
    def afass_st(self):
        if self.match("id") and self.match("=") and self.ep():
            
            return True
        
        return False
       

    # bool WHILE_ST()
    # WHILE_ST -> while(LOGC_EP){BLOCK_ST} 
    # recursive descent
    def while_st(self):
        if self.match("while"):
            condition_label = self.geq_while_start()
            if self.match("(") and self.logc_ep() and self.match(")"):
                false_result = self.geq_while_c(condition_label)
                if self.match("{") and self.block_st() and self.match("}"):
                    self.geq_while_bt(condition_label, false_result)
                    return True
        
        return False

    # bool EP()
    # EP -> LOGC_EP | MATH_EP | str
    # recursive descent
    def ep(self):
        tmp = self.current
        if self.match("str"):
            return True
        self.current = tmp # reset
        if self.math_ep():
            return True
        self.current = tmp # reset
        if self.logc_ep():
            return True
        self.current = tmp # reset
        return False

    # bool MATH_EP()
    # MATH_EP -> TD | TD op1 MATH_EP 
    # recursive descent
    def math_ep(self):
        if not self.td():
            return False
        if self.peek() and self.peek()[0] in [",", ")", ";"]:
            return True
        while self.op1():
            op = self.tokens[self.current - 1][0]
            if not self.td():
                return False
            if op == "+":
                self.geq_plus()
            elif op == "-":
                self.geq_minus()
        if self.peek() and self.peek()[0] in [",", ")", ";"]:
            return True

    # bool TD()
    # TD ->TERM | TERM op2 TD
    # recursive descent
    def td(self):
        if not self.term():
            return False
        while self.op2():
            op = self.tokens[self.current - 1][0]
            if not self.term():
                return False
            if op == "*":
                self.geq_mul()
            elif op == "/":
                self.geq_div() 
        return True

    # bool TERM()
    # TERM -> id | intc | real | ( MATH_EP )
    # recursive descent
    def term(self):
        tmp = self.current
        if self.match("id"):
            self.push(self.tokens[self.current-1][0])
            return True
        self.current = tmp # reset
        if self.match("intc"):
            self.push(self.tokens[self.current-1][0])
            return True
        self.current = tmp # reset
        if self.match("real"):
            self.push(self.tokens[self.current-1][0])
            return True
        self.current = tmp # reset
        if self.match("(") and self.math_ep() and self.match(")"):
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_EP()
    # LOGC_EP -> LOGC_ST | LOGC_ST op3 LOGC_ST | ! LOGC_EP
    # recursive descent
    def logc_ep(self):
        tmp = self.current
        if self.logc_st():
            if self.peek() and self.peek()[0] in [",", ")", ";"]:
                return True
            else:
                return False
            if self.op3():
                op = self.tokens[self.current - 1][0]
                if  self.logc_st():
                    if op == "&&":
                        self.geq_and()
                    elif op == "||":
                        self.geq_or()
                    if self.peek() and self.peek()[0] in [",", ")", ";"]:
                        return True
                    else:
                        return False
        self.current = tmp # reset
        if self.match("!"):
            if self.logc_ep():
                self.geq_not()
                return True
            
            return False
        self.current = tmp # reset
        return False

    # bool LOGC_ST()
    # LOGC_ST -> (LOGC_EP) | LOGC_TERM op4 LOGC_TERM
    # recursive descent
    def logc_st(self):
        tmp = self.current
        if self.match("("):
            if self.logc_ep() and self.match(")"): # parenthesis for case of inner comparison
                return True
            
            return False
        self.current = tmp # reset
        if self.logc_term():
            if self.op4():
                op = self.tokens[self.current - 1][0]
                if self.logc_term(): # comparison  
                    if op == "<":
                        self.geq_less_than()
                    elif op == "<=":
                        self.geq_less_than_equal()
                    elif op == ">":
                        self.geq_greater_than()
                    elif op == ">=":
                        self.geq_greater_than_equal()
                    elif op == "==":
                        self.geq_equal_equal()
                    elif op == "!=":
                        self.geq_not_equal()
                    return True
            return False
        self.current = tmp # reset
        
        return False

    # bool LOGC_TERM()
    # LOGC_TERM -> TERM | str
    # recursive descent
    def logc_term(self):
        tmp = self.current
        if self.term():
            return True
        self.current = tmp # reset
        if self.match("str"):
            return True
        self.current = tmp # reset
        return False

    # terminals
    # bool OP1()
    # op1 = { + | - }
    # recursive descent
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
    # recursive descent
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
    # recursive descent
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
    # recursive descent
    def op4(self):
        token = self.peek()
        if token and token[0] in ["<", "<=", ">", ">=", "==", "!="]:
            
            return self.match(token[0])
        
        return False

def transform_file(input_file):
    try:
        with open(input_file, "r") as file:
            content = file.read()
        content = re.sub(r'<"([^"]+)",\s*(\d+)>', r'("\1", \2)', content)
        tokens = eval(f"[{content}]")
        return tokens
    except FileNotFoundError:
        return []
    except Exception as e:
        return []


def generate_quadruple(input_file):
    tokens = transform_file(input_file)
    with open("quad.txt", "w") as f:
        pass
    parser = Parser(tokens)  # Pass the token list to the Parser
    start_parsing = parser.start()
    print("gen_quad finished")
    