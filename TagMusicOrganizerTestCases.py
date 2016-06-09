import TagMusicOrganizer
import unittest

class TagMusicOrganizerTestCase(unittest.TestCase):
    def testSimpleFeaturedArtist(self):
        artists = TagMusicOrganizer.splitFeaturedArtist('Josh Garrels')
        self.assertEqual(artists, None)
        
    def testFeaturedInTitle(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('We Don\'t (feat. R. Swift)')
        self.assertEqual('R. Swift', ft)
        
    def testCommaArtist(self):
        artists = TagMusicOrganizer.splitFeaturedArtist('Crosby, Stills, Nash & Young')
        self.assertEqual(artists, None)

    def testFeaturedArtistInTitle(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('We Don\'t (feat. R. Swift)')
        self.assertEqual(ft, 'R. Swift')
