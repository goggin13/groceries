if docker ps | grep -o grocery-list-web ; then
  docker exec -it grocery-list-web bash
elif docker ps | grep -o grocery-list-console ; then
  docker exec -it grocery-list-console bash
else
	docker run \
		-it \
    -p 3000:3000 \
		--name grocery-list-console \
		-v $HOME/Desktop/github/groceries:/var/www/grocery-list \
		--rm \
		goggin13/grocery-list \
		bash
fi
