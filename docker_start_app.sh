# docker run \
#   --name grocery-list-web \
#   -v $HOME/Documents/projects/grocery-list:/var/www/grocery-list \
#   --rm \
#   goggin13/grocery-list

docker run \
  -it \
  -p 3000:3000 \
  --name grocery-list-web \
  -v $HOME/Documents/projects/grocery-list:/var/www/grocery-list \
  --rm \
  goggin13/grocery-list \
  bash
