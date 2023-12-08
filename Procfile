# Heroku apps include a Procfile that specifies the commands that are executed by the app on startup
#
# https://devcenter.heroku.com/articles/procfile

web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}