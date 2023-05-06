# Automark for Rekordbox

Automark for Rekordbox is a Python script that automates the process of adding cue points to your Rekordbox collection XML file. The script reads the XML file and adds cue points to the tracks based on a customizable set of rules. The cue points are added relative to the drop, which must be manually marked in Rekordbox.

## Installation

To use the script, first install the required dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Running the script

To run the script from the command line, navigate to the directory containing the script and run the following command:

```bash
python main.py path/to/rekordbox.xml
```

This will process all tracks in the XML file and add the cue points and loops based on the customized rules.

You can also specify a comma-separated list of playlists to edit by using the `--playlists` option:

```bash
python main.py path/to/rekordbox.xml --playlists "Playlist 1,Playlist 2"
```

This will only process the tracks in the specified playlists.

## Customizing Cue Points and Loops

The cue points and loops are defined in `cue_points.py`. You can customize the cue points by modifying the `hot_cue_points`, `memory_cue_points`, and `loop_cue_points` lists. You can also create your own lists and combine them to create a custom set of cue points and loops.

To create a custom cue point or loop, add a dictionary with the following keys to the appropriate list:

-   "name": A descriptive name for the cue point or loop (e.g., "32 pre")
-   "beats": The number of beats relative to the drop (e.g., -32 for 32 beats before the drop)
-   "num": The cue number (0-7 for hot cues, -1 for memory cues)
-   "type": The cue type ("cue" for hot cues and memory cues, "loop" for loop cues)
-   "length": The length of the loop in beats (only for loop cues)

Please note that the cue points and loops are added relative to the drop, which must be manually marked in Rekordbox. The script only adds cue points and loops when there is already a drop marker set, and the tempo and location of the drop marker must be correct before running the script.

## Customizing Drop Marker Number

By default, the script uses the hot cue labeled "D" in Rekordbox (represented by the number 3) as the drop marker. However, you can customize the drop marker number by modifying the `drop_mark_num` variable in `cue_points.py`. Set it to the desired hot cue number that corresponds to your preferred drop marker (e.g., 0 for A, 1 for B, 2 for C, etc.).

Please note that you need to manually set the drop marker in Rekordbox for each track, and the script will only add cue points and loops relative to the selected drop marker.

## Workflow

The recommended workflow for using this script is as follows:

1.  In Rekordbox, export your collection to an XML file (File > Export Collection).
2.  Run the script on the XML file using the command line as described above.
3.  In Rekordbox, make sure that your XML file is loaded in the rekordbox xml tab. Settings for this are in Preferences > Advanced > rekordbox xml > Imported Library.
4.  To update the tags for the tracks in a specific playlist, select all the tracks in the playlist and drag them into your local playlist. This will update the tags for the tracks and add any new cue points and loops that were added by the script. Press "Skip" to skip importing any duplicate tracks.

Please note that the script does not modify your original Rekordbox library directly. Instead, it creates a modified copy of your library in the form of an XML file, which you can import back into Rekordbox.

## Contributing
Contributions are always welcome! If you find any bugs or issues with the script, please open an issue in the repository. If you would like to contribute to the code, please feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code for personal or commercial purposes. Please see the `LICENSE` file for more information.
