import nltk





def get_datasets():

    pd_file = open('datasets/pd.txt', 'w', encoding="utf8")
    cr_file = open('datasets/cr.txt', 'w', encoding="utf8")

    with open('datasets/C_merged_PD_in_CR_trunc_clean.txt', 'r', encoding='utf8') as f:
        vocab = {}
        for line in f:
            if len(line.strip()) > 0:
                id = line.split()[0]
                c = line.split()[1]
                text = " ".join(line.split()[2:]).strip()
                text = " ".join(nltk.wordpunct_tokenize(text)).lower()

                if c == "!CR":
                    cr_file.write(text + '\n')
                    words = text.split()
                    for w in words:
                        if w in vocab:
                            vocab[w][0] += 1
                        else:
                            vocab[w] = [1, 0]
                elif c == "!PD":
                    pd_file.write(text + '\n')
                    words = text.split()
                    for w in words:
                        if w in vocab:
                            vocab[w][1] += 1
                        else:
                            vocab[w] = [0, 1]
        pd_file.close()
        cr_file.close()
    words = []
    for word, freq in vocab.items():
        if freq[0] > 0 and freq[1] > 2:
            words.append((word, freq[0], freq[1]))

    words = sorted(words, reverse=True, key= lambda x: x[-1])
    train = open('datasets/en_en_dict_train.txt', 'w', encoding='utf8')
    test = open('datasets/en_en_dict_test.txt', 'w', encoding='utf8')

    counter = 0
    for w, f1, f2, in words[:5000]:
        if counter % 3 == 0:
            test.write(w + '\t' + w + '\n')
        else:
            train.write(w + '\t' + w + '\n')
        counter += 1
    train.close()
    test.close()

if __name__ == '__main__':
    get_datasets()















