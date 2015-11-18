from data import category

#clubs movies on the basis of their genre, genreates genre_movie dictionary
def club_genre():
    temp_data = {}
    for k in category:
        x = category[k]
        for index, item in enumerate(x):
            if item in temp_data:
                temp_data[item].append(k)
            else:
                temp_data[item] = [k]
    print temp_data
    

if __name__ == "__main__":
    club_genre()
