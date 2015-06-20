# TagMusicOrganizer.py
#
# Parse id3 tags for mp3
# Put into target directory with the format
#
# Artist/
#   Album/
#     NN. Artist - Title

import sys
import os
import eyed3
import glob
import argparse
import re

def splitFeaturedArtist(string_to_check):
    match = re.match('(.*)\[\( ]f(?:ea)?t.?(?:uring)? *([a-z0-9 &-_+]*)\)?(\(.*\))?',
                     string_to_check, re.IGNORECASE)
    if match:
        print('Found featured artist in: ' + string_to_check)
        return match.group(1), match.group(2), match.group(3)
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(debug=False,
                        source='/Users/derek/Desktop/',
                        target='/Users/derek/Music/Downloaded/',
                        manual_artist=''
                        )
    parser.add_argument('-src', '-in', dest='source', help='Source directory')
    parser.add_argument('-dst', '-out', dest='target', help='Target directory')
    parser.add_argument('-d', '--debug', dest='debug', help='Debug mode (dry run)',
                        action='store_true')
    parser.add_argument('-artist', dest='manual_artist', help='Force artist directory (e.g., Various)')

    args = vars(parser.parse_args())
    source = args['source']
    target = args['target']
    debug = args['debug']
    manual_artist = args['manual_artist']

    # Open files
    files = []
    if os.path.isfile(source):
        files.append(source)
    elif os.path.isdir(source):
        for f in glob.glob(os.path.dirname(source) + '/*.mp3'):
            files.append(f)

    for f in files:
        print('reading: ' + f)
        audio_file = eyed3.load(f)
        artist = audio_file.tag.artist
        title = audio_file.tag.title
        album = audio_file.tag.album
        track_number, total_tracks = audio_file.tag.track_num

        if album is None:
            album = 'Untitled'
        if track_number is None:
            track_number = 1

        # Check for ft, feat, etc in artist name
        artists = splitFeaturedArtist(artist)
        featured_artist = None
        if artists:
            print(artists)
            artist, featured_artist, extra = artists
            if extra:
                featured_artist += extra

        artist = artist.strip()

        split_title = splitFeaturedArtist(title)
        extra_title = None
        if split_title:
            title, featured_artist, extra_title = split_title
            
        title = title.strip().replace('/', '-')
        if featured_artist:
            featured_artist = featured_artist.strip()
        
        # Output to target directory as Artist/Album/NN. Artist - Song.mp3
        artist_folder = manual_artist if manual_artist else artist
        path = target + '/' + artist_folder + '/' + album + '/'
        rename = (('%02d' % track_number) + '. ' + artist + ' - ' + title +
                  (' (ft. ' + featured_artist + ')' if featured_artist else '') +
                  (' ' + extra_title if extra_title else ''))
        print('Output path: ' + path)
        try:
            os.makedirs(path)
            print('Made directory')
        except OSError as exc:
            if os.path.isdir(path):
                pass
            else:
                raise
        print('Output name: ' + rename)
        if not debug:
            audio_file.rename(path + rename)
