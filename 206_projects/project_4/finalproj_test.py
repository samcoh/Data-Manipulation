from finalproj import *
import unittest
import sqlite3


init_db(DBNAME)
movie_theater = list_movietheaters("60022")[0]
#result = list_movietheaters("60022")[0]
mov = movie_information(movie_theater)[0]
movies = list_movietheaters("48104")
move = movie_information(movies[0])
#Please note: these tests only work if the data is coming from the cache.
#If the cache is deleted this information will be updated and the data represented in these tests will be incorrect.
class TestClasses(unittest.TestCase):
    def test_Theater_constructor(self):
        t1 = Theater(name ="AMC",url = "url",list_movies = ["Shark Movie", "Bad Mom"],street_address = "619 orchard",city = "Ann Arbor",state = "MI",zip ="48104")

        self.assertEqual(t1.theater_name, "AMC")
        self.assertEqual(t1.theater_url,"url" )
        self.assertEqual(t1.list_movies,["Shark Movie", "Bad Mom"])
        self.assertEqual(t1.street_address, "619 orchard")
        self.assertEqual(t1.city, "Ann Arbor")
        self.assertEqual(t1.state, "MI")
        self.assertEqual(t1.zip, "48104")

        self.assertIsInstance(t1, Theater)
    def test_Movie_constructor(self):
        m1 = Movie(name="Sammie", year="1998", time= "105", url="url", rating="PG", genre='Drama,Action', descrip= "Student at UM", directors= "Molly", num_directors= 5, stars= "l,m", num_stars=5, more_details_url="url2", gross = "gross", weekend="weekend", budget="Budget", cumulative = "Cumulative")
        self.assertEqual(m1.movie_name,"Sammie")
        self.assertEqual(m1.movie_year, "1998")
        self.assertEqual(m1.movie_time, "105")
        self.assertEqual(m1.movie_url,"url")
        self.assertEqual(m1.movie_rating, "PG")
        self.assertEqual(m1.movie_genre,'Drama,Action')
        self.assertEqual(m1.movie_descrip, "Student at UM")
        self.assertEqual(m1.movie_directors, "Molly")
        self.assertEqual(m1.movie_number_of_directors, 5)
        self.assertEqual(m1.movie_stars,"l,m" )
        self.assertEqual(m1.movie_number_of_stars, 5)
        self.assertEqual(m1.movie_more_details_url, "url2")
        self.assertEqual(m1.movie_gross_usa, "gross")
        self.assertEqual(m1.movie_opening_weekend_usa,"weekend")
        self.assertEqual(m1.movie_budget, "Budget" )
        self.assertEqual(m1.movie_worldwide_gross, "Cumulative")


        self.assertIsInstance(m1, Movie)
class TestHTMLFunctions(unittest.TestCase):
    def test_list_movietheaters(self):
        #result = list_movietheaters("60022")[0]

        self.assertEqual(movie_theater.theater_name, "AMC Northbrook Court 14")
        self.assertEqual(movie_theater.street_address,  "1525 Lake Cook Road")
        self.assertEqual(movie_theater.city, "Northbrook")
        self.assertEqual(movie_theater.state, "IL")
        self.assertEqual(movie_theater.zip, "60062")
        self.assertEqual(movie_theater.list_movies,[
        'A Quiet Place ', 'A Wrinkle in Time ', 'Black Panther ', 'Blockers ',
         'Chappaquiddick ', 'Game Night ', "God's Not Dead: A Light in Darkness ",
         'Isle of Dogs ', 'Love, Simon ', 'Midnight Sun ', 'Pacific Rim: Uprising ',
          'Paul, Apostle of Christ ', 'Peter Rabbit ', 'Ready Player One ', 'Red Sparrow ',
           'Sherlock Gnomes ', 'The Death of Stalin ', 'The Greatest Showman ',
            'The Miracle Season ', 'Tomb Raider ', 'Acrimony ', 'Unsane '
            ])
    def test_movie_information(self):
        # result = list_movietheaters("60022")[0]
        # mov = movie_information(result)[0]
        self.assertEqual(mov.movie_name, "A Quiet Place ")
        self.assertEqual(mov.movie_genre, "Drama,Horror,Thriller")
        self.assertEqual(mov.movie_stars, "Emily Blunt,John Krasinski,Noah Jupe,Millicent Simmonds")
        self.assertEqual(mov.movie_directors,"John Krasinski")
        self.assertEqual(mov.movie_year, "2018")
        self.assertEqual(mov.movie_time, "90")
        self.assertEqual(mov.movie_rating, "PG-13")
        self.assertEqual(mov.movie_number_of_stars, 4)
        self.assertEqual(mov.movie_number_of_directors, 1)


class TestDatabase(unittest.TestCase):
    #tests to make sure that my theater table is properly constructed
    #also tests to see if the table can satify queries that are necessary for my program
    def test_Theaters_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        #init_db(DBNAME)
        # movies = list_movietheaters("48104")
        # mov = movie_information(movies[0])

        sql = 'SELECT Name FROM Theaters'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Goodrich Quality 16',), result_list)
        self.assertEqual(len(result_list), 79)

        sql = '''
            SELECT Id, EnteredZipCode, Name,
                   StreetAddress,City,State, ZipCode, MoviesPlaying
            FROM Theaters
            WHERE City = "Ann Arbor"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 3)
        self.assertEqual(result_list[0][3], "3686 Jackson Road")

        conn.close()

    #tests to make sure that my theater table is properly constructed
    #also tests to see if the table can satify queries that are necessary for my program
    def test_Movies_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT Id, Name, ReleaseYear, Minutes, Rating,
                   Genre,Directors,NumberOfDirectors,Stars,NumberOfStars,Budget,
                   GrossProfitUSA,OpeningWeekendUSA, CumulativeWorldwideGross
            FROM Movies
        '''
        results =cur.execute(sql).fetchall()
        self.assertEqual(len(results[0]),14)
        sql = '''
            SELECT Id
            FROM Movies
            WHERE Name = "A Quiet Place "
            LIMIT 1
        '''
        results = cur.execute(sql)
        for x in results:
            results = x[0]
        self.assertEqual(results, 1)
        sql = '''
            SELECT Name
            FROM Movies
            WHERE Minutes = "90"
        '''
        result_list = cur.execute(sql).fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 1)

        sql = '''
            SELECT COUNT(*)
            FROM Movies
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 25)

        conn.close()

class TestDataProcessing(unittest.TestCase):
    def test_general_info_from_plot_functions(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT MoviesPlaying
            FROM Theaters
            WHERE Name = "Goodrich Quality 16" AND StreetAddress = "3686 Jackson Road"
        '''
        cur.execute(sql)
        for x in cur:
            results = x
        self.assertEqual(results,("1,2,23,3,4,5,24,6,25,8,9,10,11,12,14,15,16,17,20,21,22",))

        statement = '''
            SELECT Budget,CumulativeWorldwideGross,Name
            FROM Movies
            WHERE Id = "2"
        '''
        result_list = cur.execute(statement).fetchall()
        self.assertEqual(result_list,[('103,000,000', '106,564,863', 'A Wrinkle in Time ')])
unittest.main()
