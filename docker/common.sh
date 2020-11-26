if [ "$USER" = "mattgoggin" ]; then
  echo "running on Matt's machine"
  export LOCAL_VOLUME_PATH=$HOME/Documents/projects/grocery-list
else
  echo "running on Kelly's machine"
  export LOCAL_VOLUME_PATH=$HOME/Desktop/github/groceries
fi;
