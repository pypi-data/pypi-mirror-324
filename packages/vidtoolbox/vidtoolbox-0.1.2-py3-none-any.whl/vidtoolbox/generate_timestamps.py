import os
import argparse
import subprocess

def format_duration(seconds):
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def create_file_list(video_directory):
    """Retrieve video files and display the order for user confirmation."""
    files = sorted([f for f in os.listdir(video_directory) if f.endswith('.mp4')])

    print("\n📌 The chapter timestamps will use the following video order:")
    for index, file in enumerate(files, start=1):
        print(f"  {index}. {file}")

    confirm = input("\n✅ Confirm the order? (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ Timestamp generation canceled!")
        return None
    return files

def generate_timestamps(video_directory):
    """Generate YouTube chapter timestamps based on video durations."""
    files = create_file_list(video_directory)
    if files is None:
        return

    timestamps = []
    total_time = 0  # Accumulated time

    for file in files:
        file_path = os.path.join(video_directory, file)

        # Get video duration
        cmd_duration = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'format=duration', '-of', 'csv=p=0',
            file_path
        ]
        duration = float(subprocess.check_output(cmd_duration).decode().strip())

        # Format time
        timestamp = format_duration(total_time)
        chapter_name = os.path.splitext(file)[0]  # Remove .mp4 extension
        timestamps.append(f"{timestamp} - {chapter_name}")

        # Update accumulated time
        total_time += duration

    # Default filename is the folder name
    folder_name = os.path.basename(os.path.normpath(video_directory))
    output_timestamps = os.path.join(video_directory, f"{folder_name}.txt")

    # Write to `timestamps.txt`
    with open(output_timestamps, "w", encoding="utf-8") as f:
        f.write("\n".join(timestamps))

    print(f"\n✅ YouTube chapter timestamps generated: {output_timestamps}")

def display_timestamps(video_directory):
    """Read and display the content of timestamps.txt."""
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if not os.path.exists(timestamps_path):
        print("\n❌ `timestamps.txt` not found. Please make sure it has been generated.")
        return False

    print("\n📌 Here are the chapter timestamps:")
    with open(timestamps_path, "r", encoding="utf-8") as f:
        print(f.read())  # Display content directly

    return True

def main():
    parser = argparse.ArgumentParser(description="Generate YouTube chapter timestamps")
    parser.add_argument("video_directory", help="Directory containing video files")
    
    args = parser.parse_args()
    generate_timestamps(args.video_directory)

if __name__ == "__main__":
    main()