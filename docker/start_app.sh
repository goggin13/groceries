docker run \
  -it \
  -p 5000:5000 \
  --name grocery-list-web \
  -v $HOME/Documents/projects/grocery-list:/var/www/grocery-list \
  --rm \
  goggin13/grocery-list
