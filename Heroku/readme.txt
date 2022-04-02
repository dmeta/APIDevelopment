heroku create fastapi-damianmeta

heroku buildpacks:set heroku/python

heroku create --buildpack https://git.heroku.com/fastapi-damianmeta.git

git push heroku main

heroku ps:scale web=1



https://git.heroku.com/fastapi-damianmeta.git
