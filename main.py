import argparse
from imgtoascii import AsciiArt

def main():
    parser = argparse.ArgumentParser(
        prog="imgtoascii",
        description="A program that converts images into ASCII Art"
    )
    parser.add_argument("path", help="path of the source image")
    parser.add_argument("--cols", default=120, type=int, help="columns (or width) of the output image")
    parser.add_argument("--fill", action="store_true", default=False, help="use filled characters instead of letters and symbols")
    parser.add_argument("--color", action="store_true", default=False, help="print colored characters instead of monochrome")
    parser.add_argument("--chars", help="characters to use instead of grayscale")
    parser.add_argument("--output", help="print result in the specified file")
    parser.add_argument("--png", action="store_true", help="save ascii art as PNG image")
    args = parser.parse_args()

    try:
        img = AsciiArt(args.path)
        if args.png:
            img.to_png(args.cols, args.output, args.color, args.fill)
        elif args.output:
            img.to_file(args.cols, args.output, args.fill)
        else:
            img.to_terminal(args.cols, args.color, args.fill, args.chars)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()
    