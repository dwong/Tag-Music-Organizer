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
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.dirname(os.path.realpath(__file__)) + '/env.cfg'))
default_source = config.get('env', 'source')
default_target = config.get('env', 'target')
debug = False

def splitFeaturedArtist(string_to_check):
    match = re.match('([^\(]*)?[\( ]*(?:f(?:ea)?t[\.]?(?:uring)?) *([a-z0-9\.\ &-]*)[\)\( ]?(.*)?',
                     string_to_check, re.IGNORECASE)
    if debug:
        if match:
            print('Found featured artist in: "%s"' % string_to_check)
        else:
            print('No featured artist in "%s"' % string_to_check)
    if match:
        if debug:
            print('artist: %s, featured artist: %s, extra: %s' % (match.group(1), match.group(2), match.group(3)))
        return match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(debug=False,
                        source=default_source,
                        target=default_target,
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

    if debug:
        print('Source: %s\nTarget: %s' % (source, target))
        
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
        artist = manual_artist if manual_artist else audio_file.tag.artist
        title = audio_file.tag.title
        album = audio_file.tag.album
        track_number, total_tracks = audio_file.tag.track_num
        featured_artist = None

        if album is None:
            album = 'Untitled'
        if track_number is None:
            track_number = 1

        # Check for ft, feat, etc in artist name
        if debug:
            print('checking id3 artist tag')
        artists = splitFeaturedArtist(artist)
        if artists:
            artist, featured_artist, extra = artists

        artist = artist.strip()

        if debug:
            print('checking id3 title tag')
        split_title = splitFeaturedArtist(title)
        extra_title = None
        if split_title:
            title, featured_artist, extra_title = split_title
        title = title.strip().replace('/', '-')
        if featured_artist:
            featured_artist = featured_artist.replace(')', '')
            
        
        # Output to target directory as Artist/Album/NN. Artist - Song.mp3
        artist_folder = artist

        # Ensure valid characters in path
        artist_folder = artist_folder.replace('/', '-')
        album = album.replace('/', '-')

        # Construct output path
        path = target + '/' + artist_folder + '/' + album + '/'
        track_number = ('%02d' % track_number)
        featured_artist_output = ' (ft. ' + featured_artist + ')' if featured_artist else ''
        if debug:
            print('featured artist string: %s' % featured_artist_output)
        extra_title = ' ' + extra_title if extra_title else ''
        rename = (track_number + '. ' + artist + ' - ' + title +
                  featured_artist_output + extra_title)
        print('Output path: ' + path)
        if debug:
            print('Would have made directory')
        else:
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
