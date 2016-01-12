# kicker-scorer
REST-full web service to track kicker score

## Architecture

The end app should have the following layers

              |
          _________
          | nginx |             - container
          ---------
          /       \             - http socket
    ------          ---------
      UI             API (N)    - containers
    ------          ---------
                        |
                    ---------
                        DB      - container
                    ---------

kicker-scorer         - aggregate everything (docker-compose?)
kicker-scorer-load    - nginx container
kicker-scorer-db      - mariadb container
kicker-scorer-api     - flask uwsgi web app container
kicker-scorer-ui      - angular2 static files

## Routes
```
POST	/communities
GET		/communities

POST 	/comminities/NOWORK/players
GET		/communities/NOWORK/players

GET 	/communities/NOWORK/teams
POST 	/communities/NOWORK/teams 				- create a team

POST	/communities/NOWORK/matches				- initiate match for two teams
GET		/communities/NOWORK/matches?filter

PUT 	/matches/3415323/teamName/goal?player=ac	    - update score
PUT 	/matches/3415323/teamLastName/goal    		- update score

GET		/matches/3415323	  					- get match result
```

## How to install

run MariaDB container
```
docker run --name dbserver -v /home/docker/db:/home/docker/db -e MYSQL_ROOT_PASSWORD=test -d mariadb --datadir /home/docker/db
```

run web application (nginx, uwsgi, flask)
```
docker run --name webapp --link dbserver -d -p 80:80 -v /home/docker/logs:/home/docker/logs webapp:latest
```
