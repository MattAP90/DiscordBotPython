from simplejustwatchapi.justwatch import offers_for_countries, search

def get_movies(user_input): 
    movies = ''
    results = search(user_input, "US", "en", 10, True)
    for result in results:
        movies += '**' + result.title + '**(' + str(result.release_year) + ')\n'
        movies += 'POSTER:\n' + str(result.poster) + '\n'
        movies += '\n'
    return movies

def get_movie_info(user_input):
   return user_input 
