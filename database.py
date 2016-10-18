from sys import argv
import os

class Movie:
    # title is a string
    # year is an integer
    # plot is a string
    # imdb_rating is float
    # msaa one of the follwoign strings: "G", "PG", "PG-13", "R", "NC-17"
    # actors is a list of strings
    # director is a string
    # runtime is an integer representing the number of minutes of runtime
    # genre is a list of strings
    # metascore is an integer
    def __init__(self, _filename, _title, _year, _plot, _imdb_rating, 
            _msaa, _actors, _director, _runtime, _genre, _metascore):
        self.filename = _filename;
        self.title = _title
        self.year = _year
        self.plot = _plot
        self.imdb_rating = _imdb_rating
        self.msaa = _msaa
        self.actors = _actors
        self.director = _director
        self.runtime = _runtime
        self.genre = _genre
        self.metascore = _metascore


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

movies = {};
for search_directory in search_directories:
    for filename in os.listdir(search_directory):
        all_files.append(search_directory + "/" + filename)
        search_title = filename;
