# VITC-Ride-Share
##How to Contribute ?
###1)Fork the main repository
###2)Clone the forked repository from https://github.com/<your name>/<forked repo>
###3)After cloning, in the terminal of the local computer  

  ```
  git remote add origin https://github.com/<your name>/<forked repo>
  git remote add upstream https://github.com/<Person who owns the main repository>/<Repo Name that is forked from the owner>
  ``` 
  ###Eg:
  ```
    git remote add origin https://github.com/TestUser/VITC-Ride-Share ------->User who forked this repository from owner
    git remote add upstream https://github.com/ShyamSundhar1411/VITC-Ride-Share ------->The user who owns this repository
  ```
 ### 4)Create a new branch in local computer (Do not push to origin with master/main branch)
  ```
      git checkout -b "New branch"
  ```
 ### 5)Pushing through new branch
  ```
    git push -u origin New Branch
  ```
  6)Open a pull request 
 ##How to sync the forked repository with main repository ?
  ###1)Fetch it from the upstream in your terminal and merge it
  ```
    git checkout branch name
    git fetch upstream (or pull can also be used git pull)
    git merge master
  ```
  ##How to run the project ?
  ###1)After cloning make use of the pipenv(virtual environment)
  ```
  pipenv install (make sure to pip install pipenv)
  and to activate once its done
  pipenv shell
  ```
  ###2)Sync environment packages
  ```
  pipenv sync
  ```
  ###3)Execute the following commands in order
  ```
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
  ```
  4)Open localhost:8000
