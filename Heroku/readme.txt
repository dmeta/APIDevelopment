heroku create fastapi-damianmeta

heroku buildpacks:set heroku/python

heroku create --buildpack https://git.heroku.com/fastapi-damianmeta.git

git push heroku main

heroku ps:scale web=1


heroku addons:create heroku-postgresql:hobby-dev

https://git.heroku.com/fastapi-damianmeta.git
https://fastapi-damianmeta.herokuapp.com/
