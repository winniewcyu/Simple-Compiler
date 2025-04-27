from lexical import tokenize
from parsing import parse_file

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"
    tokenize(input_file, output_file)
    parse_file(output_file)