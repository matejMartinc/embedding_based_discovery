# Embeddinhg based  discovery

## Installation

Experiments were conducted with Python 3.9. First install dependencies:

pip install requirements.txt

Clone Facebook MUSE library into the project:

git clone https://github.com/facebookresearch/MUSE

Go to MUSE/src/utils.py file and in lines 76 and 80 change 'fastText' to 'fasttext' (i.e., change capital T to t) otherwise the code will crash

## How to use it

```
python build_datasets()


python MUSE/supervised.py --src_lang 'cr' --tgt_lang 'pd' --emb_dim 100 --max_vocab -1 --n_refinement 20 --dico_train "datasets/en_en_dict_train.txt" --dico_eval "datasets/en_en_dict_test.txt" --src_emb  'embeddings/cr.bin' --tgt_emb  'embeddings/pd.bin' --cuda 0
```

## Dockerised execution

We have prepared a docker for you that executes and runs the experiments. 

### Build the Docker Image
Run the following command to build the Docker image:

```bash
docker build . -t lbd_embeddings
```
Run the Docker Container
Once the image is built, execute the container using:

```bash
docker run -p 8888:8888 lbd_embeddings
```
You can then access Jupyter Lab in your browser at:

```
http://localhost:8888/lab?token=mysecrettoken
```
This setup ensures a streamlined process for running the experiments.