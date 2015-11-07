from math import sqrt
from ratings import critics
import MySQLdb as mdb

class domain_select(object):
    def menu(self):
        sim_obj = similarity()
        while(1):
            print("Enter choice\n1. Eucledian\n2. Pearson\n3. Exit")
            inp = raw_input()
            if(inp == "1"):
                print "enter person1 and person2\n"
                p1 = raw_input()
                p2 = raw_input()
                distance = sim_obj.sim_distance(critics,p1,p2)
            if(inp == "2"):
                p1 = raw_input()
                p2 = raw_input()
                distance = sim_obj.sim_pearson(critics,p1,p2)
            if(inp == "3"):
                return
            print "Similarity distance is ",distance
            

class similarity(object):
    def sim_distance(self,db,p1,p2):
        si={}
        for item in db[p1]:
            if item in db[p2]:
                si[item]=1
        if len(si)==0: return 0
        sum_of_squares=sum([pow(db[p1][item]-db[p2][item],2)
                            for item in db[p1]
                                if item in db[p2]])
        return 1/(1+sum_of_squares)

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

class grouping(object):
    #Ranking function
    def ranking(self):
        return
    

class controller(object):
    #Retrieve fn
    def retrieve(self):
        return
    #Recommend
    def recommend(self):
        return
    

class connect(object):
    #MYSQL database connectivity
    def db_connect(self):
        con = mdb.connect('localhost', 'vishakha', 'vishakha', 'ratings');
        return con
   


            

if __name__ == "__main__":
    while(True):
        print("Enter choice\n1. Calculate similarity\n2. Exit\n")
        inp = raw_input()
        if(inp == "1"):
            dom_obj = domain_select()
            dom_obj.menu()
        if(inp == "2"):
            break


