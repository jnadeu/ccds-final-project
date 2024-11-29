import datetime
import pymongo
from pymongo import MongoClient, ReadPreference
import redis
import json

# Init MongoDB
client = MongoClient("mongodb://app:secret@mongodb:27017")
#                     #replicaSet="myReplicaSet",
#                     read_preference=ReadPreference.PRIMARY,
#                     directConnection=True)
db = client.test
collection = db.movies

# Init Redis
r = redis.Redis(host='redis-cache', port=6379, decode_responses=True)

def search_movie(text):
    """
    Search movies by title and sort results by popularity, text score and rating.
    Also return facets for field `genre`, `releaseYear` and `votes`.

    Hint: check MongoDB's $facet stage
    """
    pipeline = [
        # Filtrar por título
        {"$match": {"title": {"$regex": text, "$options": "i"}}},

        # Ordenar por popularidad, text score y rating
        {"$sort": {"popularity": -1, "vote_count": -1, "vote_average": -1}},

        # Limitar los resultados a los primeros 30 para el facet de búsqueda
        {"$facet": {
            "searchResults": [
                #{"$limit": 5},
                {"$project": {"_id":1, "title": 1, "popularity": 1,
                              "poster_path": 1, "vote_count": 1,
                              "vote_average": 1}}
            ],
            "genreFacet": [
                {"$unwind": "$genres"},
                {"$sortByCount": "$genres"}
            ],
            "releaseYearFacet": [
                {"$group": {"_id": {"$year": "$release_date"},
                            "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ],
            "votesFacet": [
                {"$group": {"_id": "$vote_count", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]
        }}
    ]

    # Ejecutar la pipeline de agregación
    results = list(collection.aggregate(pipeline))[0]

    # Devolver el resultado en el formato solicitado
    return {
        "genreFacet": results["genreFacet"],
        "releaseYearFacet": results["releaseYearFacet"],
        "searchResults": results["searchResults"],
        "votesFacet": results["votesFacet"]
    }


def get_top_rated_movies():
    """
    Return top rated 25 movies with more than 5k votes
    """
    cached_data = r.get("top_rated_movies")
    if cached_data:
        return json.loads(cached_data)
    
    top_rate = collection.find({"vote_count": {"$gte": 5000}},
                           {"_id": 1, "poster_path": 1, "release_date": 1,
                            "title": 1, "vote_average": 1,
                            "vote_count": 1}).sort("vote_average", -1).limit(25)
    top_rate_movies = []
    for movie in top_rate:
        top_rate_movies.append(movie)
        
    r.setex("top_rated_movies", 600, json.dumps(top_rate_movies, default=str))
    return top_rate_movies


def get_recent_released_movies():
    """
    Return recently released movies that at least are reviewed by 50 users
    """
    cached_data = r.get("recent_released_movies")
    if cached_data:
        return json.loads(cached_data)

    current_date=datetime.datetime.now()
    released=collection.find({"release_date": {"$lt": current_date},
                              "vote_count":{"$gt": 50}}, 
                                {"_id": 1, "poster_path": 1, "release_date": 1,
                                 "title": 1, "vote_average": 1, "vote_count":1
                                 }).sort("release_date", -1).limit(50)
    released_list=[]
    for movie in released:
        released_list.append(movie)
        
    r.setex("recent_released_movies", 600, json.dumps(released_list, default=str))
    return released_list


def get_movie_details(movie_id):
    """
    Return detailed information for the specified movie_id
    """
    cached_data = r.get("movie_detail_"+str(movie_id))
    if cached_data:
        return json.loads(cached_data)
    
    movie=collection.find_one({"_id": movie_id},{"_id":1, "genres":1,
                                                 "overview": 1, "poster_path": 1,
                                                 "release_date": 1, "tagline": 1,
                                                 "title": 1, "vote_average": 1,
                                                 "vote_count": 1})
    
    r.setex("movie_detail_"+str(movie_id), 600, json.dumps(movie, default=str))
    return movie


def get_similar_movies(movie_id, genres):
    """
    Return a list of movies that are similar to the provided genres.

    Movies need to be sorted by the number genres that match in descending order
    (a movie matching two genres will appear before a movie only matching one). When
    several movies match with the same number of genres, movies with greater rating must
    appear first.

    Discard movies with votes by less than 500 users. Limit to 10 results.
    """
    similar_movies = []
    discard_genres = []
    while len(similar_movies) < 10 and len(genres) > 0:
        limit = 10 - len(similar_movies)
        similar = collection.find({"genres": {"$all": genres},
                                   "vote_count": {"$gt": 500},
                                   "_id": {"$ne": movie_id}},
                                  {"_id": 1, "genres": 1, "poster_path": 1,
                                   "release": 1, "title": 1, "vote_average": 1,
                                   "vote_count": 1}
                                  ).sort("vote_average", pymongo.DESCENDING
                                         ).limit(limit)
        for movie in similar:
            similar_movies.append(movie)

        discard_genres = genres.pop()
    
    return similar_movies


def get_movie_likes(username, movie_id):
    """
    Returns a list of usernames of users who also like the specified movie_id
    """
    return ["username.of.another.student"]


def get_recommendations_for_me(username):
    """
    Return up to 10 movies based on similar users taste.
    """
    return [
        {
            "_id": 496243,
            "poster_path": "/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
            "release_date": datetime.datetime(2019, 5, 30, 0, 0),
            "title": "Parasite",
            "vote_average": 8.515,
            "vote_count": 16430,
        }
    ]
