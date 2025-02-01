import os
import argparse
import subprocess
from vidtoolbox.generate_timestamps import generate_timestamps, create_file_list, display_timestamps

def merge_videos(video_directory, output_file=None, keep_filelist=False):
    """Generate timestamps.txt first, confirm, and then merge videos."""
    # Ensure timestamps.txt is up-to-date
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if os.path.exists(timestamps_path):
        print(f"\n🛑 Detected an existing `{folder_name}.txt`, regenerating...")
        os.remove(timestamps_path)

    generate_timestamps(video_directory)  # Generate timestamps.txt first

    # Read and display `timestamps.txt`
    if not display_timestamps(video_directory):
        return

    # Confirm if the timestamps are correct
    confirm = input("\n✅ Confirm that the timestamps are correct? (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ Merge canceled!")
        return

    # Ensure that the merged video does not include an existing merged file
    files = create_file_list(video_directory)
    if files is None:
        return

    # Default video name is the folder name
    if not output_file:
        output_file = os.path.join(video_directory, f"{folder_name}.mp4")
    else:
        output_file = os.path.join(video_directory, output_file)

    # Generate file_list.txt
    file_list_path = os.path.join(video_directory, "file_list.txt")
    with open(file_list_path, "w") as f:
        for file in files:
            # Use the correct absolute path to avoid multi-directory issues
            file_path = os.path.abspath(os.path.join(video_directory, file))
            f.write(f"file '{file_path}'\n")

    print(f"\n🚀 **Starting video merge, output file:** {output_file}\n")

    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", file_list_path, "-c", "copy", output_file
    ]
    
    subprocess.run(cmd)
    print(f"✅ Video merge completed! Output file: {output_file}")

    # **Automatically delete file_list.txt**
    if not keep_filelist:
        os.remove(file_list_path)
        print("🧹 `file_list.txt` deleted")

def main():
    parser = argparse.ArgumentParser(description="Merge multiple .mp4 videos and ensure timestamps.txt is confirmed first")
    parser.add_argument("video_directory", help="Directory containing video files")
    parser.add_argument("-o", "--output", help="Output video filename (default is the folder name)")
    parser.add_argument("--keep-filelist", action="store_true", help="Keep file_list.txt")

    args = parser.parse_args()
    merge_videos(args.video_directory, args.output, args.keep_filelist)

if __name__ == "__main__":
    main()
