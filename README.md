# Automark for Rekordbox

Automark for Rekordbox is a Python script that automates the process of adding cue points to your Rekordbox collection XML file. The script reads the XML file and adds cue points to the tracks based on a set of predefined rules. The cue points are added before the drop, which must be manually selected in Rekordbox.

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

This will process all tracks in the XML file and add the cue points based on the predefined rules.

You can also specify a comma-separated list of playlists to edit by using the `--playlists` option:

```bash
python main.py path/to/rekordbox.xml --playlists "Playlist 1,Playlist 2"
```

This will only process the tracks in the specified playlists.

## Cue points

The cue points are defined in `cue_points.py` and consist of two lists: `hot_cue_points` and `memory_cue_points`. The hot cue points correspond to the buttons on the controller labeled A-H and have values between 0-7. The memory cue points have a value of -1.

To create a custom cue point, add a dictionary with the following keys to the appropriate list:

-   "name": A descriptive name for the cue point (e.g., "32 pre")
-   "beats": The number of beats relative to the drop (e.g., -32 for 32 beats before the drop)
-   "num": The cue number (0-7 for hot cues, -1 for memory cues)

Note that the cue points are added before the drop and must be manually selected in Rekordbox. The script only adds cue points when there is already a drop marker set, and the tempo and location of the drop marker must be correct before running the script.

## Workflow

The recommended workflow for using this script is as follows:

1.  In Rekordbox, export your collection to an XML file (File > Export Collection).
2.  Run the script on the XML file using the command line as described above.
3.  In Rekordbox, make sure that your XML file is loaded in rekordbox xml tab. Settings for this are in Preferences > Advanced > rekordbox xml > Imported Library.
4.  To update the tags for the tracks in a specific playlist, select all the tracks in the playlist and drag them into your local playlist. This will update the tags for the tracks and add any new cue points that were added by the script. Press "Skip" to skip importing any duplicate tracks.

Please note that the script does not modify your original Rekordbox library directly. Instead, it creates a modified copy of your library in the form of an XML file, which you can import back into Rekordbox.

## Contributing

Contributions are always welcome! If you find any bugs or issues with the script, please open an issue in the repository. If you would like to contribute to the code, please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code for personal or commercial purposes. Please see the `LICENSE` file for more information.
