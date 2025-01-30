FROM python:3.12-alpine

ADD *.whl /tmp
RUN --mount=type=cache,target=/root/.cache/  pip install /tmp/cattle_grid*.whl
