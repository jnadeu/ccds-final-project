#!/bin/bash
sleep 10

mongoimport --uri mongodb://app:secret@mongo_db:27017 --db test --collection movies --drop < mongodb/TMDB_dataset.json

mongosh --host mongo_db:27017 -u app -p secret --eval 'db.movies.updateMany({}, [ { $set: { release_date: { $convert: {input: "$release_date", to: "date", onError: null} } } } ] )'

