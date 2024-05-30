from simplejustwatchapi.justwatch import offers_for_countries, search, details

def get_movies(user_input): 
    movies = ''
    results = search(user_input, "US", "en", 10, True)
    for result in results:
        movies += '**' + result.title + '**(' + str(result.release_year) + ')\n'
        movies += 'JW ID: ' + result.entry_id + '\n'
        movies += 'POSTER:\n<' + str(result.poster) + '>\n'
        movies += '\n'
    return movies

def get_movie_info(user_input):
    
    movie_info = ''
    result = details(user_input, "US", "en", True)
    if result is None:
        movie_info += 'id entered not found, use !msearch to find movies and ids\nReturning top search if movie title was entered\n\n'
        result = search(user_input, "US", "en", 1, True)
        result = result[0]
        if result.title == 'Movie 43':
            movie_info += '**Movie 43 was returned, meaning movie was not found by search**\n\n'
        movie_info += _assemble_movie_string(result)
        return movie_info
    else:
        movie_info += _assemble_movie_string(result)
        return movie_info

def get_streaming(user_input):

    movies_streaming = ''
    results = search(user_input, "US", "en", 3, True)
    for result in results:
        movies_streaming += '**' + result.title + '**(' + str(result.release_year) + ')'
        movies_streaming += _assemble_streaming(result)
    return movies_streaming


def _assemble_movie_string(result):
 
    info = ''
    info += '**' + result.title + '**\nRelease Date: ' + result.release_date + '\n'
    info += 'Runtime: ' + str(result.runtime_minutes) + '\nGenres: '
    count = 1
    total_genres = len(result.genres)
    for genre in result.genres:
        if count == total_genres:
            info += genre + '\n'
        else:
            info += genre + ', '
            count += 1
    info += 'Poster: ' + result.poster + '\n'
    info += 'Desc: \n    ' + result.short_description + '\n\n'
    info += 'JustWatch: \n<' + result.url + '>\n'
    info += _assemble_streaming(result)

    return info

def _assemble_streaming(result):

    info = ''
    s_flag = 0
    a_flag = 0
    f_flag = 0
    r_flag = 0
    rent_count = 0
    for offer in result.offers:
        if offer.monetization_type == 'FLATRATE':
            if s_flag == 0:
                info += '\nSTREAMING:\n'
                s_flag = 1
            info += offer.package.name + ': <' + offer.url + '>\n'
        elif offer.monetization_type == 'ADS':
            if a_flag == 0:
                info += '\nFREE WITH ADS:\n'
                a_flag = 1
            info += offer.package.name + ': <' + offer.url + '>\n'
        elif offer.monetization_type == 'FREE':
            if f_flag == 0:
                info += '\nFREE:\n'
                f_flag = 1
            info += offer.package.name + ': <' + offer.url + '>\n'
        elif offer.monetization_type == 'RENT':
            if r_flag == 0:
                info += '\nRENT:\n'
                r_flag = 1
            if rent_count < 3:
                info += offer.package.name + '(' + offer.price_string + '): <' + offer.url + '>\n'
                rent_count += 1
    info += '\n'
    return info
