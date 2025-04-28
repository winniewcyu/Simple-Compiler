import re # regex
from symbol_table import SymbolTable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.sym_table = SymbolTable()
        self.scope = 1

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    # bool Match(TOKEN tok) 
    # check identifier and string
    # LL(1)
    def match(self, tok):
        token = self.peek()
        if not token:
            print(f"Failed to parse {tok}: no token found at {self.current} position")
            return False
        if tok == "id" and token[1] == 0:
            self.current += 1
            print(f"ID: {token[0]}, current: {self.current}")
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
        print(f"Failed to parse {tok}: no valid token found at {self.current} position")
        return False

    # non-terminals
    # bool START()
    # START -> EX_DECLA | EX_DECLA START
    # Recursive Descent
    def start(self):
        if not self.ex_decla():
            print(f"Failed to parse START: no EX_DECLA found at {self.current} position")
            return False
        print("Passed: EX_DECLA")
        if self.peek():
            if self.start():
                print("Passed: START")
                return True
            print(f"Failed to parse START: no valid EX_DECLA found at {self.current} position")
            return False
        return True
        
    # bool EX_DECLA()
    # EX_DECLA -> FUNC_DEF | DECLA
    # Recursive Descent
    def ex_decla(self):
        outter_var_list = []
        token = self.peek()
        if not token:
            print(f"Failed to parse EX_DECLA: no token found at {self.current} position")
            return False
        if token[0] in ["double", "int", "char"]:
            tmp = self.current
            if self.decla(outter_var_list, None):
                print("Passed: DECLA")
                return True
            self.current = tmp # reset
            if self.func_def():
                print("Passed: FUNC_DEF")
                return True
        print(f"Failed to parse EX_DECLA: no valid token found at {self.current} position")
        return False

    # bool FUNC_DEF()
    # FUNC_DEF -> TYPE id(PARAM_LIST){BLOCK_ST} | TYPE main(){BLOCK_ST}
    # LL(1)
    def func_def(self):
        inner_var_list = []
        return_var_list = []
        if not self.type():
            print(f"Failed to parse FUNC_DEF: no TYPE found at {self.current} position") # checked on the parent layer but just to be sure
            return False
        print("Passed: TYPE")
        type_ = self.tokens[self.current-1][0]
        token = self.peek()
        if not token:
            print(f"Failed to parse FUNC_DEF: no token found at {self.current} position")
            return False
        if token[0] == "main":
            if self.match("main") and self.match("(") and self.match(")") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}"):
                function = self.sym_table.insert_function(type_, len(inner_var_list), return_var_list, inner_var_list )
                self.sym_table.insert("main", "funct", function, self.scope, None)
                print(f"insert function: {type_}, {len(inner_var_list)}, {inner_var_list}, {return_var_list}")
                print(f"insert main function: {self.scope}")
                print("Passed: TYPE main(){BLOCK_ST}")
                return True
        elif self.match("id"):
            func_name = self.tokens[self.current-1][0]
            if self.match("(") and self.param_list() and self.match(")") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}"):
                function = self.sym_table.insert_function(type_, len(inner_var_list), return_var_list, inner_var_list)
                self.sym_table.insert(func_name, "funct", function, self.scope, None)
                print(f"insert function: {type_}, {len(inner_var_list)}, {inner_var_list}, {return_var_list}")
                print(f"insert {func_name} function: {self.scope}")
                print("Passed: TYPE id(PARAM_LIST){BLOCK_ST}")
                return True
        print(f"Failed to parse FUNC_DEF: no valid token found at {self.current} position")
        return False

    # bool TYPE()
    # TYPE -> double | int | char 
    # LL(1) / LR(0) reduce
    def type(self):
        token = self.peek()
        if not token:
            print(f"Failed to parse TYPE: no token found at {self.current} position")
            return False
        if token[0] == "double":
            return self.match("double")
        if token[0] == "int":
            return self.match("int")
        if token[0] == "char":
            return self.match("char")
        print(f"Failed to parse TYPE: no valid token found at {self.current} position")
        return False
        
    # bool DECLA()
    # DECLA -> TYPE VAR_LIST;
    # Recursive Descent
    def decla(self, outter_var_list ,inner_var_list):
        if self.type():
            type_ = self.tokens[self.current - 1][0]
            if inner_var_list is not None:
                var_list = inner_var_list
            elif outter_var_list is not None:
                var_list = outter_var_list
            if self.var_list(var_list):
                if self.match(";"):
                    for var in var_list:
                        if isinstance(var, tuple):
                            var_name, length = var
                            size = self.sym_table.calculate_size(type_, int(length))
                            array = self.sym_table.insert_array(type_, "NULL", length, size)
                            if outter_var_list is not None:
                                self.sym_table.insert(var_name, type_, array, self.scope + 1 , size)
                                print(f"Inserted array: {var_name}, type: {type_}, length: {length}, size: {size}")
                            elif inner_var_list is not None:
                                self.sym_table.insert_function_symbol(var_name, type_, array, self.scope + 1, size)
                                print(f"Inserted array in function symbol table: {var_name}, type: {type_}, length: {length}, size: {size}")
                        else:
                            var_name = var
                            size = self.sym_table.calculate_size(type_, 1)
                            if outter_var_list is not None:
                                self.sym_table.insert(var_name, type_, "NULL", self.scope + 1, size)   
                                print(f"Inserted var: {var_name}, type: {type_}, size: {size}")
                            elif inner_var_list is not None:
                                self.sym_table.insert_function_symbol(var_name, type_, "NULL", self.scope + 1, size)
                                print(f"Inserted var in function symbol table: {var_name}, type: {type_}, size: {size}")            
                    print("Passed: TYPE VAR_LIST;")
                    return True
        return False

    # bool VAR_LIST() 
    # VAR_LIST -> VAR VAR_LIST'
    # VAR_LIST' -> , VAR VAR_LIST' | ɛ 
    # Recursive Descent
    def var_list(self, var_list):
        if self.var(var_list):
            print("Passed: VAR")
            while self.match(","):
                if self.var(var_list):
                    print("Passed: , VAR")
                else:
                    print(f"Failed to parse VAR_LIST: no VAR found after ',' at {self.current} position")
                    return False
            print("Passed: VAR_LIST")
            return True        
        print(f"Failed to parse VAR_LIST: no VAR found at {self.current} position")
        return False

    # bool VAR() 
    # VAR -> id [intc] | id INITIAL 
    # INTITIAL -> = EP | ɛ 
    # Recursive Descent
    def var(self, var_list):
        if self.match("id"):
            tmp = self.current
            if self.match("["):
                if self.match("intc"):
                    var_list.append((self.tokens[self.current - 3][0], self.tokens[self.current - 1][0])) # id, intc
                    if self.match("]"):
                        print("Passed: id [intc]")
                        return True
                    print(f"Failed to parse VAR: no ']' found after intc at {self.current} position")
                    return False
                print(f"Failed to parse VAR: no intc found after '[' at {self.current} position")
                return False
            self.current = tmp
            var_list.append(self.tokens[self.current - 1][0])
            if self.match("="):
                if self.ep():
                    print("Passed: = EP")
                    return True
                print(f"Failed to parse VAR: no EP found after '=' at {self.current} position")
                return False
            self.current = tmp
            print("Passed: ɛ")
            print("Passed: id INITIAL")
            return True
        print(f"Failed to parse VAR: no id found at {self.current} position")
        return False

    # bool PARAM_LIST()
    # PARAM_LIST -> ɛ | PARAM | PARAM, PARAM_LIST
    # Recursive Descent
    def param_list(self):
        token = self.peek()
        if token and token[0] == ")":
            print("Passed: ɛ (param_list)")
            return True
        if not self.param():
            print(f"Failed to parse PARAM_LIST: no PARAM found at {self.current} position")
            return False
        print("Passed: PARAM")
        while self.match(","):
            if not self.param():
                print(f"Failed to parse PARAM_LIST: no PARAM found after ',' at {self.current} position")
                return False
            print("Passed: , PARAM")
        print("Passed: PARAM_LIST")
        return True
    
    # bool PARAM()
    # PARAM -> TYPE id
    # LR(0) shift
    def param(self):
        if self.type():
            print("Passed: TYPE, Shift: TYPE")
            if self.match("id"):
                print("Passed: TYPE id, Shift: id")
                return True
        return False

    # bool BLOCK_ST()
    # BLOCK_ST -> STATM | STATM BLOCK_ST
    # Recursive Descent
    def block_st(self, inner_var_list, return_var_list):
        if not self.statm(inner_var_list, return_var_list):
            print(f"Failed to parse BLOCK_ST: no STATM found at {self.current} position")
            return False    
        print("Passed: STATM")
        if self.peek()[0] == "}":
            print("Passed: BLOCK_ST (after set } checking)")
            return True
        if self.block_st(inner_var_list, return_var_list):
            print("Passed: BLOCK_ST")
            return True
        return False

    # bool STATM()
    # STATM -> DECLA | ASS_ST | IF_ST | FOR_ST | WHILE_ST | RETURN_ST 
    # LR(0) shift
    def statm(self, inner_var_list, return_var_list):
        token = self.peek()
        if not token:
            print(f"Failed to parse STATM: no token found at {self.current} position")
            return False
        if token[0] in ["double", "int", "str"]:
            return self.decla(None, inner_var_list)
        if token[1] == 0:
            return self.ass_st()
        if token[0] == "if":
            return self.if_st(inner_var_list, return_var_list)
        if token[0] == "for":
            return self.for_st(inner_var_list, return_var_list)
        if token[0] == "while":
            return self.while_st(inner_var_list, return_var_list)
        if token[0] == "return":
            return self.return_st(return_var_list)
        print(f"Failed to parse STATM: no valid token found at {self.current} position")
        return False

    # bool RETURN_ST()
    # RETURN_ST -> return EP; 
    # recursive descent
    def return_st(self, return_var_list):
        if self.match("return") and self.ep() and self.match(";"):
            return_var_list.append(self.tokens[self.current - 2][0])
            print("Passed: return EP;")
            return True
        print(f"Failed to parse RETURN_ST at {self.current} position")
        return False

    # bool ASS_ST()
    # ASS_ST -> id = EP; 
    # recursive descent
    def ass_st(self):
        if self.match("id") and self.match("=") and self.ep() and self.match(";"):
            print("Passed: id = EP;")
            return True
        print(f"Failed to parse ASS_ST at {self.current} position")
        return False

    # bool IF_ST()
    # IF_ST -> if (LOGC_EP){BLOCK_ST} ELSE_ST 
    # recursive descent
    def if_st(self, inner_var_list, return_var_list):
        if self.match("if") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}") and self.else_st(inner_var_list, return_var_list):
            print("Passed: if (LOGC_EP){BLOCK_ST} ELSE_ST")
            return True
        print(f"Failed to parse IF_ST at {self.current} position")
        return False

    # bool ELSE_ST()
    # ELSE_ST -> ɛ | else {BLOCK_ST} 
    # recursive descent
    def else_st(self, inner_var_list, return_var_list):
        tmp = self.current
        if self.match("else") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}"):
            print("Passed: else {BLOCK_ST}")
            return True
        self.current = tmp
        print("Passed: ɛ (else_st)")
        return True

    # bool FOR_ST()
    # FOR_ST -> for (ASS_ST LOGC_EP; AFASS_ST){BLOCK_ST} 
    # recursive descent
    def for_st(self, inner_var_list, return_var_list):
        if self.match("for") and self.match("(") and self.ass_st():
            if self.logc_ep() and self.match(";") and self.afass_st() and self.match(")") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}"):
                print("Passed: for (ASS_ST LOGC_EP; ASS_ST){BLOCK_ST}")
                return True
            print(f"Failed to parse FOR_ST without matching logc_ep at {self.current} position")
            return False
        print(f"Failed to parse FOR_ST at {self.current} position")
        return False

    # bool AFASS_ST()
    # AFASS_ST -> id = EP
    # recursive descent
    def afass_st(self):
        if self.match("id") and self.match("=") and self.ep():
            print("Passed: id = EP")
            return True
        print(f"Failed to parse AFASS_ST at {self.current} position")
        return False
       

    # bool WHILE_ST()
    # WHILE_ST -> while(LOGC_EP){BLOCK_ST} 
    # recursive descent
    def while_st(self, inner_var_list, return_var_list):
        if self.match("while") and self.match("(") and self.logc_ep() and self.match(")") and self.match("{") and self.block_st(inner_var_list, return_var_list) and self.match("}"):
            print("Passed: while(LOGC_EP){BLOCK_ST}")
            return True
        print(f"Failed to parse WHILE_ST at {self.current} position")
        return False

    # bool EP()
    # EP -> LOGC_EP | MATH_EP | str
    # recursive descent
    def ep(self):
        tmp = self.current
        if self.match("str"):
            print("Passed: str")
            id_list.append("char")
            return True
        self.current = tmp # reset
        if self.math_ep():
            print("Passed: MATH_EP")
            return True
        self.current = tmp # reset
        if self.logc_ep():
            print("Passed: LOGC_EP")
            return True
        self.current = tmp # reset
        print(f"Failed to parse EP at {self.current} position")
        return False

    # bool MATH_EP()
    # MATH_EP -> TD | TD op1 MATH_EP 
    # recursive descent
    def math_ep(self):
        id_list = []
        var1 = None
        if not self.td(id_list):
            print(f"Failed to parse MATH_EP at {self.current} position")
            return False
        if not id_list or any(var_type not in ["int", "double"] for var_type in id_list):
            print(f"Semantic Error: Non-numeric type found in MATH_EP at position {self.current}")
            return False
        var1 = id_list[0]
        print("Passed: TD")
        if self.peek() and self.peek()[0] in [",", ")", ";"]:
            return True
        while self.op1():
            id_list = []
            if not self.td(id_list):
                print(f"Failed to parse MATH_EP at {self.current} position")
                return False
            if not id_list or any(var_type not in ["int", "double"] for var_type in id_list):
                print(f"Semantic Error: Non-numeric type found in MATH_EP at position {self.current}")
                return False
            var2 = id_list[0]  # Second operand type
            if var1 != var2:
                print(f"Semantic Error: {var1} cannot be + or - with {var2}")
                return False
            id_list = [var1]
            print("Passed: TD op1 MATH_EP")
        if self.peek() and self.peek()[0] in [",", ")", ";"]:
            return True

    # bool TD()
    # TD ->TERM | TERM op2 TD
    # recursive descent
    def td(self, id_list):
        var1 = None
        if not self.term(id_list):
            print(f"Failed to parse TD at {self.current} position")
            return False
        if not id_list or any(var_type not in ["int", "double"] for var_type in id_list):
            print(f"Semantic Error: Non-numeric type found in TD at position {self.current}")
            return False
        var1 = id_list[0]
        print("Passed: TERM")
        while self.op2():
            id_list = []
            if not self.term(id_list):
                print(f"Failed to parse TD at {self.current} position")
                return False
            if not id_list or any(var_type not in ["int", "double"] for var_type in id_list):
                print(f"Semantic Error: Non-numeric type found in TD at position {self.current}")
                return False
            var2 = id_list[0]  # Second operand type
            if var1 != var2:
                print(f"Semantic Error: {var1} cannot be * or / with {var2}")
                return False
            id_list = [var1]
            print("Passed: TERM op2 TD")
        return True

    # bool TERM()
    # TERM -> id | intc | real | ( MATH_EP )
    # recursive descent
    def term(self, id_list):
        tmp = self.current
        if self.match("id"):
            id_name = self.tokens[self.current - 1][0]
            id_node = self.sym_table.search_function_symbol(id_name)
            if not id_node:
                print(f"Failed to retrieve type from function symbol table for {id_name} at {self.current} position")
                id_node = self.sym_table.search(id_name)
                if not id_node:
                    print(f"Failed to retrieve type from symbol table for {id_name} at {self.current} position")
                    return False
            id_list.append(id_node.type)
            print(f"Retrieved id type: {id_node.type} for {id_name} at {self.current} position")
            print("Passed: id")
            return True
        self.current = tmp # reset
        if self.match("intc"):
            print("Passed: intc")
            id_list.append("int")
            return True
        self.current = tmp # reset
        if self.match("real"):
            print("Passed: real")
            id_list.append("double")
            return True
        self.current = tmp # reset
        if self.match("(") and self.math_ep() and self.match(")"):
            print("Passed: ( MATH_EP )")
            return True
        self.current = tmp # reset
        return False

    # bool LOGC_EP()
    # LOGC_EP -> LOGC_ST | LOGC_ST op3 LOGC_ST | ! LOGC_EP
    # recursive descent
    def logc_ep(self):
        id_list = []
        tmp = self.current
        if self.logc_st(id_list):
            if self.op3() and self.logc_st(id_list):
                print("Passed: LOGC_ST op3 LOGC_ST")
                if self.peek() and self.peek()[0] in [",", ")", ";"]:
                    return True
                else:
                    print(f"Failed to parse LOGC_EP: no after set ',' or ')' or ';' found after LOGC_ST op3 LOGC_ST at {self.current} position")
                    return False
        self.current = tmp # reset
        if self.match("!"):
            if self.logc_ep():
                print("Passed: ! LOGC_EP")
                return True
            print(f"Failed to parse LOGC_EP: no LOGC_EP found after '!' at {self.current} position")
            return False
        self.current = tmp # reset
        if self.logc_st(id_list):
            print("Passed: LOGC_ST")
            if self.peek() and self.peek()[0] in [",", ")", ";"]:
                return True
            else:
                print(f"Failed to parse LOGC_EP: no after set ',' or ')' or ';' found after LOGC_ST at {self.current} position")
                return False
        self.current = tmp # reset
        print(f"Failed to parse LOGC_EP at {self.current} position")
        return False

    # bool LOGC_ST()
    # LOGC_ST -> (LOGC_EP) | LOGC_TERM op4 LOGC_TERM
    # recursive descent
    def logc_st(self, id_list):
        var1 = None
        tmp = self.current
        if self.match("("):
            if self.logc_ep() and self.match(")"): # parenthesis for case of inner comparison
                print("Passed: (LOGC_EP)")
                return True
            print(f"Failed to parse LOGC_ST: no LOGC_EP found after '(' at {self.current} position")
            return False
        self.current = tmp # reset
        if self.logc_term(id_list):
            var1 = id_list[0]
            if not var1 in ["int", "double", "char"]:
                print(f"Semantic Error: error in type {var1} at position {self.current}")
                return False
            id_list = []
            if self.op4():
                op = self.tokens[self.current - 1][0]
                if var1 is "char":
                    if op in ["<", "<=", ">", ">="]:
                        print(f"Semantic Error: {var1} cannot be < or <= or > or >=")
                        return False
                if self.logc_term(id_list): # comparison
                    if var1 != id_list[0]:
                        print(f"Semantic Error: {var1} cannot be == or != or < or <= or > or >= with {id_list[0]}")
                        return False
                    id_list = [var1]
                    print("Passed: LOGC_TERM op4 LOGC_TERM")
                    return True
            print(f"Failed to parse LOGC_ST: no LOGC_TERM found after op4 at {self.current} position")
            return False
        self.current = tmp # reset
        print(f"Failed to parse LOGC_ST at {self.current} position")
        return False

    # bool LOGC_TERM()
    # LOGC_TERM -> TERM | str
    # recursive descent
    def logc_term(self, id_list):
        tmp = self.current
        if self.term(id_list):
            print("Passed: TERM(logc_term)")
            return True
        self.current = tmp # reset
        if self.match("str"):
            id_list.append("char")
            print("Passed: str(logc_term)")
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
    # recursive descent
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
    # recursive descent
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
    # recursive descent
    def op4(self):
        token = self.peek()
        if token and token[0] in ["<", "<=", ">", ">=", "==", "!="]:
            print(f"Passed: {token[0]}")
            return self.match(token[0])
        print(f"Failed to parse OP4: no OP4 found at {self.current} position")
        return False

def transform_file(input_file):
    try:
        with open(input_file, "r") as file:
            content = file.read()
        content = re.sub(r'<"([^"]+)",\s*(\d+)>', r'("\1", \2)', content)
        tokens = eval(f"[{content}]")
        return tokens
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return []
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []

def parse_file(input_file):
    tokens = transform_file(input_file)
    parser = Parser(tokens)  # Pass the token list to the Parser
    start_parsing = parser.start()
    if start_parsing == True:
        print("Parsing successful, Accepted.")
        return True
    else:
        print("Parsing failed, Rejected.")
        return False