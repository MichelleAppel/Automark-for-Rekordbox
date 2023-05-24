import argparse
from automark.automark import process_collection_xml
from automark.cue_points import cue_points, drop_mark_num

def main():
    parser = argparse.ArgumentParser(description="Automatically add cue points to Rekordbox collection XML.")
    parser.add_argument("path", help="Path to Rekordbox collection XML file.")
    parser.add_argument("--playlists", default="", help="Comma-separated list of playlists to edit. Leave empty to process all tracks.")
    args = parser.parse_args()

    selected_playlists = args.playlists.split(",") if args.playlists else None

    process_collection_xml(
        args.path,
        selected_playlists,
        remove_existing_marks=True,
        retain_first_tempo=True,
        drop_mark_num=drop_mark_num,
        cue_points=cue_points
        )

if __name__ == "__main__":
    main()
