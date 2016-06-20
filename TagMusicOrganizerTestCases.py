import TagMusicOrganizer
import unittest

class TagMusicOrganizerTestCase(unittest.TestCase):
    def testSimpleFeaturedArtist(self):
        artists = TagMusicOrganizer.splitFeaturedArtist('Josh Garrels')
        self.assertEqual(artists, None)
        
    def testFeaturedInTitleWithParenthesis(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('We Don\'t (feat. R. Swift)')
        self.assertEqual('R. Swift', ft)

    def testFeaturedInTitleNoParenthesis(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('Daywalkers ft Lecrae')
        self.assertEqual('Lecrae', ft)
        
    def testFeaturedInTitleNoParenthesisFullWord(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('Fantasy featuring O.D.B.')
        self.assertEqual('O.D.B.', ft)

    def testCommaArtist(self):
        artists = TagMusicOrganizer.splitFeaturedArtist('Crosby, Stills, Nash & Young')
        self.assertEqual(artists, None)
