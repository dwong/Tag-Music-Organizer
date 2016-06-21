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

    def testExtraMix(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('Say Something (ft Someone) [Radio Edit]')
        self.assertEqual('[Radio Edit]', extra)
        
    def testCommaArtist(self):
        artists = TagMusicOrganizer.splitFeaturedArtist('Crosby, Stills, Nash & Young')
        self.assertEqual(artists, None)

    def testFeaturedWithAmpersand(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('How Did We Get Here ft Andy Mineo & JGivens')
        self.assertEqual('Andy Mineo & JGivens', ft)
