from lexical import tokenize
from parsing import parse_file
from semantic import generate_quadruple

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"
    tokenize(input_file, output_file)
    check_result = parse_file(output_file)
    if check_result is True:
        generate_quadruple(output_file)