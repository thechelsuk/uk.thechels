import csv
import config
# File paths

SOURCE_CSV = config.SUB_CSV_FILE
OUTPUT_OPML = config.SUB_OPML_FILE


def main():

    csv_data = []
    try:
        with open(SOURCE_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_data.append(row)
    except FileNotFoundError:
        print(f"Error: Source file not found at {SOURCE_CSV}")
        return
    except Exception as e:
        print(f"An error occurred while reading CSV: {e}")
        return

    opml_outlines = []

    for entry in csv_data:
        channel_id = entry.get('Channel ID')
        name = entry.get('Channel title')

        if channel_id and name:
            feedurl = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

            outline_item = f'  <outline text="YT - {name}" title="YT - {name}" type="rss" xmlUrl="{feedurl}" />'
            opml_outlines.append(outline_item)

    # Write OPML file
    opml_header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<opml version="2.0">\n'
        '  <head>\n'
        '    <title>YouTube Channels</title>\n'
        '  </head>\n'
        '  <body>\n'
        '    <outline text="8 - YouTube" title="8 - YouTube" type="folder">\n')
    opml_footer = '\n</outline>\n</body>\n</opml>\n'
    with open(OUTPUT_OPML, 'w', encoding='utf-8') as f:
        f.write(opml_header)
        for outline in opml_outlines:
            f.write(f'    {outline}\n')
        f.write(opml_footer)


if __name__ == "__main__":
    main()
