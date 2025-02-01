import os
import subprocess
import argparse

def format_duration(seconds):
    """Convert seconds into HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_file_size(file_path):
    """Get file size in MB."""
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb

def get_video_info(video_directory, sort_by="name"):
    """Retrieve video resolution, duration, and file size from a given directory and sort the output."""
    files = [f for f in os.listdir(video_directory) if f.endswith('.mp4')]

    video_data = []
    for file in files:
        file_path = os.path.join(video_directory, file)

        # Get video resolution
        cmd_size = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
            file_path
        ]
        width_height = subprocess.check_output(cmd_size).decode().strip()

        # Get video duration
        cmd_duration = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'format=duration', '-of', 'csv=p=0',
            file_path
        ]
        duration = float(subprocess.check_output(cmd_duration).decode().strip())
        formatted_duration = format_duration(duration)

        # Get file size
        file_size = get_file_size(file_path)

        video_data.append((file, width_height, formatted_duration, file_size, duration))

    # **Sort videos based on user selection**
    if sort_by == "name":
        video_data.sort(key=lambda x: x[0])  # Sort by filename
    elif sort_by == "size":
        video_data.sort(key=lambda x: x[3], reverse=True)  # Sort by file size (largest to smallest)
    elif sort_by == "duration":
        video_data.sort(key=lambda x: x[4], reverse=True)  # Sort by duration (longest to shortest)

    # **Print output**
    print("\n📌 Video Information:")
    for file, width_height, formatted_duration, file_size, _ in video_data:
        print(f"Video: {file}, Resolution: {width_height}, Duration: {formatted_duration}, File Size: {file_size:.2f} MB")

def main():
    parser = argparse.ArgumentParser(description="Retrieve video resolution, duration, and file size with sorting options")
    parser.add_argument("video_directory", help="Directory containing video files")
    parser.add_argument("--sort", choices=["name", "size", "duration"], default="name",
                        help="Sorting method: name (default), size (file size), duration (video length)")
    
    args = parser.parse_args()
    get_video_info(args.video_directory, args.sort)

if __name__ == "__main__":
    main()
