FROM mambaorg/micromamba:0.23.3

USER root

COPY client/.devcontainer/environment.yml /tmp/environment.yml


RUN micromamba install -n base -f /tmp/environment.yml -y

ENV PYTHONPATH "${PYTHONPATH}:/"

