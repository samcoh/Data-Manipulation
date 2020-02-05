import json
import requests
import webbrowser

class Media:
	def __init__(self, title = "No Title", author = "No Author", release_year = "No Release Year", json = None):
		if json is not None:
			try:
				self.title = json["trackName"]
				self.author= json["artistName"]
				self.year = int(json["releaseDate"][:4])
			except:
				self.title = json["collectionName"]
				self.author= json["artistName"]
				self.year = int(json["releaseDate"][:4])

		else:
			self.title = title
			self.author = author
			self.year = release_year
	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.year)
	def __len__(self):
		return 0
#new= Media(2016, "Jaws", "Steven")
#print(new)
## Other classes, functions, etc. should go here
class Song(Media):
	def __init__(self, title = "No Title", author = "No Author", release_year = "No Release Year", track_length = "No Track Length", album = "No Album", genre= "No Genre", json = None):
		super().__init__(title, author, release_year, json)
		if json is not None:
			self.tracklen = (json["trackTimeMillis"] * .001) #convert milliseconds to seconds
			self.album = json["collectionName"]
			self.genre= json["primaryGenreName"]
		else:
			self.tracklen = track_length
			self.album = album
			self.genre = genre
	def __str__(self):
		return super().__str__()+" ["+self.genre+"]"
	def __len__(self):
		return int(self.tracklen) #returns length in seconds
# song= Song("title", "author", 2016, 5, "album", "genre")
# print(song.tracklen)
# print(song.year)
# print(song.title)
# print(song.author)
# print(song.album)
# print(song.genre)
# print(song)
class Movie(Media):
	def __init__(self, title = "No Title", author = "No Author", release_year = "No Release Year", rating= "No Rating", movie_length= "No Movie Length", json = None):
		super().__init__(title, author, release_year, json)
		if json is not None:
			self.rating = json["contentAdvisoryRating"]
			self.movielen = (json["trackTimeMillis"] * .001)/60 #convert milliseconds to seconds and seconds to minutes
		else:
			self.rating = rating
			self.movielen = movie_length
	def __str__(self):
		return super().__str__()+" ["+self.rating+"]"
	def __len__(self):
		 return int(round(self.movielen, 0)) #return minutes

# movie= Movie("Jaws", "Steven", 2016, "R", 1.95,)
# print(movie.title)
# print(movie.author)
# print(movie.rating)
# print(movie.movielen)
# print(movie)
# print(movie.__len__())
# print(movie)
# print(song)
# print(media)
# print(movie.title)
# print(movie.rating)
# print(movie.author)
# print(media.title)
# print(song.album)


def get_from_url(p):
	base_url = "https://itunes.apple.com/search?"
	result = requests.get(base_url, params = {'term': p, 'limit': 20})
	data= json.loads(result.text)
	data_from_api= data['results']
	return data_from_api
#p = ("moana", "helter skelter")
#print(get_from_url(p))
#print(get_from_url("Helter Skelter"))
#print(get_from_url("Dave Ramsey"))
#print(get_from_url("Pardon My Take"))

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	response= input("Please enter a search term, or enter exit to quit: ")
	while response != 'exit':
		try:
			for x in list_with_nums:
				split = x.split('.')
				if int(response) == int(split[0]):
					url = list_with_nums[x]
					print("Launching...")
					print(url)
					webbrowser.open(url, new = 0, autoraise = True)
		except:
			response = get_from_url(response)
			if len(response) == 0:
				response = input("There are no results. Please type in a new term to search or exit to quit: ")
				continue
			number = 0
			songs_list = {}
			movies_list = {}
			media_list = {}
			for x in response:
				if x["wrapperType"] == "track":
					url = x["trackViewUrl"]
					if x["kind"] == 'feature-movie':
						movie = Movie(json = x)
						movies_list[url] = movie.__str__()
					elif x["kind"]== 'song':
						song = Song(json = x)
						songs_list[url] = song.__str__()
					else:
						media = Media(json = x)
						media_list[url] = media.__str__()
				else:
					url = x["collectionViewUrl"]
					media = Media(json = x)
					media_list[url] = media.__str__()
			list_with_nums = {}
			print("MOVIES")
			for m in movies_list:
				number = number + 1
				string = str(number)+". "+ movies_list[m]
				list_with_nums[string] = m
				print(string)
			if len(movies_list) == 0:
				print("No results in this category")

			print("SONGS")
			for s in songs_list:
				number = number + 1
				string = str(number)+". "+ songs_list[s]
				list_with_nums[string] = s
				print(string)
			if len(songs_list) == 0:
				print("No results in category")

			print("OTHER MEDIA")
			for x in media_list:
				number = number + 1
				string = str(number)+". "+ media_list[x]
				list_with_nums[string] = x
				print(string)
			if len(media_list)==0:
				print("No results in this category")
		answer = input("Enter a number for more info, or another search term, or exit: ")
		response = answer
		if response == "exit":
			print("Bye!")
