source docker/common.sh

docker run \
  -it \
  --env PORT=5000 \
  -p 5000:5000 \
  --name grocery-list-web \
  -v $LOCAL_VOLUME_PATH:/var/www/grocery-list \
  --rm \
  goggin13/grocery-list
