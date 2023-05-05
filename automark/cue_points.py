"""
This file allows you to customize the cue points for your tracks.
To adjust the cue points, you can modify the hot_cue_points and memory_cue_points lists.
You can also create your own lists and combine them to create a custom set of cue points.

Hot cues have num values between 0-7, which correspond to the buttons on the controller labeled A-H.
Memory cues have num values of -1.

To create a custom cue point, add a dictionary with the following keys to the appropriate list:
    - "name": A descriptive name for the cue point (e.g., "32 pre")
    - "beats": The number of beats relative to the drop (e.g., -32 for 32 beats before the drop)
    - "num": The cue number (0-7 for hot cues, -1 for memory cues)
"""

# Hot cue points
hot_cue_points = [
    {"name": "drop", "beats": 0, "num": 3},
    {"name": "32 pre", "beats": -32, "num": 2},
    {"name": "64 pre", "beats": -64, "num": 1},
    {"name": "128 pre", "beats": -128, "num": 0},
]

# Memory cue points
memory_cue_points = [{"name": f"{i} pre", "beats": -i, "num": -1} for i in range(0, 577, 64)]

# Combine hot cue points and memory cue points
cue_points = hot_cue_points + memory_cue_points
