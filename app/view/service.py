import datetime
import pymongo
from pymongo import MongoClient, ReadPreference
import redis

# Init MongoDB
client = MongoClient("mongodb://mongo2/db:27017",
                     #replicaSet="myReplicaSet",
                     read_preference=ReadPreference.PRIMARY,
                     directConnection=True)
db = client.test
collection = db.movies

# Init Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

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
    return [
        {
            "_id": 238,
            "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "release_date": datetime.datetime(1972, 3, 14, 0, 0),
            "title": "The Godfather",
            "vote_average": 8.707,
            "vote_count": 18677,
        },
        {
            "_id": 278,
            "poster_path": "/lyQBXzOQSuE59IsHyhrp0qIiPAz.jpg",
            "release_date": datetime.datetime(1994, 9, 23, 0, 0),
            "title": "The Shawshank Redemption",
            "vote_average": 8.702,
            "vote_count": 24649,
        },
    ]


def get_recent_released_movies():
    """
    Return recently released movies that at least are reviewed by 50 users
    """
    return [
        {
            "_id": 1151534,
            "poster_path": "/rpzFxv78UvYG5yQba2soO5mMl4T.jpg",
            "release_date": datetime.datetime(2023, 9, 29, 0, 0),
            "title": "Nowhere",
            "vote_average": 7.895,
            "vote_count": 195,
        },
        {
            "_id": 866463,
            "poster_path": "/soIgqZBoTiTgMqUW0JtxsPWAilQ.jpg",
            "release_date": datetime.datetime(2023, 9, 29, 0, 0),
            "title": "Reptile",
            "vote_average": 7.354,
            "vote_count": 65,
        },
    ]


def get_movie_details(movie_id):
    """
    Return detailed information for the specified movie_id
    """
    return {
        "_id": 238,
        "genres": ["Drama", "Crime"],
        "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional "
        "Italian-American Corleone crime family. When organized crime "
        "family patriarch, Vito Corleone barely survives an attempt on "
        "his life, his youngest son, Michael steps in to take care of the "
        "would-be killers, launching a campaign of bloody revenge.",
        "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "release_date": datetime.datetime(1972, 3, 14, 0, 0),
        "tagline": "An offer you can't refuse.",
        "title": "The Godfather",
        "vote_average": 8.707,
        "vote_count": 18677,
    }


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
    while len(similar_movies) < 10:
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
