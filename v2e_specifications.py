"""
Python code for extracting video specifications to use as an input for V2E.

V2E script converts RGB videos to synthesizing fake DVS
events after SuperSloMo has generated interpolated
frames from the original video frames.

@author: Mustafa Sakhai
@contact: msakhai@agh.edu.pl
"""


import cv2
import argparse


def get_video_specs(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Unable to open video file")
        return None

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()

    return frame_count, fps, width, height


def main():
    parser = argparse.ArgumentParser(description='Customize video processing arguments')
    parser.add_argument('-i', '--input_video', required=True, help='Input video file path')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--auto_timestamp_resolution', type=bool, default=False,
                        help='Automatically set timestamp resolution')
    parser.add_argument('--dvs_exposure', nargs='+', type=float, help='DVS exposure duration')
    parser.add_argument('--output_folder', help='Output folder path')
    parser.add_argument('--pos_thres', type=float, default=0.15, help='Positive threshold')
    parser.add_argument('--neg_thres', type=float, default=0.15, help='Negative threshold')
    parser.add_argument('--sigma_thres', type=float, default=0.03, help='Sigma threshold')
    parser.add_argument('--dvs_aedat2', help='DVS aedat2 file path')
    parser.add_argument('--output_width', type=int, help='Output width')
    parser.add_argument('--output_height', type=int, help='Output height')
    parser.add_argument('--stop_time', type=int, default=3, help='Stop time')
    parser.add_argument('--cutoff_hz', type=int, default=15, help='Cutoff frequency in Hz')

    args = parser.parse_args()

    # Get video specifications
    frame_count, fps, width, height = get_video_specs(args.input_video)

    if frame_count is None:
        return

    # Customize arguments based on video specifications
    timestamp_resolution = 1 / fps if fps else 0  # Set timestamp resolution based on FPS if available
    output_width = width // 2 if width else 0  # Set output width to half of the original width if available
    output_height = height // 2 if height else 0  # Set output height to half of the original height if available

    # Print customized arguments
    print(
        f"--timestamp_resolution={timestamp_resolution} --output_width={output_width} --output_height={output_height}")
    print(
        f"--overwrite --auto_timestamp_resolution={args.auto_timestamp_resolution} --dvs_exposure duration {args.dvs_exposure} --output_folder={args.output_folder} --pos_thres={args.pos_thres} --neg_thres={args.neg_thres} --sigma_thres={args.sigma_thres} --dvs_aedat2 {args.dvs_aedat2} --output_width={args.output_width} --output_height={args.output_height} --stop_time={args.stop_time} --cutoff_hz={args.cutoff_hz}")


if __name__ == "__main__":
    main()
