FROM python:3.9-alpine3.13
LABEL maintainer="jblancocas"

# Output will be printed directly to the console.
# So we can see the logs as they are running
ENV PYTHONBUFFERED 1

     #local machine     #docker image 
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# This runs a command on the alpine image when building
# We could use several RUN statements for each command, (each RUN is a layer image)
# but this way is more lightweight and efficient
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# python -m venv /py -> creates a virtualenv inside docker image. needed? not really,
#   but there could be some conflict with project dependencies and base image python 


ENV PATH="/py/bin:$PATH"

USER django-user