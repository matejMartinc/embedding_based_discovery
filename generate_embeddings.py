import fasttext
import nltk

def make_embeddings(input, output):
    with open(input, "r", encoding="utf8") as f:
        text = " ".join(nltk.wordpunct_tokenize(f.read())).lower()
    filename = input.split('.')[0] + "_preprocessed." +  input.split('.')[1]
    with open(filename, "w", encoding="utf8") as f:
        f.write(text)
    model = fasttext.train_unsupervised(filename, min_count=6, model='skipgram')
    model.save_model(output + ".bin")

make_embeddings('datasets/pd.txt', 'embeddings/pd')
make_embeddings('datasets/cr.txt', 'embeddings/cr')

