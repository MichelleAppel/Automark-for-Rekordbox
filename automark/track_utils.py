from pyrekordbox.xml import PositionMark, Tempo

def add_mark_to_track(track, Name, Type, Start, End, Num):
    ''' Add a mark to a track. 
    
        Args:
            track (pyrekordbox.Track): The track to add the mark to.
            Name (str): The name of the mark.
            Type (str): The type of the mark.
            Start (float): The start position of the mark in seconds.
            End (float): The end position of the mark in seconds.
            Num (int): The number of the mark.
        
        Returns:
            pyrekordbox.PositionMark: The mark that was added to the track.
    '''
    mark = PositionMark(parent=track._element, Name=Name, Type=Type, Start=Start, End=End, Num=Num)
    track.marks.append(mark)
    return mark

def remove_marks_from_track(track):
    ''' Remove all marks from a track.
    
        Args:
            track (pyrekordbox.Track): The track to remove the marks from.
            
        Returns:
            None        
    '''
    for mark in track.marks[:]:
        track._element.remove(mark._element)
        track.marks.remove(mark)

def remove_tempos_except_first(track):
    ''' Remove all tempos from a track except the first one.

        Args:
            track (pyrekordbox.Track): The track to remove the tempos from.

        Returns:
            None
    '''
    for tempo in track.tempos[1:]:
        track._element.remove(tempo._element)
        track.tempos.remove(tempo)

def find_drop_mark(marks):
    ''' Find the drop mark in a track.

        Args:
            track (pyrekordbox.Track): The track to find the drop mark in.

        Returns:
            pyrekordbox.PositionMark: The drop mark if it was found, otherwise None.
    '''
    for mark in marks:
        if mark["Num"] == 3:
            return mark
    return None

def calculate_position_in_seconds(position_in_bars, tempo):
    ''' Calculate the position in seconds from the position in bars and the tempo.

        Args:
            position_in_bars (float): The position in bars.
            tempo (pyrekordbox.Tempo): The tempo.

        Returns:
            float: The position in seconds.
    '''
    return position_in_bars * (60 / tempo)

def add_cue_points(track, drop_mark, cue_points, cue_type="cue"):
    ''' Add cue points to a track.

        Args:
            track (pyrekordbox.Track): The track to add the cue points to.
            drop_mark (pyrekordbox.PositionMark): The drop mark.
            cue_points (list): A list of cue points to add to the track.
            cue_type (str): The type of the cue points to add to the track.

        Returns:
            None
    '''
    position_in_seconds = drop_mark['Start']
    tempo = track.tempos[0]['Bpm']
    position_in_bars = position_in_seconds / (60 / tempo)

    for cp in cue_points:
        position_in_bars_cp = position_in_bars + cp["beats"]  # Updated to use + instead of -
        position_in_seconds_cp = position_in_bars_cp * (60 / tempo)

        if position_in_seconds_cp > 0:
            add_mark_to_track(track, Name=cp["name"], Type=cue_type, Start=position_in_seconds_cp, End=None, Num=cp["num"])


def get_tracks_from_playlist(playlist_node, rb_xml):
    """
    Get track objects from a playlist node.

    Args:
        playlist_node (Node): The playlist node from which to extract the tracks.
        rb_xml (RekordboxXml): The Rekordbox XML object containing the tracks database.

    Returns:
        list: A list of track objects from the playlist node.
    """
    track_keys = playlist_node.get_tracks()
    track_objects = []

    for key in track_keys:
        track_object = rb_xml.get_track(TrackID = key)
        track_objects.append(track_object)

    return track_objects
