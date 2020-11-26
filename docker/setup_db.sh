source docker/common.sh

docker exec \                
  grocery-list-web \         
  bundle exec rake db:create 
                             
docker exec \                
  grocery-list-web \         
  undle exec rake db:migrate
