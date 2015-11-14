# kicker-scorer
REST-full web service to track kicker score

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
