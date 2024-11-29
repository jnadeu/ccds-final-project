
  
  
  docker-compose -f registry-compose.yml up
  docker tag alpine localhost:5000/alpine\n
  docker pull alpine:latest
  docker tag alpine localhost:5000/alpine\n
  docker push localhost:5000/alpine\n
  curl http://localhost:5000/v2/_catalog\n