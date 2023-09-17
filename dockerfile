FROM python:3.11 AS build

# copy project
COPY . /usr/src/app/

WORKDIR /usr/src/app

#  RUN pip install --upgrade pip
RUN pip install gunicorn

# install dependencies --no-cache-dir remove th __pyc
RUN pip install --no-cache-dir -r requirements.txt

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
  