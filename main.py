# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:58:51 2022

@author: Jonah
"""

import objecttier
import sqlite3
############################################################
def doGeneralStats(dbConn):
    print("General stats:")
    print(f"  # of movies: {objecttier.num_movies(dbConn):,}");
    print(f"  # of reviews: {objecttier.num_reviews(dbConn):,}");
    
############################################################
    
def doCommand1(dbConn):
    name = input("Enter movie name (wildcards _ and % supported): ")
    movies = objecttier.get_movies(dbConn, name)
    print()
    if movies is None or movies == []:
        print("# of movies found: 0\n")
    elif len(movies) > 100:
        print(f"# of movies found: {len(movies)}\n")
        print("There are too many movies to display, please narrow your search and try again...")
    else:
        print(f"# of movies found: {len(movies)}\n")
        for x in movies:
            print(f"{x.Movie_ID} : {x.Title} ({x.Release_Year})")

############################################################

def doCommand2(dbConn):
    movie_id = input("Enter movie id: ")
    MovieInfo = objecttier.get_movie_details(dbConn, movie_id)
    print()
    if MovieInfo is None:
        print("No such movie...")
    else:
        print(f"{movie_id} : {MovieInfo.Title}")
        print(f" Release date: {MovieInfo.Release_Date}")
        print(f" Runtime: {MovieInfo.Runtime} (mins)")
        print(f" Orig language: {MovieInfo.Original_Language}")
        print(f" Budget: ${MovieInfo.Budget:,} (USD)")
        print(f" Revenue: ${MovieInfo.Revenue:,} (USD)")
        print(f" Num reviews: {MovieInfo.Num_Reviews}")
        print(f" Avg rating: {MovieInfo.Avg_Rating:.2f} (0..10)")
        genres = ""
        for x in MovieInfo.Genres:
            genres += x + ", "
        print(f" Genres: {genres}")
        companies = ""
        for x in MovieInfo.Production_Companies:
            companies += x + ", "
        print(f" Production companies: {companies}")
        print(f" Tagline: {MovieInfo.Tagline}")
    print()

############################################################

def doCommand3(dbConn):
    num = int(input("N? "))
    if num < 1:
        print("Please enter a positive value for N...\n")
        return
    num_revs = int(input("min number of reviews? "))
    if num_revs < 1:
        print("Please enter a positive value for min number of reviews...\n")
        return
    print()
    movies = objecttier.get_top_N_movies(dbConn, num, num_revs)
    for x in movies:
        print(f"{x.Movie_ID} : {x.Title} ({x.Release_Year}), avg rating = {x.Avg_Rating:.2f} ({x.Num_Reviews} reviews)")
    print()

############################################################

def doCommand4(dbConn):
    rating = int(input("Enter rating (0..10): "))
    if rating < 0 or rating > 10:
        print("Invalid rating...\n")
        return
    movie_id = input("Enter movie id: ")
    num = objecttier.add_review(dbConn, movie_id, rating)
    print()
    if num == 0:
        print("No such movie...")
    else:
        print("Review successfully inserted")
        print()

############################################################

def doCommand5(dbConn):
    tag = input("tagline? ")
    movie_id = input("movie id? ")
    num = objecttier.set_tagline(dbConn, movie_id, tag)
    print()
    if num == 0:
        print("No such movie...")
        print()
        return
    else:
        print("Tagline successfully set")
        print()

############################################################
# Main:
#
print('** Welcome to the MovieLens app **')
dbConn = sqlite3.connect('MovieLens.db')
print()

doGeneralStats(dbConn)

cmd = input("Please enter a command (1-5, x to exit): ")
print()

while cmd != "x":
    if cmd == "1":
        doCommand1(dbConn)
    elif cmd == "2":
        doCommand2(dbConn)
    elif cmd == "3":
        doCommand3(dbConn)
    elif cmd == "4":
        doCommand4(dbConn)
    elif cmd == "5":
        doCommand5(dbConn)
    else:
        print("**Error, unknown command, try again...")

    cmd = input("Please enter a command (1-5, x to exit): ")
    print()

#
# done
#