
import numpy as np
import io
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import nltk


def get_gene_list():
    with open('datasets/C_merged_PD_in_CR_trunc_clean_synonyms_B_genes_trunc.txt', 'r', encoding='utf8') as f:

        vocab = defaultdict(int)
        for line in f:
            if len(line.strip()) > 0:
                c = line.split()[1]
                text = " ".join(line.split()[2:]).strip()
                text = " ".join(nltk.wordpunct_tokenize(text)).lower()
                if c == "!pd":
                    words = text.split()
                    for w in words:
                        vocab[w] += 1

        vocab = sorted(list(vocab.items()), reverse=True, key=lambda x: x[1])
        vocab = [x[0] for x in vocab]
        return set(vocab)


def load_fasttext(emb_path, nmax=1000000):
    vectors = []
    word2id = {}
    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for i, line in enumerate(f):
            word, vect = line.rstrip().split(' ', 1)
            vect = np.fromstring(vect, sep=' ')
            assert word not in word2id, 'word found twice'
            vectors.append(vect)
            word2id[word] = len(word2id)
            if len(word2id) == nmax:
                break
    id2word = {v: k for k, v in word2id.items()}
    embeddings = np.vstack(vectors)
    return embeddings, id2word, word2id

def get_emb(word, emb, word2id):
    avg_emb = []
    for word_part in word.split():
        word_emb = emb[word2id[word_part.lower()]].tolist()
        avg_emb.append(word_emb)
    avg = np.average(np.array(avg_emb), axis=0)
    word_emb = avg
    return word_emb

def embeds_to_dict(emb, word2id):
    dict = {}
    words = list(word2id.items())
    for w, id in words:
        dict[w] = emb[id]
    return dict

def get_most_similar(word, word_emb, embeds, n = 10, word_list=[]):
    neigh = []
    items = list(embeds.items())
    values = [v for k, v in items]
    keys = [k for k, v in items]
    #print(np.array(values).shape)
    cs = cosine_similarity(word_emb.reshape(1, -1), np.array(values)).squeeze()
    for i in range(len(keys)):
        neigh.append((keys[i], cs[i]))
    neigh = sorted(neigh, key=lambda x: x[1], reverse=True)
    counter = 0
    word_results = []
    emb_results = []
    for w, score in neigh:
        if word.lower() not in w.lower() and w.lower() not in word.lower():
            if len(word_list) == 0 or w in word_list:
                if counter >= n:
                    break
                counter += 1
                word_results.append((w, score))
                emb_results.append(embeds[w])
    return word_results, emb_results


def get_all_relations(embeds, word2id):
    gene_list = get_gene_list()
    words = list(word2id.keys())
    words = [x for x in words if x in gene_list]
    diffs = {}
    print('calculating all differences: ', len(words) * len(words))
    counter = 0

    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            word_1 = words[i]
            word_2 = words[j]
            emb_1 = embeds[word2id[word_1]]
            emb_2 = embeds[word2id[word_2]]
            diffs[word_1 + '-' + word_2] = emb_1 + emb_2
            #diffs[word_2 + '-' + word_1] = emb_2 + emb_1
            counter += 1
            if counter % 1000000 == 0:
                print('processing diff: ', counter)
    print('Done')
    return diffs




def get_same_relations_in_domain_2(embeds_1, word2id_1, relations_1, embeds_2, word2id_2):

    diffs = get_all_relations(embeds_2, word2id_2)

    for rel in relations_1:
        el1, el2 = rel
        emb_1 = get_emb(el1, embeds_1, word2id_1)
        emb_2 = get_emb(el2, embeds_1, word2id_1)
        emb_rel = emb_1 + emb_2
        word_res, emb_res = get_most_similar(el1 + '-' + el2.lower(), emb_rel, diffs, n=10, word_list=[])
        print("Circadian rhythm: ", el1 + ' rel. ' + el2)
        print("Most similar plant defense rel:\n")
        print('rank\trelation\tcosine sim.')
        for idx, w in enumerate(word_res):
            score = w[1]
            w = w[0]
            w = w.replace('-', ' rel. ')
            print(str(idx + 1) + '.' + '\t' + w + "\t{:.4f}".format(score))
        print('------------------------------------------')
        print()


def get_analogy(word_1, embeds_1, word2id_1, genes_1, word_2, embeds_2, word2id_2):

    emb_1 = get_emb(word_1, embeds_1, word2id_1)
    emb_2 = get_emb(word_2, embeds_2, word2id_2)
    embeds_2 = embeds_to_dict(embeds_2, word2id_2)

    for gene in genes_1:
        emb_gene = get_emb(gene, embeds_1, word2id_1)
        emb_result = emb_1 + emb_gene - emb_2
        word_res, emb_res = get_most_similar(word_2.lower(), emb_result, embeds_2, n=10, word_list=get_gene_list())
        print("Circadian rhythm domain: ", word_1 + ' rel. ' + gene.lower())
        print("Most similar in plant defense domain:\n")
        print('rank\trelation\tcosine sim.')
        for idx, w in enumerate(word_res):
            score = w[1]
            w = w[0]
            w = 'plant defense rel. ' + w
            print(str(idx + 1) + '.' + '\t' + w + "\t{:.4f}".format(score))
        print('------------------------------------------')
        print()


if __name__ == '__main__':
    word_1 = 'circadian rhythm'
    word_2 = 'plant defense'
    genes_1 = ['CCA1', 'LHY', 'TOC1', 'PRR1', 'GI', 'LNK1', 'PRR5', 'ELF4', 'PRR9', 'PRR7',
               'PCL1', 'ELF3', 'ELF4', 'transcription translation negative feedback loops',
               'TTFL', 'negative feedback loop', 'oscillator', 'clock']

    relations_1 = [['CCA1', 'PRR7'],
                   ['CCA1', 'PRR9'],
                   ['CCA1', 'PRR5'],
                   ['CCA1', 'TOC1'],
                   ['CCA1', 'ELF3'],
                   ['CCA1', 'ELF4'],
                   ['CCA1', 'LUX'],
                   ['LHY', 'PRR7'],
                   ['LHY', 'PRR9'],
                   ['LHY', 'PRR5'],
                   ['LHY', 'TOC1'],
                   ['LHY', 'ELF3'],
                   ['LHY', 'ELF4'],
                   ['LHY', 'LUX']]


    path_1 = 'embeddings/vectors-cr.txt'
    path_2 = 'embeddings/vectors-pd.txt'
    nmax = 500000  # maximum number of word embeddings to load
    embeds_1, id2word_1, word2id_1 = load_fasttext(path_1, nmax)
    embeds_2, id2word_2, word2id_2 = load_fasttext(path_2, nmax)
    get_same_relations_in_domain_2(embeds_1, word2id_1, relations_1, embeds_2, word2id_2)


