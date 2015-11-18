from year import year

#clubs movies on the basis of their years, genreates year_movie dictionary
def club_year():
    temp_data = {}
    for k in year:
        if(k in temp_data):
            temp_data[year[k]].append(k)
        else:
            temp_data[year[k]] = [k]
    print temp_data

if __name__ == "__main__":
    club_genre()
