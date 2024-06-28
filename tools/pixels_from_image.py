from PIL import Image
import sys
import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Convert an image to a list of pixels')
    parser.add_argument('path', help='Path of the image')
    parser.add_argument('-wd', '--width', type=int, help='Output width (default: original width)')
    parser.add_argument('-ht', '--height', type=int, help='Output height (default: original height)')
    parser.add_argument('-s', '--scale', type=float, help='Output scale (default: 1.0)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    args = parser.parse_args()

    # RAII
    def get_output(): return open(args.output, 'w') if args.output else sys.stdout

    # Load the image
    image = Image.open(args.path)

    # Calculate the output size
    if args.width is None and args.height is None and args.scale is None:
        width, height = image.size
    elif args.width is None and args.height is None:
        width, height = int(image.width * args.scale), int(image.height * args.scale)
    elif args.width is None:
        width, height = int(args.height / image.height * image.width), args.height
    elif args.height is None:
        width, height = args.width, int(args.width / image.width * image.height)
    else:
        width, height = args.width, args.height

    # Process the image
    if width != image.width or height != image.height:
        image = image.resize((width, height))
    image = np.asarray(image)

    # Output format: row:int col:int R:uint8 G:uint8 B:uint8
    if image.shape[2] == 3:
        image = np.concatenate((image, np.full((height, width, 1), 255, dtype=np.uint8)), axis=2)
    with get_output() as f:
        for row in range(height):
            for col in range(width):
                if image[row, col, 3] == 0:
                    continue
                f.write(f'{row} {col} {image[row, col, 0]} {image[row, col, 1]} {image[row, col, 2]}\n')


if __name__ == '__main__':
    main()
