# fastapi
## Create an environment
Create a project folder and a .venv folder within:
```sh
py -3 -m venv venv

```
## Activate the environment
Before you work on your project, activate the corresponding environment:
```sh
.venv\Scripts\activate
```
## install FastAPI
```sh
pip install fastapi[all]
```
## Install the Server Program
```sh
pip install "uvicorn[standard]"

```
## OAuth2 with Password (and hashing), Bearer with JWT tokens
### Install python-jose
```sh
pip install "python-jose[cryptography]"
```
### Password hashing
```sh
pip install "passlib[bcrypt]"
```
### Install  PyCryptodome
```sh
pip install pycryptodome
```
### For Sent Mail outlook
```sh
p
```



## After clone project 
``` sh 
pip install -r requirements.txt
pip freeze                                ## To show all
```
## run App
```sh
#uvicorn main:app                          
#uvicorn app.main:app --reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```







route param
posts?limit=10&skip=2&search=to

https://youtu.be/0sOvCWFmrtA?t=39918




…or create a new repository on the command line
echo "# fastapi" >> README.md
  git init
  git add README.md
  git commit -m "first commit"
  git branch -M main
  git remote add origin https://github.com/ristonhen/fastapi.git
  git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/ristonhen/fastapi.git
  git branch -M main
  git push -u origin main