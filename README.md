# Automark for Rekordbox

`Automark for Rekordbox` is a Python library that simplifies the process of adding custom markers to your Rekordbox playlists or entire library. The library comes with a set of predefined rules for placing markers around the drop, but it also allows users to define their own rules.

**⚠️ Warning:** This library uses `pyrekordbox`, which directly modifies your Rekordbox library. While we've made efforts to ensure the library's reliability, there's always a risk of data loss or corruption when working with third-party tools. Please make sure to **back up your Rekordbox library** before using this tool. Use at your own risk!

## Features

-   Automatically add markers around the drop (hotcue 'D') according to predefined rules:
    -   Hotcue 'A' 128 beats before the drop
    -   Hotcue 'B' 64 beats before the drop
    -   Hotcue 'C' 32 beats before the drop
    -   Memory cues every 64 beats before the drop until the beginning of the track
-   Easily customize or define your own rules for placing markers
-   Apply rules to specific playlists or the entire library

## Installation

1.  Ensure you have Python 3.6 or higher installed.
2.  Clone this repository or download the source code.
3.  Install the required dependencies using `pip`:

bash

`pip install -r requirements.txt`

## Usage

python

`from automark import automark  # Apply the default rules to a specific Rekordbox playlist automark.apply_rules_to_playlist(playlist_name="My Playlist")  # Apply the default rules to the entire Rekordbox library automark.apply_rules_to_library()`

To define your own rules, please refer to the `marker_rules.py` script and the examples provided.

## Contributing

We welcome contributions to the project. Feel free to submit issues, feature requests, or pull requests. Please follow the code style and structure outlined in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/c/LICENSE) file for more information.
