from math import sqrt
#import MySQLdb as mdb
from movies import movies
from critics import critics
from genre_movie import genre_movie
from year_movie import year_movie
from category import category
from average_rating import average_rating
from genre import genre

class domain_select(object):

    #constructor
    def __init__(self):
        return

    #there are 2 kinds of similartiy measeres (user can choose)
    def sim_menu(self):
        sim_obj = similarity()
        while(1):
            print("\nEnter choice\n1. Eucledian\n2. Pearson\n3. Exit")
            inp = raw_input()
            if(inp == "1"):
                print "Enter person1 and person2\n"
                print "\n1st person:\n"
                p1 = raw_input()
                print "\n2st person:\n"
                p2 = raw_input()
                distance = sim_obj.sim_distance(critics,p1.lower(),p2.lower())
            if(inp == "2"):
                print "Enter person1 and person2\n"
                print "\n1st person:\n"
                p1 = raw_input()
                print "\n2st person:\n"
                p2 = raw_input()
                distance = sim_obj.sim_pearson(critics,p1,p2)
            if(inp == "3"):
                return
            print "Similarity distance is ",distance

    #two types of features implemented - Genre, Year
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

    #call nearest neighbours module for given person
    def group_inp(self):
        print("\nEnter name of the user\n")
        user = raw_input()
        group_obj = grouping()
        #group_obj.topMatches(critics,user,n=10,similar=sim_pearson)
        group_obj.topMatches(critics,user,n=10)

    #calculate recommendation on the basis of ratings
    def recomm(self):
        print("\nEnter name of the user\n")
        user = raw_input()
        control_obj = controller()
        control_obj.getRecommendations(critics,user)

class grouping(object):
    
    #Ranking function
    #Returns the best matches for person from the critics dictionary.
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
    
    #distance calculation based on Pearson Correlation
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
    
    #Recommend
    #gets recommendations for a person by using a weighted average of every other user's rankings
    def getRecommendations(self,critics,person):
        totals={}
        simSums={}
        sim_obj = similarity()
        for other in critics:
            if other==person:
                continue
            sim=sim_obj.sim_pearson(critics,person,other)
            if sim<=0:
                continue
            for item in critics[other]:
                if item not in critics[person] or critics[person][item]==0:
                    totals.setdefault(item,0)
                    totals[item]+=critics[other][item]*sim
                    simSums.setdefault(item,0)
                    simSums[item]+=sim
        #normalized ranking list
        rankings=[(total/simSums[item],item) for item,total in totals.items( )]
        #sorted list
        rankings.sort( )
        rankings.reverse( )
        suggestions =  [x[1] for x in rankings][:10]
        print "\n### POPULAR RESULTS ###\n"
        for index,suggestions in enumerate(suggestions):
            print index+1,". ",suggestions
            

    #Recommendation based on genre
    def cat_recomm(self,genre_movie,avg_rat,_genre):
        rec = {}
        index = 1
        for item in genre_movie:
            #print item
            if(item == _genre):
                
                candidate_movies = genre_movie[item]
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
        for movie in candidate_movies:
            if(movie in avg_rat) and (avg_rat[movie] >= 2.5):
                rec[movie] = avg_rat[movie]
        print "\n### POPULAR RESULTS FOR ",_year.upper()," ###\n"
        for item in rec:
            if(rec[item] >= 2):
                print index,".", item
                index += 1
        
class ui(object):

	def menu(self):
		#User is prompted to enter a choice for user-wise suggestion or feature-wise suggestion
	    while(True):
		print("\nEnter choice\n1. Similarity Between Users\n2. List Similar Users \n3. General Suggestion\n4. Feature-wise Suggestion\n5. Exit\n")
		inp = raw_input()
		if(inp == "1"):
		    dom_obj = domain_select()
		    dom_obj.sim_menu()
		if(inp == "2"):
		    dom_obj = domain_select()
		    dom_obj.group_inp()
		if(inp == "3"):
		    dom_obj = domain_select()
		    dom_obj.recomm()
		if(inp == "4"):
		    dom_obj = domain_select()
		    dom_obj.feature_menu()
		if(inp == "5"):
		    break

##class connect(object):
##    
##    #MYSQL database connectivity
##    def db_connect(self):
##        con = mdb.connect('localhost', 'vishakha', 'vishakha', 'data');
##        return con


if __name__ == "__main__":
    
    if_obj = ui()
    if_obj.menu()
