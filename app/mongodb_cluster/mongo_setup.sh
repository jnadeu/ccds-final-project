#!/bin/bash
sleep 10


mongosh --host mongo1:27017 <<EOF
  var cfg = {
    "_id": "myReplicaSet",
    "version": 1,
    "members": [
      {
        "_id": 0,
        "host": "mongo1:27017",
        "priority": 2
      },
      {
        "_id": 1,
        "host": "mongo2:27017",
        "priority": 0
      },
      {
        "_id": 2,
        "host": "mongo3:27017",
        "priority": 0
      }
    ]
  };
  rs.initiate(cfg);
EOF


mongosh --host mongo1:27017 --db test --collection movies --drop < /mongodb_cluster/TMDB_dataset.json

mongosh --host mongo1:27017 --eval 'db.movies.updateMany({}, [ { $set: { release_date: { $convert: {input: "$release_date", to: "date", onError: null} } } } ] )'

