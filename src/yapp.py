import html_converter
import latex_converter
import preprocessor
import argparse

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='yaPP: yet another PreProcessor')
    args_parser.add_argument('input_file', nargs=1, type=str, metavar='input_file', help='input file path')
    args_parser.add_argument('output_file', nargs=1, type=str, metavar='output_file', help='output file path')
    args_parser.add_argument('-t', '--to', nargs=1, type=str, default='html', choices=['html', 'latex'], help='markup language to convert to')

    args = args_parser.parse_args()

    if args.to[0] == 'latex':
        c = latex_converter.LatexConverter
    else:
        c = html_converter.HtmlConverter

    input = open(args.input_file[0], 'r').read()

    p = preprocessor.Preprocessor(c, input)

    p.process()

    output = open(args.output_file[0], 'w')
    p.write(output)
