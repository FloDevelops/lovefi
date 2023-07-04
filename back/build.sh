docker build -t lovefi-back .
docker run -p 127.0.0.1:8080:8080 -it --rm --name lovefi-back lovefi-back