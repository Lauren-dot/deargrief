# This file establishes the python container for our working environment
# This is where - in the real world - we would establish a variety of working/staging environments

# pull official base image
FROM python:3.9.5

# set work directory
WORKDIR /usr/Dear_Grief

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/Dear_Grief/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/Dear_Grief/