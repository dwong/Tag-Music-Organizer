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

    def testFeaturedWithCommas(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('Streets of Philadelphia (feat. Mac the Doulos, Young Joshua, Ackdavis and R-Swift)')
        self.assertEqual('Mac the Doulos, Young Joshua, Ackdavis and R-Swift', ft)
        self.assertEqual('', extra)
        self.assertEqual('Streets of Philadelphia', artist)

    def testFeaturedWithApostrophe(self):
        artist, ft, extra = TagMusicOrganizer.splitFeaturedArtist('Missio Dei (feat. God\'s Servant)')
        self.assertEqual('God\'s Servant', ft)

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
        featured = TagMusicOrganizer.removeArtistsFromList('Andy Mineo,Mali Music', 'Andy Mineo')
        self.assertEqual('Mali Music', featured)

    def testNoneManualArtist(self):
        featured = TagMusicOrganizer.removeArtistsFromList('Andy Mineo,Mali Music', None)
        self.assertEqual(None, featured)

    def testManualArtistInMiddle(self):
        featured = TagMusicOrganizer.removeArtistsFromList('Lecrae,Andy Mineo,Mali Music', 'Andy Mineo')
        self.assertEqual(featured, 'Lecrae,Mali Music')

    def testRemoveArtistsFromArtists(self):
        featured = TagMusicOrganizer.removeArtistsFromList('Lecrae,Andy Mineo,Mali Music', 'Lecrae, Andy Mineo')
        self.assertEqual(featured, 'Mali Music')

    def testRemoveArtistsWithAndFromArtists(self):
        featured = TagMusicOrganizer.removeArtistsFromList('Lecrae,Andy Mineo,Mali Music', 'Lecrae and Andy Mineo')
        self.assertEqual(featured, 'Mali Music')

    def testNormalizeWithNone(self):
        self.assertEqual(None, TagMusicOrganizer.normalizeArtistList(None))

    def testFeaturedWithFtInName(self):
        ft = TagMusicOrganizer.splitFeaturedArtist('The Spinners - Leftover Tears')
        self.assertEqual(None, ft)

    def testFeaturedWithFtAtEnd(self):
        ft = TagMusicOrganizer.splitFeaturedArtist('A Gift')
        self.assertEqual(None, ft)        

if __name__ == '__main__':
    unittest.main()        

