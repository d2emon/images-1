import sys


def main(input_file, output_file):
    print(input_file, output_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("images-1.py <inputfile> <outputfile>")
        sys.exit(0)
    input_file, output_file = sys.argv[1:3]
    main(input_file, output_file)
