from .xml import PositionMark

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
    marks_to_remove = [mark for mark in track.marks]
    for mark in marks_to_remove:
        if mark._element in track._element:
            track._element.remove(mark._element)

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

def find_drop_mark(marks, drop_mark_num=3):
    ''' Find the drop mark in a track.

        Args:
            track (pyrekordbox.Track): The track to find the drop mark in.
            drop_mark_num (int): The number of the drop mark. Default is 3 (D in rekordbox).

        Returns:
            pyrekordbox.PositionMark: The drop mark if it was found, otherwise None.
    '''
    return next((mark for mark in marks if mark["Num"] == drop_mark_num), None)

def calculate_position_in_seconds(position_in_bars, tempo):
    ''' Calculate the position in seconds from the position in bars and the tempo.

        Args:
            position_in_bars (float): The position in bars.
            tempo (pyrekordbox.Tempo): The tempo.

        Returns:
            float: The position in seconds.
    '''
    return position_in_bars * (60 / tempo)

def calculate_position_in_bars(position_in_seconds, tempo):
    ''' Calculate the position in bars from the position in seconds and the tempo.

        Args:
            position_in_seconds (float): The position in seconds.
            tempo (pyrekordbox.Tempo): The tempo.

        Returns:
            float: The position in bars.
    '''
    return position_in_seconds / (60 / tempo)

def add_cue_points(track, drop_mark, cue_points):
    ''' Add cue points to a track.

        Args:
            track (pyrekordbox.Track): The track to add the cue points to.
            drop_mark (pyrekordbox.PositionMark): The drop mark.
            cue_points (list): A list of cue points to add to the track.

        Returns:
            None
    '''
    position_in_seconds = drop_mark['Start']
    tempo = track.tempos[0]['Bpm']
    position_in_bars = calculate_position_in_bars(position_in_seconds, tempo)

    for cp in cue_points:
        position_in_bars_cp = position_in_bars + cp["beats"]
        position_in_seconds_cp = position_in_bars_cp * (60 / tempo)

        if position_in_seconds_cp > 0:
            if cp["type"] == "loop":
                length = cp["length"]
                end = calculate_position_in_seconds(position_in_bars_cp + length, tempo)
            else:
                end = None
        
            add_mark_to_track(track, Name=cp["name"], Type=cp["type"], Start=position_in_seconds_cp, End=end, Num=cp["num"])


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
