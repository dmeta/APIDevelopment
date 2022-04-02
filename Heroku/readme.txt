heroku create fastapi-damianmeta

heroku buildpacks:set heroku/python

heroku create --buildpack https://git.heroku.com/fastapi-damianmeta.git

git push heroku main



https://git.heroku.com/fastapi-damianmeta.git
