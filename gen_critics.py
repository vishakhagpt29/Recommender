from movies import movies
from names import names
import random

#assigns random rating for movies of user, generates critics nested dictionary
def gen_critics(critics):
    sub_dict = {}
    for name in names:
        no_of_movies = random.randrange(3,10)
        while(no_of_movies > 0):
            sub_dict[movies[random.randrange(0,len(movies))]] = random.randrange(1,5)
            no_of_movies = no_of_movies - 1
        critics[name] = sub_dict
        sub_dict = {}
    return critics

if __name__ == "__main__":
    critics = {}
    critics = gen_critics(critics)
    print critics
