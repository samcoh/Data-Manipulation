import unittest
import proj1_w18 as proj1
import json

f = open('sample_json.json', 'r')
data= json.load(f)
f.close()
class TestMedia(unittest.TestCase):
    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        #added starting below...
        self.assertEqual(m2.year, "No Release Year")
        m3 = proj1.Media("1999", "Prince", "Twenty-Seventeen")

        self.assertEqual(m3.year, "Twenty-Seventeen")

        #checking to see if they are instances of media
        self.assertIsInstance(m1, proj1.Media)
        self.assertIsInstance(m2, proj1.Media)
        self.assertIsInstance(m3, proj1.Media)
    def testMedia__str__(self):
        m = proj1.Media()
        m1 = proj1.Media("Bridget Jones's Diary (Unabridged)", "Helen Fielding", 2012)

        self.assertEqual(m.__str__(), "No Title by No Author (No Release Year)")
        self.assertEqual(m1.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
    def testMedia__len__(self):
        m = proj1.Media("Bridget Jones's Diary (Unabridged)", "Helen Fielding", 2012)

        self.assertEqual(len(m), 0)

class TestSong(unittest.TestCase):
    def testSongConstructorInherits(self):
        m = proj1.Song()
        m1 = proj1.Song("Single Ladies", "Beyonce", 2008, 191, "I Am...Sasha Fierce", "Contemporary R&B")

        self.assertIsInstance(m, proj1.Song)

        self.assertEqual(m.title, "No Title")
        self.assertEqual(m.author, "No Author")
        self.assertEqual(m.year, "No Release Year")

        self.assertEqual(m1.title, "Single Ladies")
        self.assertEqual(m1.author, "Beyonce")
        self.assertEqual(m1.year, 2008)
    def testSongNotInstanceofMedia(self):
        m1 = proj1.Song("Single Ladies", "Beyonce", 2008, 191, "I Am...Sasha Fierce", "Contemporary R&B")

        self.assertNotIsInstance(m1.tracklen, proj1.Media)
        self.assertNotIsInstance(m1.album, proj1.Media)
        self.assertNotIsInstance(m1.genre, proj1.Media)
    def testSongConstructorAdditions(self):
        m= proj1.Song()
        m1 = proj1.Song("Single Ladies", "Beyonce", 2008, 191, "I Am...Sasha Fierce", "Contemporary R&B")

        self.assertEqual(m.tracklen, "No Track Length")
        self.assertEqual(m.album, "No Album")
        self.assertEqual(m.genre, "No Genre")

        self.assertEqual(m1.tracklen, 191)
        self.assertEqual(m1.album, "I Am...Sasha Fierce")
        self.assertEqual(m1.genre, "Contemporary R&B")
    def testSong__str__(self):
        m = proj1.Song()
        m1 = proj1.Song(title = "Hey Jude", author = "The Beatles", release_year = 1968, genre= "Rock")

        self.assertEqual(m.__str__(), "No Title by No Author (No Release Year) [No Genre]")
        self.assertEqual(m1.__str__(),"Hey Jude by The Beatles (1968) [Rock]")
    def testSong__len__(self):
        m = proj1.Song("Single Ladies", "Beyonce", 2008, 191, "I Am...Sasha Fierce", "Contemporary R&B")
        m1= proj1.Song("Single Ladies", "Beyonce", 2008, 180, "I Am...Sasha Fierce", "Contemporary R&B")

        self.assertEqual(len(m), 191)
        self.assertEqual(len(m1), 180)

class TestMovie(unittest.TestCase):
    def testMovieConstructorInherits(self):
        m = proj1.Movie()
        m1 = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 122.4)

        self.assertIsInstance(m, proj1.Movie)
        self.assertIsInstance(m1, proj1.Movie)

        self.assertEqual(m.title, "No Title")
        self.assertEqual(m.author, "No Author")
        self.assertEqual(m.year, "No Release Year")

        self.assertEqual(m1.title, "Jaws")
        self.assertEqual(m1.author, "Steven Speilberg")
        self.assertEqual(m1.year, 1975)
    def testMovieConstructorAdditions(self):
        m = proj1.Movie()
        m1 = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 122.4)

        self.assertEqual(m.rating, 'No Rating')
        self.assertEqual(m.movielen, "No Movie Length")

        self.assertEqual(m1.rating, 'PG')
        self.assertEqual(m1.movielen, 122.4)
    def testMovieNotInstanceofMediaorSong(self):
        m = proj1.Movie()
        m1 = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 122.4)

        self.assertNotIsInstance(m.rating, proj1.Media)
        self.assertNotIsInstance(m.movielen, proj1.Media)
        self.assertNotIsInstance(m.rating, proj1.Song)
        self.assertNotIsInstance(m.movielen, proj1.Song)
    def testMovie__str__(self):
        m = proj1.Movie()
        m1 = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 122.4)

        self.assertEqual(m.__str__(), "No Title by No Author (No Release Year) [No Rating]")
        self.assertEqual(m1.__str__(), "Jaws by Steven Speilberg (1975) [PG]")
    def testMovie__len__(self):
        m = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 179.4)
        m1 = proj1.Movie("Jaws", "Steven Speilberg", 1975, "PG", 122.6)

        self.assertEqual(len(m), 179)
        self.assertEqual(len(m1), 123)

class TestMediaJson_Part2(unittest.TestCase):
    def test_json_Media_init(self):
        m = proj1.Media(json = data[2])
        self.assertEqual(m.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(m.author, "Helen Fielding")
        self.assertEqual(m.year, 2012)
    def test_json_Media_str(self):
        m= proj1.Media(json=data[2])
        self.assertEqual(m.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
    def test_json_Media_len(self):
        m = proj1.Media(json=data[2])
        self.assertEqual(len(m), 0)

class TestSongJson_Part2(unittest.TestCase):
    def test_json_Song_init(self):
        m = proj1.Song(json=data[1])
        self.assertEqual(m.title, "Hey Jude")
        self.assertEqual(m.author, "The Beatles")
        self.assertEqual(m.year, 1968)
        self.assertEqual(m.genre, "Rock")
        self.assertEqual(m.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(m.tracklen, 431.333)
    def test_json_Song_instancevariablerelevance(self):
        m = proj1.Song(json=data[1])
        self.assertNotIsInstance(m.album, proj1.Media)
        self.assertNotIsInstance(m.album, proj1.Movie)
        self.assertNotIsInstance(m.genre, proj1.Movie)
        self.assertNotIsInstance(m.genre, proj1.Media)
        self.assertNotIsInstance(m.tracklen, proj1.Media)
        self.assertNotIsInstance(m.tracklen, proj1.Movie)
    def test_json_Song_str(self):
        m= proj1.Song(json=data[1])
        self.assertEqual(m.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
    def test_json_Song_len(self):
        m=proj1.Song(json=data[1])
        self.assertEqual(len(m), 431)

class TestMovieJson_Part2(unittest.TestCase):
    def test_json_Movie_init(self):
        m = proj1.Movie(json=data[0])
        self.assertEqual(m.title, 'Jaws')
        self.assertEqual(m.author, "Steven Spielberg")
        self.assertEqual(m.year, 1975)
        self.assertEqual(m.movielen, 124.19091666666667)
        self.assertEqual(m.rating, "PG")
    def test_json_Movie_instancevariablerelevance(self):
        m = proj1.Movie(json=data[0])
        self.assertNotIsInstance(m.movielen, proj1.Song)
        self.assertNotIsInstance(m.movielen, proj1.Media)
        self.assertNotIsInstance(m.rating, proj1.Song)
        self.assertNotIsInstance(m.rating, proj1.Media)
    def test_json_Movie_str(self):
        m= proj1.Movie(json= data[0])
        self.assertEqual(m.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
    def test_json_Movie_len(self):
        m= proj1.Movie(json=data[0])
        self.assertEqual(len(m), 124)

class TestItunesApi_Part3(unittest.TestCase):
    def test_common_itunes_api(self):
        common_param= ("baby","love")
        common2_param = "baby"
        common3_param = "love"

        common = proj1.get_from_url(common_param)
        common2 = proj1.get_from_url(common2_param)
        common3 = proj1.get_from_url(common3_param)

        self.assertEqual(len(common), 20)
        self.assertEqual(len(common2), 20)
        self.assertEqual(len(common3), 20)
    def test_less_common_itunes_api(self):
        less_common = "moana"
        less_common2 = "helter skelter"

        m = proj1.get_from_url(less_common)
        m2 = proj1.get_from_url(less_common2)

        self.assertEqual(len(m), 20)
        self.assertEqual(len(m2), 20)
    def test_nonsense_itunes_api(self):
        nonsense_param = "doidsaofeinafqei"
        m2 = proj1.get_from_url(nonsense_param)
        self.assertEqual(len(m2), 0)
    def test_blank_param_itunes_api(self):
        blank_param = ""
        m3 = proj1.get_from_url(blank_param)
        self.assertEqual(len(m3), 0)
    def test_itunes_api_type(self):
        param = "Miley Cyrus"
        t = proj1.get_from_url(param)
        self.assertEqual(type(t), list)

unittest.main()
