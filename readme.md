# Docker must be running before starting these instructions
`docker ps # from a terminal should show some output`

# in terminal you will leave open to run the server
```
./docker/build_and_tag.sh
./docker/start_app.sh
```

# in another terminal window
```
./docker/exec.sh
flask init-db # only needed once
pytest
```

# visit http://localhost:5000/items in your browser
# Add some items
