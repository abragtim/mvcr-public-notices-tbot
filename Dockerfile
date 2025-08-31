FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yaml .

RUN conda env create -f environment.yaml

SHELL ["conda", "run", "-n", "mvcr-track-application", "/bin/bash", "-c"]

COPY . .

RUN mkdir -p data/storage

CMD ["conda", "run", "--no-capture-output", "-n", "mvcr-track-application", "python", "tbot.py"]
