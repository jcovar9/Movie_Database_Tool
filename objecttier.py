#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
    def __init__(self, _id, _title, _year):
        self._Movie_ID = _id
        self._Title = _title
        self._Release_Year = _year
    @property
    def Movie_ID(self):
        return self._Movie_ID
    @property
    def Title(self):
        return self._Title
    @property
    def Release_Year(self):
        return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie):
    def __init__(self, _id, _title, _year, _numRevs, _avgRates):
        Movie.__init__(self, _id, _title, _year)
        self._Num_Reviews = _numRevs
        self._Avg_Rating = _avgRates
    @property
    def Num_Reviews(self):
        return self._Num_Reviews
    @property
    def Avg_Rating(self):
        return self._Avg_Rating



##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails(MovieRating):
    def __init__(self, _id, _title, _date, _runtime, _lang, _budget, _revenue,
                 _numRevs, _avgRates, _tagline, _genres, _companies):
        MovieRating.__init__(self, _id, _title, _date[:4], _numRevs, _avgRates)
        self._Release_Date = _date
        self._Runtime = _runtime
        self._Original_Language = _lang
        self._Budget = _budget
        self._Revenue = _revenue
        self._Tagline = _tagline
        self._Genres = _genres
        self._Production_Companies = _companies
    @property
    def Release_Date(self):
        return self._Release_Date
    @property
    def Runtime(self):
        return self._Runtime
    @property
    def Original_Language(self):
        return self._Original_Language
    @property
    def Budget(self):
        return self._Budget
    @property
    def Revenue(self):
        return self._Revenue
    @property
    def Tagline(self):
        return self._Tagline
    @property
    def Genres(self):
        return self._Genres
    @property
    def Production_Companies(self):
        return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
    try:
        sql = """Select COUNT(*)
                From Movies"""
        row = datatier.select_one_row(dbConn, sql)
        return row[0]
    except:
        return -1
    


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    try:
        sql = """Select COUNT(*)
                From Ratings"""
        row = datatier.select_one_row(dbConn, sql)
        return row[0]
    except:
        return -1
   


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
    movies = []
    try:
        sql = """Select Movie_ID, Title, strftime('%Y', Release_Date)
                From Movies
                Where Title like ?
                Order by Title Asc"""
        rows = datatier.select_n_rows(dbConn, sql, [pattern])
        for row in rows:
            x = Movie(row[0], row[1], row[2])
            movies.append(x)
        return movies
    except:
        return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
    sql = "Select Movie_ID From Movies Where Movie_ID = ?"
    if datatier.select_one_row(dbConn, sql, [movie_id]) == ():
        return None
    try:
        sql = """Select Movies.Movie_ID, Title, Date(Release_Date), Runtime, 
                Original_Language, Budget, Revenue
                From Movies
                Where Movies.Movie_ID = ?"""
        minfo = datatier.select_one_row(dbConn, sql, [movie_id])
        sql = """Select Tagline From Movies
                Join Movie_Taglines on Movies.Movie_ID = Movie_Taglines.Movie_ID
                Where Movies.Movie_ID = ?"""
        taglineinfo = datatier.select_one_row(dbConn, sql, [movie_id])
        if taglineinfo == ():
            tagline = ""
        else:
            tagline = taglineinfo[0]
        sql = """Select Count(Rating), avg(Rating)
                From Ratings
                Where Ratings.Movie_ID = ?"""
        ratinginfo = datatier.select_one_row(dbConn, sql, [movie_id])
        if ratinginfo == () or ratinginfo[1] is None:
            ratinginfo = (0, 0.0)
        sql = """Select Genres.Genre_Name
                From Movie_Genres
                Join Genres on Movie_Genres.Genre_ID = Genres.Genre_ID
                Where Movie_Genres.Movie_ID = ?
                Order By Genre_Name Asc"""
        genreinfo = datatier.select_n_rows(dbConn, sql, [movie_id])
        genres = []
        for x in genreinfo:
            genres.append(x[0])
        sql = """Select Companies.Company_Name
                From Movie_Production_Companies
                Join Companies on Movie_Production_Companies.Company_ID = 
                    Companies.Company_ID
                Where Movie_Production_Companies.Movie_ID = ?
                Order by Company_Name Asc"""
        companyinfo = datatier.select_n_rows(dbConn, sql, [movie_id])
        companies = []
        for x in companyinfo:
            companies.append(x[0])
        mdo = MovieDetails(minfo[0], minfo[1], minfo[2], minfo[3], minfo[4], 
                           minfo[5], minfo[6], ratinginfo[0], ratinginfo[1], 
                           tagline, genres, companies)
        return mdo
    except:
        return None
        
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    returnList = []
    sql = f"""Select Movies.Movie_ID, Title, Release_Date, Count(Rating),
                Avg(Rating)
            From Movies
            Join Ratings on Movies.Movie_ID = Ratings.Movie_ID
            Group By Movies.Movie_ID
            Having Count(Rating) >= {min_num_reviews}
            Order By Avg(Rating) Desc
            Limit {N}"""
    rows = datatier.select_n_rows(dbConn, sql)
    for x in rows:
        tempObj = MovieRating(x[0], x[1], x[2][:4], x[3], x[4])
        returnList.append(tempObj)
    return returnList


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    sql = "Select Movie_ID From Movies Where Movie_ID = ?"
    if datatier.select_one_row(dbConn, sql, [movie_id]) != ():
        try:
            sql = f"""INSERT INTO Ratings
                VALUES({movie_id}, {rating})"""
            val = datatier.perform_action(dbConn, sql)
            if val == -1:
                val = 0
            return val
        except:
            return 0
    else:
        return 0
    

##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    sql = "Select Movie_ID From Movies Where Movie_ID = ?"
    if datatier.select_one_row(dbConn, sql, [movie_id]) != ():
        try:
            sql = f"""Select Tagline
                    From Movie_Taglines
                    Where Movie_ID = {movie_id}"""
            value = datatier.select_one_row(dbConn, sql)
            if value == ():
                sql = f"""INSERT INTO Movie_Taglines
                       VALUES({movie_id}, '{tagline}')"""
                val = datatier.perform_action(dbConn, sql)
            else:
                sql = f"""UPDATE Movie_Taglines
                       SET Tagline = '{tagline}'
                       WHERE Movie_ID = {movie_id}"""
                val = datatier.perform_action(dbConn, sql)
            if val == -1:
                val = 0
            return val
        except:
            return 0
    else:
        return 0
