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
    - "type": The cue type ("cue" for hot cues, "cue" for memory cues, "loop" for loop cues)
    - "length": The length of the loop in beats (only for loop cues)
"""

# Drop mark number (3 is D in rekordbox)
drop_mark_num = 3

# Hot cue points
hot_cue_points = [
    {"name": "drop hot cue", "beats": 0, "num": 3, "type": "cue"},
    {"name": "-32 hot cue", "beats": -32, "num": 2, "type": "cue"},
    {"name": "-64 hot cue", "beats": -64, "num": 1, "type": "cue"},
    {"name": "-128 hot cue", "beats": -128, "num": 0, "type": "cue"},
]

# Memory cue points: intervals of 64 beats before the drop from 0 to 576
memory_cue_points = [{"name": f"{-i} memory cue", "beats": -i, "num": -1, "type": "cue"} for i in range(0, 577, 64)]

# Loop cue points. Loops need a length in beats.
loop_cue_points = [
    {"name": "-64 loop", "beats": -64, "length": 64, "num": 4, "type": "loop"},
    {"name": "-128 loop", "beats": -128, "length": 64, "num": 5, "type": "loop"},
    {"name": "-192 loop", "beats": -192, "length": 64, "num": 6, "type": "loop"},
    {"name": "-256 loop", "beats": -256, "length": 64, "num": 7, "type": "loop"},
]

# Combine hot cue points, memory cue points, and loop cue points
cue_points = hot_cue_points + memory_cue_points # + loop_cue_points
