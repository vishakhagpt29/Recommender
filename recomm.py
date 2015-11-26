from math import sqrt
import MySQLdb as mdb
from movies import movies
from critics import critics
from genre_movie import genre_movie
from year_movie import year_movie
from category import category
from average_rating import average_rating
from genre import genre

class domain_select(object):

    #there are 2 kinds of similartiy measeres (user can choose)
    def sim_menu(self):
        sim_obj = similarity()
        while(1):
            print("\nEnter choice\n1. Eucledian\n2. Pearson\n3. Exit")
            inp = raw_input()
            if(inp == "1"):
                print "enter person1 and person2\n"
                p1 = raw_input()
                p2 = raw_input()
                distance = sim_obj.sim_distance(critics,p1.lower(),p2.lower())
            if(inp == "2"):
                p1 = raw_input()
                p2 = raw_input()
                distance = sim_obj.sim_pearson(critics,p1,p2)
            if(inp == "3"):
                return
            print "Similarity distance is ",distance

    #there are 2 types of features implemented
    def feature_menu(self):
            print("\nEnter choice\n1. Genre\n2. Year\n3. Back\n")
            inp = raw_input()
            if(inp == "1"):
                print "Available Genre :",genre
                print("Enter genre\n")
                _genre = raw_input()
                control_obj = controller()
                control_obj.cat_recomm(genre_movie,average_rating,_genre)
            if(inp == "2"):
                print("Enter year (1926 - 1998)\n")
                _year = raw_input()
                control_obj = controller()
                control_obj.year_recomm(year_movie,average_rating,_year)
            if(inp == "3"):
                return

    def group_inp(self):
        print("\nEnter name of the user\n")
        user = raw_input()
        group_obj = grouping()
        #group_obj.topMatches(critics,user,n=10,similar=sim_pearson)
        group_obj.topMatches(critics,user,n=10)

class grouping(object):
    
    #Ranking function
    # Returns the best matches for person from the prefs dictionary.
    # Number of results and similarity function are optional params.
    def topMatches(self,critics,person,n):
        sim_obj = similarity()
        scores=[(sim_obj.sim_pearson(critics,person,other),other)
        for other in critics if other!=person]
        # Sort the list so the highest scores appear at the top
        scores.sort( )
        scores.reverse( )
        neighbours =  [x[1] for x in scores][:n]
        print "\n### TOP 10 NEIGHBOURS OF",person.upper()," ###\n"
        for index,neighbour in enumerate(neighbours):
            print index+1,". ",neighbour


class similarity(object):

    #distance calculation based on Eucledian distance
    def sim_distance(self,db,p1,p2):
        si={}
        for item in db[p1.lower()]:
            if item in db[p2.lower()]:
                si[item]=1
        if len(si)==0: return 0
        sum_of_squares=sum([pow(db[p1.lower()][item]-db[p2.lower()][item],2)
                            for item in db[p1.lower()]
                                if item in db[p2.lower()]])
        return 1/(1+sum_of_squares)

    #distance calculation based on Pearson Correlation
##    def sim_pearson(self,db,p1,p2):
##        si={}
##        for item in db[p1]:
##            if item in db[p2]:
##                si[item]=1
##        n=len(si)
##        if n==0: return 0
##        sum1=sum([db[p1.lower()][it] for it in si])
##        sum2=sum([db[p2.lower()][it] for it in si])
##        sum1Sq=sum([pow(db[p1.lower()][it],2) for it in si])
##        sum2Sq=sum([pow(db[p2.lower()][it],2) for it in si])
##        pSum=sum([db[p1.lower()][it]*db[p2.lower()][it] for it in si])
##        num=pSum-(sum1*sum2/n)
##        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
##        if den==0: return 0
##        r=num/den
##        return r
    def sim_pearson(self,db,p1,p2):
        si={}
        for item in db[p1]:
            if item in db[p2]: si[item]=1
        n=len(si)
        if n==0: return 0
        sum1=sum([db[p1][it] for it in si])
        sum2=sum([db[p2][it] for it in si])
        sum1Sq=sum([pow(db[p1][it],2) for it in si])
        sum2Sq=sum([pow(db[p2][it],2) for it in si])
        pSum=sum([db[p1][it]*db[p2][it] for it in si])
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0: return 0
        r=num/den
        return r

class controller(object):
    
    #Retrieve fn
    def retrieve(self):
        return
    
    #Recommend
    def recommend(self):
        return

    #Recommendation based on genre
    def cat_recomm(self,genre_movie,avg_rat,_genre):
        rec = {}
        index = 1
        for item in genre_movie:
            #print item
            if(item == _genre):
                
                candidate_movies = genre_movie[item]
            
##            else:
##                print "Genre Not Fount in Database."
##                return
        for movie in candidate_movies:
            if(movie in avg_rat) and (avg_rat[movie] >= 2.5):
                rec[movie] = avg_rat[movie]
        print "\n### POPULAR RESULTS IN ",_genre.upper()," ###\n"
        for item in rec:
            if(rec[item] >= 2):
                print index,".", item
                index += 1

    #Recommendation based on year    
    def year_recomm(self,year_movie,avg_rat,_year):
        rec = {}
        index = 1
        for item in year_movie:
            if(item == _year):
                candidate_movies = year_movie[item]
##            else:
##                print "Year Not Fount in Database."
##                return
        for movie in candidate_movies:
            if(movie in avg_rat) and (avg_rat[movie] >= 2.5):
                rec[movie] = avg_rat[movie]
        print "\n### POPULAR RESULTS FOR ",_year.upper()," ###\n"
        for item in rec:
            if(rec[item] >= 2):
                print index,".", item
                index += 1
        


class connect(object):
    
    #MYSQL database connectivity
    def db_connect(self):
        con = mdb.connect('localhost', 'vishakha', 'vishakha', 'data');
        return con


if __name__ == "__main__":
    
    #User is prompted to ebter a choice for user-wise suggestion or feature-wise suggestion
    while(True):
        print("\nEnter choice\n1. Similarity between users\n2. List similar users \n3. Feature-wise Suggestion\n4. Exit\n")
        inp = raw_input()
        if(inp == "1"):
            dom_obj = domain_select()
            dom_obj.sim_menu()
        if(inp == "2"):
            dom_obj = domain_select()
            dom_obj.group_inp()
        if(inp == "3"):
            dom_obj = domain_select()
            dom_obj.feature_menu()
        if(inp == "4"):
            break
