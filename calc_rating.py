from movies import movies
from critics import critics
import data

#calculates the average rating of all movies, genreates average_rating dictionary
def calc_rating():
	movie_user = {}
	avg_rat = {}
	for movie in movies:
	  for user in critics:
	    if(movie in critics[user].keys()):
	      if(movie in avg_rat):
		avg_rat[movie] = avg_rat[movie] + critics[user][movie]
	      else:
		avg_rat[movie] = critics[user][movie]
	      
	      if(movie in movie_user):
		movie_user[movie] = movie_user[movie] + 1
	      else:
		movie_user[movie] = 1
	print avg_rat

	for film in avg_rat:
	    avg_rat[film] = round(float(avg_rat[film])/float(movie_user[film]),1)
	print avg_rat

if __name__ == "__main__":
	calc_rating()
