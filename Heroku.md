Deployment on Heroku

heroku login
## App name
heroku create pythonapi-adnandmth 
## commit changes to remote repo
git push origin master
## commit changes to heroku repo
git push heroku master
## logs details
heroku logs -t
## check installed addons
heroku addons
## create postgres instance
## https://dashboard.heroku.com/apps/pythonapi-adnandmth/settings
heroku addons:create heroku-postgresql:mini