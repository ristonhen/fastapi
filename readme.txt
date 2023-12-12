## Create VM local machine
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
$ pip install fastapi[all]
$ pip install "passlib[bcrypt]"
$ pip install "python-jose[cryptography]"
$ pip freeze                                ## To show all pkg

$ pip install aiosmtplib
$ pip install pycryptodome
$ pip install pywin32

$ pip install -r requirements.txt
$ uvicorn main:app                          ## run App
uvicorn app.main:app --reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## https://docs.sqlalchemy.org/en/14/
$ pip install SQLAlchemy

## https://alembic.sqlalchemy.org/en/latest/front.html#installation
$ pip install alembic
    $ alembic init set_name
    ## set_name go to .env to import Base app.database
    ## find target_metadata = None change to Base.metadata

    ## go to alembic.init find sqlalchemy.url 
        set to sqlalchemy.url = postgresql+psycopg2://postgres:123@localhost:5432/fastapi




fetch("http://localhost:8000/").then(res => res.json()).then(console.log())

#open window go to "Edit the system environment"

route param
posts?limit=10&skip=2&search=to

https://youtu.be/0sOvCWFmrtA?t=39918

#git commit to branch
#https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/git-push-new-branch-remote-github-gitlab-upstream-example

task-4-routers

github@branch/c/remote/push  (new-branch)
git clone https://github.com/ristonhen/fastapi.git
cd git*
git checkout -b task-8-add_alembic

github@branch/c/remote/push (task-2)
git branch -a
touch devolution.jpg
git add .
git commit -m "complet with alembic"
git push --set-upstream origin task-8-add_alembic

github@branch/c/remote/push (new-branch)
touch eden.html
git add .
git commit -m "Completed normal API"
git push origin



### HTTP Request message status code .
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status







…or create a new repository on the command line
echo "# fastapi" >> README.md
git init
git add README.md
git commit -m "Completed"
git branch -M main
git remote add origin https://github.com/ristonhen/fastapi.git
git push -u origin main



…or push an existing repository from the command line
git remote add origin https://github.com/ristonhen/fastapi.git
git branch -M main
git push -u origin main