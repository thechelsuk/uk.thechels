import pathlib
import helper

SOURCE = "https://www.youtube.com/feeds/videos.xml?channel_id=UCwK4oZ8hw9RS6tZKEjw_qLw"
OUTPUT_FILE = "./_data/videos.yml"

if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        output_file = root / OUTPUT_FILE
        existing_videos = helper.load_videos_file(output_file)
        merged_videos = helper.merge_videos(existing_videos,
                                            helper.get_videos(SOURCE))
        helper.save_videos(output_file, merged_videos)
        print("Videos completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
