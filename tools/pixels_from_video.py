import cv2
import sys
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description='Convert a video to a list of pixels')
    parser.add_argument('path', help='Path of the video')
    parser.add_argument('-wd', '--width', type=int, help='Output width (default: original width)')
    parser.add_argument('-ht', '--height', type=int, help='Output height (default: original height)')
    parser.add_argument('-s', '--scale', type=float, help='Output scale (default: 1.0)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--transparent', nargs=3, type=int, help='Transparent color (default: None)')
    args = parser.parse_args()

    # RAII
    def get_output(): return open(args.output, 'w') if args.output else sys.stdout\

    # Load the video
    cap = cv2.VideoCapture(args.path)

    # Get the video information
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Calculate the output size
    if args.width is None and args.height is None and args.scale is None:
        width, height = int(width), int(height)
    elif args.width is None and args.height is None:
        width, height = int(width * args.scale), int(height * args.scale)
    elif args.width is None:
        width, height = int(args.height / height * width), args.height
    elif args.height is None:
        width, height = args.width, int(args.width / width * height)
    else:
        width, height = args.width, args.height

    # Output format: row:int col:int R:uint8 G:uint8 B:uint8
    frame_time = 1.0 / fps  # time per frame in seconds
    transparent = tuple(args.transparent) if args.transparent is not None else (-1, -1, -1)
    with get_output() as f:
        current_frame_time = time.time()
        while cap.isOpened():
            current_frame_time += frame_time  # Update the current frame time
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            # Skip the frame if out of time
            if start_time > current_frame_time:
                continue
            # Process the frame
            frame = cv2.resize(frame, (width, height))
            for row in range(height):
                for col in range(width):
                    # opencv uses BGR instead of RGB
                    B, G, R = frame[row, col]
                    if (R, G, B) == transparent:
                        continue
                    f.write(f'{row} {col} {R} {G} {B}\n')
            f.write('\n')
            # Wait for the next frame
            elapsed_time = time.time() - start_time
            sleep_time = frame_time - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)


if __name__ == '__main__':
    main()
