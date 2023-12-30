## base image from docker hub
FROM python:3.9.7

## specify working directory to simplify the directory selection
WORKDIR /usr/src/app

## copy file from the host to the container directory
COPY requirements.txt ./

## run this command inside the container
## requirements.txt is available in the container after it was copied from local machine
RUN pip install --no-cache-dir -r requirements.txt

## copy all the sources in the directory
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]