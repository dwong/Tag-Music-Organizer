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

    def testManualArtistInArtists(self):
        featured = TagMusicOrganizer.removeArtistFromList('Andy Mineo,Mali Music', 'Andy Mineo')
        self.assertEqual('Mali Music', featured)

    def testNoneManualArtist(self):
        featured = TagMusicOrganizer.removeArtistFromList('Andy Mineo,Mali Music', None)
        self.assertEqual(None, featured)

    def testManualArtistInMiddle(self):
        featured = TagMusicOrganizer.removeArtistFromList('Lecrae,Andy Mineo,Mali Music', 'Andy Mineo')
        self.assertEqual(featured, 'Lecrae,Mali Music')

if __name__ == '__main__':
    unittest.main()        

