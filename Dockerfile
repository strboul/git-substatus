ARG PY_VERSION
FROM python:${PY_VERSION}-alpine
LABEL MAINTAINER="strboul"
LABEL REPOSITORY="https://github.com/strboul/git-substatus"
LABEL HOMEPAGE="https://github.com/strboul/git-substatus"

RUN apk add --update --no-cache --no-progress git

ARG INSTALL_PATH="/opt/git-substatus/"
RUN mkdir -p "$INSTALL_PATH"
COPY setup.py README.md get_version.sh "$INSTALL_PATH"
COPY git_substatus/ "$INSTALL_PATH"/git_substatus
RUN cd "$INSTALL_PATH" && \
  python -m pip install --upgrade pip .
RUN rm -rf "$INSTALL_PATH"

ENTRYPOINT ["git-substatus"]
