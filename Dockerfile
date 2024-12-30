FROM python:3.11.9-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    libsqlite3-dev \
    libbz2-dev \
    libreadline-dev \
    liblzma-dev \
    zlib1g-dev \
    git \
    && python3 -m pip install --upgrade pip \
    && pip install jupyterlab \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN git clone https://github.com/facebookresearch/MUSE.git
RUN sed -i 's/import fastText/import fasttext/' MUSE/src/utils.py
RUN sed -i 's/return fastText\.load_model/return fasttext.load_model/' MUSE/src/utils.py

COPY . /app

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token='mysecrettoken'"]
