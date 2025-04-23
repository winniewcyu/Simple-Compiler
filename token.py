import re # regex

IDENTIFIER_REGEX = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]{0,30}$')

# Part 1: Lexical Analysis
class Token:
    def __init__(self, token_str, token_type_num, token_type):
        self.token_str = token_str
        self.token_type_num = token_type_num
        self.token_type = token_type

    def __str__(self):
        return f"<\"{self.token_str}\", {self.token_type_num}>"
    
    def debug_str(self):
        return f"<\"{self.token_str}\", {self.token_type}>"

# constant 
token  = {
    # keyword
    "int": 10,
    "main": 11, 
    "char": 12, 
    "for": 13, 
    "if": 14, 
    "else": 15, 
    "return": 16,
    "while": 17,
    "double": 18,
    # operator
    "=": 30, 
    "==": 31, 
    ">=": 32, 
    "<=": 33, 
    ">": 34, 
    "<": 35, 
    "+": 36, 
    "-": 37, 
    "*": 38, 
    "/": 39,
    "!=": 40,
    "&&": 41,
    "||": 42,
    "!": 43,
    # punctuation
    "{": 50,
    "}": 51, 
    ",": 52, 
    ";": 53, 
    "(": 54, 
    ")": 55, 
    "[": 56, 
    "]": 57
}
# identifier
def create_identifier_token(value):
    if value in token:
        if token[value] == 0:
            return Token(value, 0, "identifier")
        else:
            token[value] = 0
            return Token(value, 0, "identifier")
    elif value not in token:
        token[value] = 0
        return Token(value, 0, "identifier")

# integer
def create_integer_token(value):
    if value in token:
        if token[value] == 1:
            return Token(value, 1, "integer")
        else:
            token[value] = 1
            return Token(value, 1, "integer")
    elif value not in token:
        token[value] = 1
        return Token(value, 1, "integer")

# string
def create_string_token(value):
    if value not in token:
        token[value] = 2
    return Token(value, 2, "string")

# keyword
def retrieve_keyword(key):
    if key in token:
        return Token(key, token[key], "keyword")
    else:
        print("Not a keyword")
        return None
    
# operator
def retrieve_operator(key):
    if key in token:
        return Token(key, token[key], "operator")
    else:
        print("Not an operator")
        return None

# punctuation
def retrieve_punctuation(key):
    if key in token:
        return Token(key, token[key], "punctuation")
    else:
        print("Not a punctuation")
        return None

def tokenize(input_file, output_file):
    try:
        with open(input_file, "r") as file:
            input_string = file.read()  # Read the entire content of the file into input_string
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        exit()

    log_token =[]
    result = []
    
    # Tokenize input
    i = 0
    while i < len(input_string):
        char = input_string[i]
        
        # Skip spaces and whitespace characters
        if char.isspace():
            i += 1
            continue
        
        # Process numbers (0-9)
        # currently just unsigned integer instead of signed real number
        # distinguish between number and operator is spacing
        elif char.isdigit():
            start = i
            while i < len(input_string) and input_string[i].isdigit():
                i += 1
            if i < len(input_string) and input_string[i].isalpha():
                print(f"Error: unexpected character '{input_string[i]}' at position {i}")
                exit()
            value = input_string[start:i]
            result.append(create_integer_token(value))
        
        # Process strings (enclosed in quotes)
        elif char == "\"": 
            # if there is new line in the string, report and throw error
            i += 1  # Skip opening quote
            start = i
            value = []
            while i < len(input_string) and input_string[i] != "\"":
                if input_string[i] == "\n": # check for new line
                    print(f"Error: new line in string at position {start-1}")
                    exit()
                    
                if input_string[i] == "\\":
                    escape_char = input_string[i+1]
                    if escape_char in ["n", "t", "'", "\"", "\\", "0"]:
                        value.append(f"\\{escape_char}")
                        i += 1
                    else:
                        value.append(f"\\")
                        i += 1
                else:
                    value.append(input_string[i])
                i += 1
                if i == len(input_string):  # Check for unclosed / outbound string
                    print(f"Error: unclosed string at position {start-1}")
                    exit()
            
            i += 1  # Skip closing quote
            result.append(create_string_token("".join(value)))
            # result.append(create_string_token(" ".join(value)))
        
        # Process keywords and identifiers (letters a-z, A-Z)
        elif char.isalpha():
            start = i
            while i < len(input_string) and input_string[i].isspace() == False:
                i += 1 
            value = input_string[start:i]
            if IDENTIFIER_REGEX.match(value):
                if value in token and token[value] >= 10:  # Check if it's a keyword
                    result.append(retrieve_keyword(value))
                else:  # Otherwise, it's an identifier
                    result.append(create_identifier_token(value))
            else:
                print(f"Error: invalid identifier at position {start} (dismatched regex)")
                exit()
        
        # Process operators and punctuation
        elif i + 1 < len(input_string) and input_string[i:i+2] in token:
            value = input_string[i:i+2]
            if token[value] >= 30:  # Operators
                result.append(retrieve_operator(value))
                i += 2
        elif char in token:
            if token[char] >= 30:  # Operators
                result.append(retrieve_operator(char))
            elif token[char] >= 50:  # Punctuation
                result.append(retrieve_punctuation(char))
            i += 1
        
        # Move to the next character
        else:
            print(f"Unknown character: {char}")
            i += 1

    # debug print
    log_token = [token.debug_str() for token in result]
    print(", ".join(log_token))
    # Write result to a file
    with open(output_file, "w") as file:
        file.write(", ".join(str(token) for token in result))

    return result 