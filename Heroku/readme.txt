heroku create fastapi-damianmeta

heroku buildpacks:set heroku/python

heroku create --buildpack https://git.heroku.com/fastapi-damianmeta.git

git add .
git commit -am "make it better"
git push heroku main
git push 




heroku addons:create heroku-postgresql:hobby-dev

https://git.heroku.com/fastapi-damianmeta.git
https://fastapi-damianmeta.herokuapp.com/


heroku ps:scale web=1
heroku ps:restart

heroku run "alembic upgrade head"
