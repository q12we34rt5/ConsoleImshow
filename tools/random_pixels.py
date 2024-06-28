import sys
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Generate random pixels')
    parser.add_argument('width', type=int, help='Width of the image')
    parser.add_argument('height', type=int, help='Height of the image')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    args = parser.parse_args()

    # RAII
    def get_output(): return open(args.output, 'w') if args.output else sys.stdout

    image = np.random.randint(0, 256, (args.height, args.width, 3), dtype=np.uint8)

    # Output format: row:int col:int R:uint8 G:uint8 B:uint8
    with get_output() as f:
        for row in range(args.height):
            for col in range(args.width):
                f.write(f'{row} {col} {image[row, col, 0]} {image[row, col, 1]} {image[row, col, 2]}\n')


if __name__ == '__main__':
    main()
