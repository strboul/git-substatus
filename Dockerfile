FROM python:3.7-alpine
LABEL MAINTAINER="strboul"
LABEL REPOSITORY="https://github.com/strboul/git-substatus"
LABEL HOMEPAGE="https://github.com/strboul/git-substatus"

RUN apk add --no-cache git

ARG CONTAINER_PATH="/opt/git-substatus/"
RUN mkdir -p "$CONTAINER_PATH"
COPY setup.py README.md "$CONTAINER_PATH"
COPY git_substatus/ "$CONTAINER_PATH"/git_substatus
RUN cd "$CONTAINER_PATH" && pip install .

ENTRYPOINT ["git-substatus"]
