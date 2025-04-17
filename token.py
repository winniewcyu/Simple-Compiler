# Part 1: Lexical Analysis
class Token:
    def __init__(self, token_str, token_type_num, token_type):
        self.token_str = token_str
        self.token_type_num = token_type_num
        self.token_type = token_type
        self.debug_str()

    def __str__(self):
        return f"<\"{self.token_str}\", {self.token_type_num}>"
    
    def debug_str(self):
        log_token.append(f"<\"{self.token_str}\", {self.token_type}>")

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

if __name__ == "__main__":
    
    # Read input string from a file
    input_file = "input.txt"  # Name of the input file

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
            value = input_string[start:i]
            result.append(create_integer_token(value))
        
        # Process strings (enclosed in quotes)
        elif char == "\"":
            i += 1  # Skip opening quote
            start = i
            value = []
            while i < len(input_string) and input_string[i] != "\"":
                if input_string[i] == "\\":
                    escape_char = input_string[i+1]
                    if escape_char == ["n", "t", "'", "\"", "\\", "0"]:
                        value.append(f"\\{escape_char}")
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
            while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == "_"):
                i += 1
            value = input_string[start:i]
            if value in token and token[value] >= 10:  # Check if it's a keyword
                result.append(retrieve_keyword(value))
            else:  # Otherwise, it's an identifier
                result.append(create_identifier_token(value))
        
        # Process operators and punctuation
        elif char in token:
            if input_string[i:i+2] in token:  # Check for two-character operators
                value = input_string[i:i+2]
                result.append(retrieve_operator(value))
                i += 2
            else:
                value = char
                if value in token:
                    if token[value] >= 30:  # Operators
                        result.append(retrieve_operator(value))
                    elif token[value] >= 50:  # Punctuation
                        result.append(retrieve_punctuation(value))
                i += 1
        
        # Move to the next character
        else:
            print(f"Unknown character: {char}")
            i += 1

    # debug print
    print(", ".join(log_token))
    # Write result to a file
    with open("output.txt", "w") as file:
        for token in result:
            file.write(str(token) + ", ")