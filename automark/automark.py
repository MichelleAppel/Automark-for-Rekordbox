from pyrekordbox.xml import RekordboxXml

from .track_utils import (
    remove_marks_from_track,
    remove_tempos_except_first,
    add_cue_points,
    find_drop_mark,
    get_tracks_from_playlist
)

from .cue_points import cue_points

def process_collection_xml(path, selected_playlists=None):
    xml = RekordboxXml(path)

    if selected_playlists:
        tracks = []

        for playlist_name in selected_playlists:
            playlist = xml.get_playlist(playlist_name)
            tracks += get_tracks_from_playlist(playlist, xml)
    else:
        tracks = xml.get_tracks()

    for track in tracks:
        drop_mark = find_drop_mark(track.marks)

        if drop_mark:
            remove_marks_from_track(track)
            remove_tempos_except_first(track)
            add_cue_points(track, drop_mark, cue_points)

    xml.save(path)
