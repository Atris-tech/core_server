## 

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

CREATE DATABASE atris;

CREATE USER 'atris'@'localhost' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON *.* TO 'atris'@'localhost' IDENTIFIED BY '1234';

## Todo 
Remove all redundand azure speech to text service and change it with :- https://github.com/at16k/at16k
