import os
import string
import urllib.request
import json
from sys import argv

movie_extensions = ["mp4", "mkv"]

class Movie:
    # title is a string
    # year is an integer
    # plot is a string
    # imdb_rating is float
    # msaa one of the follwoign strings: "G", "PG", "PG-13", "R", "NC-17"
    # director is a string
    # runtime is an integer representing the number of minutes of runtime
    # genre is a string
    # metascore is an integer
    def __init__(self, _filename, _title, _year, _plot, _imdb_rating, 
            _msaa, _director, _runtime, _genre): 
        self.filename = _filename;
        self.title = _title
        self.year = _year
        self.plot = _plot
        self.imdb_rating = _imdb_rating
        self.msaa = _msaa
        self.director = _director
        self.runtime = _runtime
        self.genre = _genre

    def __str__(self):
        return (self.title + "\t(" + str(self.year) + ")\t" + str(self.imdb_rating))


def printHelpMessage():
    print("This is a help message")

#------------------------------------------------------------------------#
#------------------- Begin the main execution routine -------------------#
#------------------------------------------------------------------------#
if "-h" in argv[1:] or "--help" in argv[1:]:
    printHelpMessage()
    exit(0);

search_directories = ["."]
if len(argv) > 1:
    for new_path in argv[1:]:
        search_directories.append(new_path)

all_movies = [];

decoder = json.JSONDecoder()
for search_directory in search_directories:
    for filename in os.listdir(search_directory):
        for extension in movie_extensions:
            if extension in filename:
                #all_files.append(search_directory + "/" + filename)
                search_title = filename
                year_start = search_title.index('(')
                year_end = search_title.index(')')
                search_year = int(search_title[year_start+1:year_end])
                search_title = search_title[:year_start]
                search_title = search_title.replace(" ", "+")

                weburl = "http://www.omdbapi.com/?t=%s&y=%d&plot=long&r=json" % (search_title, search_year)
                print(weburl)
                webobject = urllib.request.urlopen(weburl);
                contents = webobject.read().decode("utf-8")
                parsed_result = decoder.decode(contents)
                print(parsed_result)
                print()

                this_movie = Movie(search_directory + "/" + filename,
                                   parsed_result["Title"],
                                   int(parsed_result["Year"]),
                                   parsed_result["Plot"],
                                   float(parsed_result["imdbRating"]),
                                   parsed_result["Rated"],
                                   parsed_result["Director"],
                                   int(parsed_result["Runtime"].replace(" min", "")),
                                   parsed_result["Genre"])
                all_movies.append(this_movie)
                break

rules = []
movies = all_movies[:]
while (True):
    inputstring = raw_input("> ")
    location = inputstring.find(" ")
    if (location > -1):
        command = inputstring[:location]
        argument = inputstring[location+1:]
    else:
        command = inputstring[:]
        argument = ""

    if command == "add":
        pass
    elif command == "rules":
        pass
    elif command == "list":
        pass
    elif command == "remove":
        pass
    elif command == "sort":
        pass
    elif command == "watch":
        pass
    elif command == "details":
        pass
    elif command == "help":
        pass
    else:
        print("No such command. Type 'help' for assistance.")
