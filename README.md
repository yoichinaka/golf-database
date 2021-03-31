# Golf score Backend
This is a database and API for golfer.
Golf player can add his name and his image_file.
Then the player can store golf score, course name and date for every golf plays.
Golf Course Manager can add course name, state and image link. 

The URL is https://golf-database.herokuapp.com.

## database structure


### player table

| id | name    | user_id                        | image_link |
| -- | ------- | ------------------------------ | ---------- |
| 1  | player1 | auth0¥6056a19f618f4a00718103c2 | www1       |
| 2  | player2 | auth0¥6056c9916ee8f20068ca54ac | www2       |


 user_id comes from JWT token issued by Auth0 to identify the player.

### course table

| id |   name    |  state   | image_link |
| -- | --------- | -------- | ---------- |
|  1 | TokyoCC   | Tokyo    | www1 |
|  2 | HakoneCC  | Kanagawa | www2 |

### score table

| id | player_id | course_id | score |   date   
|--- | --------- | --------- | ----- | ------- 
  1 |         1 |         2 |    90 | 20210210
  2 |         2 |         1 |   110 | 20210220

player_id is a foreign key from player table.
course_id is a foreign key from course table.

## API document
### The list of Endpoints
    GET '/players'
    POST '/players'
    GET '/courses'
    POST '/courses'
    GET '/scores'
    GET '/players/<int:player_id>/scores'
    POST '/players/<int:player_id>/scores'
    PATCH '/players/<int:player_id>/scores/<int:score_id>'
    DELETE '/players/<int:player_id>/scores/<int:score_id>'

GET '/players'
- Fetches a list of all players, 
- Request Arguments: None
- Returns: lists of all players data which inclued id, name and image_link 
        "players": [
        [
            "1", player1", "www1"
        ],
        [
            "2", "player2", "www2"
        ]]

POST '/players'
- create a new player with his name and image_link.
  Then it is saved in the database.
- Permissions: `post:player` which is assigned to role 'Golf_Player' is required.
- Request Arguments: None
- Returns : added players name

GET '/courses'
- Fetches a list of all players, 
- Request Arguments: None
- Returns: lists of all courses data which inculed course_id, name, state, image_link .
    "courses": [
        [
            "1", "TokyoCC", "Tokyo", "www1"
        ],
        [
            "2", "HakoneCC", "Kanagawa","www2"
        ]]

POST '/courses'
- create a new course with its name and image_link.
  Then it is saved in the database.
- Permissions: `post:course` which is assigned to role 'Golf_Course_Manager' is required.
- Request Arguments: None
- Returns : added course name

GET '/scores'
- Fetches a list of all score data, 
- Request Arguments: None
- Returns: lists of all score data which include score_id, player_id, course_id, score and date.
     "scores": [
        [
            "1", "1", "2", "90", "20210210"
        ],
        [
            "2", "2", "1", "110", "20210220"
        ]]

GET '/players/<int:player_id>/scores'
- Fetches a list of scores which belong to player_id. 
- Request Arguments: player_id
- Returns: lists of all scores which belong to player_id. 
   Score iucludes score_id, player_id, course_id, score and date.
     "scores": [
        [
            "1", "1", "2", "90", "20210110"
        ]]

POST '/players/<int:player_id>/scores' 
- create a new score which belong to player_id. This requires player_id, course_id, score and date. 
- Permissions: `post:player` which is assigned to role 'Golf_Player' is required.
  Endpoint checks if player_id is same as player_id come from JWT payload
    if they are not same, abort.
- Request Arguments: player_id
- Returns : added score

PATCH '/players/<int:player_id>/scores/<int:score_id>'
- update the scores_id which belongs to player_id. This requires player_id, course_id, score and date.  
- Permissions: `post:player` which is assigned to role 'Golf_Player' is required.
  Endpoint checks if player_id is same as player_id come from JWT payload
    if they are not same, abort.
- Request Arguments: player_id
- Returns : added score

DELETE '/players/<int:player_id>/scores/<int:score_id>' 
- Delete a score from database. 
- Permissions: `post:player` which is assigned to role 'Golf_Player' is required.
  Endpoint checks if player_id is same as player_id come from JWT payload
    if they are not same, abort.
- Request Arguments: player_id and score_id
- Returns: deleted score_id

## Roles, permission and JWT token

    Golf_Course_Manager
        Can add course
        Permission is `post:course`
        JWT token is saved in setup.sh.

    Golf_Player
        Can add player
        Can add, update, delete scores
        Permissions are post:player` and  `post_delete_update:score`
        player1 and player2 JWT token is saved in setup.sh.

## Getting Started

## Python 3.8.5

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain. the domain name should be written in setup.sh file.
    the domain name is 'dev-awrgnugr.jp.auth0.com' in this repo.
3. Create a new, single page web application. 
    the application name is 'Golf'
4. Create a new API. the API name is 'Golf'.
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `post:course`
    - `post:player`
    - `post_delete_update:score`
6. Create new roles for:
    - Golf_Course_Manager 
        - can `post:course`
    - Golf_Player
        - can `post_delete_update:score` and `post_delete_update:score`

## For local set up

### Postgres server setup on local PC

Go to the Postgres Download page and download Postgres for your machine.

    For MacOS, Postgres is already downloaded. Homebrew is a popular route for installing Postgres. See this gist on installing Postgres via Brew.
     https://gist.github.com/ibraheem4/ce5ccd3e4d7a65589ce84f2a3b7c23a3
    On Linux, you can run apt-get install postgresql

 1. Start postgres server

  ```
  $ pg_ctl -D /usr/local/var/postgres start
  ```
 
 2. create database
  ```
  $ createdb golf_test
  ```
### Virtual Enviornment

install 
```
 % git clone https://github.com/yoichinaka/golf-database.git
```
 Navigate to 'golf-database' directory
```
 % pip install virtualenv
```
set up virtual env as env
```
 % python -m virtualenv env
 % source env/bin/activate
```
### PIP Dependencies
```
 % pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### set environment
```
% source setup.sh
```
### Running the server locally
```
% flask run
```
to check if it works
```
% curl localhost:5000/players
```

### Unit test ###
Unit test does the test for all endpoints with Pass and Fail test.
To do Unit test
```
% dropdb golf_test
% createdb golf_test
```
set up the database for testing 
```
% psql golf_test < golf_test.psql 
```
```
% python test_flaskr.py
```

## Implement to Heroku server
- Create Heroku account

- install Heroku CLI by
```
% brew tap heroku/brew && brew install heroku
% heroku login 
```
1. Create an application on Heroku
 ` % heroku create golf-database ` 
   'golf-database' is a name of application. 
  Then get URL of application and git URL
   https://golf-database.herokuapp.com
   https://git.heroku.com/golf-database.git

2. Create postgres database addon on Heroku
 `% heroku addons:create heroku-postgresql:hobby-dev --app ` golf-database

3. Set up the envrionmental variables on Heroku dashboard
 Go to Heroku dashbord using web brawser.
 Click Golf-database >> settings tab >> Reveal Config Vars
  Set 
   - ALGORITHMS = ['RS256']
   - API_AUDIENCE = Golf
   - AUTH0_DOMAIN = dev-awrgnugr.jp.auth0.com
   - DATABASE_URL is set by Heroku automatically

5. Git commit on local and push it to Heroku git server.
```
  % git init
  % git add .
  % git commit -m '1st commit'
  % git push heroku master
```

6. Now golf-database api has been deplyed on Heroku server.
To check this server
` % curl https://golf-database.herokuapp.com/players `
 and you can check the other api fucntions.

