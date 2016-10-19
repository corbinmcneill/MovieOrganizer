import subprocess
import shutil
import functools
import urllib.request
import os
import string
import json
import sys
from sys import argv

movie_extensions = ["mp4", "mkv", "avi", "m4v"]

def update_movies(movies, rules):
    movies = movies[:]
    for rule in rules:
        for i in range(len(movies))[::-1]:
            movie = movies[i]
            if not eval(rule):
                movies.pop(i)
    return movies

def extract_title_and_year(movie_title):
    year = None
    title = ""
    i = 0
    while i < len(movie_title):
        if movie_title[i] == '(':
            isYear = True
            for j in range(1,5):
                if not movie_title[i+j] in string.digits:
                    isYear = False
            if not movie_title[i+5] == ')':
                isYear = False
            if isYear:
                year = int(movie_title[i+1:i+5])
                i = i+6
            else:
                try:
                    i=movie_title.find(')', i)
                except ValueError:
                    i = len(movie_title)
        elif movie_title[i] == '[':
            isYear = True
            for j in range(1,5):
                if not movie_title[i+j] in string.digits:
                    isYear = False
            if not movie_title[i+5] == ']':
                isYear = False
            if isYear:
                year = int(movie_title[i+1:i+5])
                i = i+6
            else:
                try:
                    i=movie_title.find(']', i)
                except ValueError:
                    i = len(movie_title)
        elif movie_title[i] in string.ascii_letters or movie_title[i] in string.digits:
            title += movie_title[i]
            i+=1
        elif movie_title[i] == ".":
            break
        elif movie_title[i] == " " or movie_title[i] == "'":
            title += movie_title[i]
            i+=1
        else:
            i+=1
    return (title, year)

    

class Movie:
    # title is a string
    # year is an integer
    # plot is a string
    # imdb is float
    # msaa one of the follwoign strings: "G", "PG", "PG-13", "R", "NC-17"
    # director is a string
    # runtime is an integer representing the number of minutes of runtime
    # genre is a string
    # metascore is an integer
    def __init__(self, _filepath, _filename, _title, _year, _plot, _imdb, 
            _msaa, _director, _runtime, _genre): 
        self.filepath = _filepath
        self.filename = _filename
        self.title = _title
        self.year = _year
        self.plot = _plot
        self.imdb = _imdb
        self.msaa = _msaa
        self.director = _director
        self.runtime = _runtime
        self.genre = _genre

    def __str__(self):
        return "{0:55}   [{1:4}]   ({2:4})   {3:5}".format(self.title[:55], self.imdb, self.year, self.msaa)

    def print_all(self):
        print("Title:          %s"%self.title)
        print("Year:           %d"%self.year)
        print("MSAA Rating:    %s"%self.msaa)
        print("Genre(s):       %s"%self.genre)
        print("IMdB Rating:    %s"%self.imdb)
        print("Runtime:        %d min."%self.runtime)
        print("Director:       %s"%self.director)
        print("Plot:           %s"%self.plot[:60])
        for i in range(int((len(self.plot)-1)/60)):
            print("                %s"%self.plot[60*(i+1):60*(i+2)])

def printHelpMessage():
    print("This is a help message")

#------------------------------------------------------------------------#
#------------------- Begin the main execution routine -------------------#
#------------------------------------------------------------------------#
if "-h" in argv[1:] or "--help" in argv[1:]:
    printHelpMessage()
    sys.exit(0);

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
                try:
                    search_title, search_year = extract_title_and_year(filename)
                    search_title = search_title.replace(" ", "+")
                    weburl = "http://www.omdbapi.com/?t=%s&y=%d&plot=long&r=json" % (search_title, search_year)
                    webobject = urllib.request.urlopen(weburl);
                    contents = webobject.read().decode("utf-8")
                    webobject.close()
                    parsed_result = decoder.decode(contents)

                    if parsed_result["Response"] != "True":
                        print("No match found for %s. Please rename file."%(search_directory + "/" + filename))
                        break

                    this_movie = Movie(search_directory + "/" + filename,
                                       filename, 
                                       parsed_result["Title"],
                                       int(parsed_result["Year"]),
                                       parsed_result["Plot"],
                                       float(parsed_result["imdbRating"]),
                                       parsed_result["Rated"],
                                       parsed_result["Director"],
                                       int(parsed_result["Runtime"].replace(" min", "").replace("N/A", "0")),
                                       parsed_result["Genre"])
                    all_movies.append(this_movie)
                    break
                except:
                    raise

rules = []
movies = all_movies[:]
while (True):
    #try:
        inputstring = input("> ")
        location = inputstring.find(" ")
        if (location > -1):
            command = inputstring[:location]
            argument = inputstring[location+1:]
        else:
            command = inputstring[:]
            argument = ""

        if command == "add":
            rules.append(argument)
            movies = update_movies(all_movies, rules)
        elif command == "rules":
            for i in range(len(rules)):
                print("[%d]:\t%s" %(i, rules[i]))
        elif command == "list":
            for i in range(len(movies)):
                print("[%d]:\t%s" %(i, movies[i]))
        elif command == "remove":
            rules.pop(int(argument))
            movies = update_movies(all_movies, rules)
        elif command == "sort":
            rev= "!" in argument
            if "imdb" in argument:
                movies.sort(key=lambda x:-x.imdb, reverse=rev)
            elif "year" in argument:
                movies.sort(key=lambda x:x.year, reverse=rev)
            elif "msaa" in argument:
                movies.sort(key=lambda x:x.msaa, reverse=rev)
            elif "title" in argument:
                movies.sort(key=lambda x:x.title, reverse=rev)
            else:
                print ("Sorry that is not a valid sort criteria.")
        elif command == "watch":
            number = int(argument)
            shutil.copy(movies[number].filepath, "/tmp/")
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "/tmp/"+movies[number].filename])

        elif command == "details":
            number = int(argument)
            movies[number].print_all()
        elif command == "help":
            print("Sorry. No help information is currently available")
        elif command == "exit":
            os._exit(0)
        else:
            print("No such command. Type 'help' for assistance.")

