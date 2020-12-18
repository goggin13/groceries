source docker/common.sh

if docker ps | grep -o grocery-list-web ; then
  docker exec -it grocery-list-web bash
elif docker ps | grep -o grocery-list-console ; then
  docker exec -it grocery-list-console bash
else
  docker run \
    -it \
    --env PORT=5000 \
    -p 5000:5000 \
    --name grocery-list-console \
    -v $LOCAL_VOLUME_PATH:/var/www/grocery-list \
    --rm \
    goggin13/grocery-list \
    bash
fi
