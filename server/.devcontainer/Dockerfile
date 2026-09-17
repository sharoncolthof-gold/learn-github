FROM mambaorg/micromamba:0.23.3

USER root

COPY server/.devcontainer/environment.yml /tmp/environment.yml

RUN micromamba install -n base -f /tmp/environment.yml -y
# RUN micromamba create -f server/environment.yml -y

ENV PYTHONPATH "${PYTHONPATH}:/"

EXPOSE 8080
