from .xml import RekordboxXml

from .track_utils import (
    remove_marks_from_track,
    remove_tempos_except_first,
    add_cue_points,
    find_drop_mark,
    get_tracks_from_playlist
)

from .cue_points import cue_points, drop_mark_num

def process_collection_xml(
    path,
    selected_playlists=None,
    remove_existing_marks=True,
    retain_first_tempo=True,
):
    """
    Process a Rekordbox collection XML file.

    Args:
        path (str): The path to the Rekordbox collection XML file.
        selected_playlists (list): A list of playlist names to process.
                                   If None, all tracks will be processed.
        remove_existing_marks (bool): If True, removes all existing marks
                                      from the track before processing.
        retain_first_tempo (bool): If True, retains the first tempo and
                                   removes all other tempos from the track.

    Returns:
        None
    """
    xml = RekordboxXml(path)

    if selected_playlists:
        tracks = []

        for playlist_name in selected_playlists:
            playlist = xml.get_playlist(playlist_name)
            tracks += get_tracks_from_playlist(playlist, xml)
    else:
        tracks = xml.get_tracks()

    for track in tracks:
        drop_mark = find_drop_mark(track.marks, drop_mark_num)

        if remove_existing_marks:
            remove_marks_from_track(track)
        if retain_first_tempo:
            remove_tempos_except_first(track)

        if drop_mark:
            add_cue_points(track, drop_mark, cue_points)

    xml.save(path) 
