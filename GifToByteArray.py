import argparse
from PIL import Image, ImageSequence
import os

def program(inputpath, outputpath, width, height, threshold=128):
    # Ensure the output path exists
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # Open the GIF file
    with Image.open(inputpath) as im:
        # Process each frame
        frames = []
        for frame in ImageSequence.Iterator(im):
            # Convert to grayscale
            gray_frame = frame.convert('L').resize((width, height))

            # Apply threshold to convert to black and white
            bw_frame = gray_frame.point(lambda x: 255 if x > threshold else 0, '1')
            frames.append(bw_frame)

    # Prepare to store byte arrays as hexadecimal values
    frame_hex_arrays = []

    # Save frames and their byte arrays as hexadecimal values
    for i, frame in enumerate(frames):
        # Save the frame as an image
        #frame_path = os.path.join(outputpath, f"frame_{i}.png")
        #frame.save(frame_path)

        # Convert frame to byte array and then to a list of hexadecimal values
        hex_values = [f'0x{byte:02x}' for byte in frame.tobytes()]
        frame_hex_arrays.append(", ".join(hex_values))

    # Save the hexadecimal arrays to a file
    with open(os.path.join(outputpath, 'file.py'), 'w') as file:
        file.write('frames = [\n')
        for hex_values in frame_hex_arrays:
            file.write(f"[{hex_values}],\n")
        file.write(']')

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert a GIF to black and white, resize, and extract frames.')
    parser.add_argument('inputpath', type=str, help='Path to the input GIF file.')
    parser.add_argument('outputpath', type=str, help='Path to store the output frames and file.py.')
    parser.add_argument('width', type=int, help='Width to resize the frames.')
    parser.add_argument('height', type=int, help='Height to resize the frames.')
    parser.add_argument('--threshold', type=int, default=128, help='Threshold for black and white conversion (default: 128).')

    args = parser.parse_args()

    # Run the program with provided arguments
    program(args.inputpath, args.outputpath, args.width, args.height, args.threshold)


