## get abstracts
import tqdm
import nltk
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)
from itertools import combinations

def parse_interactions(intifle):

    interactions = []
    with open(intifle) as inf:
        for line in inf:
            parts = line.strip().split()
            n1 = parts[7]
            n2 = parts[8]
            if len(n1) > 2 and len(n2) > 2 and n1 != n2:
                interactions.append((n1,n2))
    return interactions


def text_generator(textfiles):

    with open(textfiles) as tfx:
        for line in tfx:
            line = line.strip()
            yield line

            
def parse_hit_list(interactions_file):

    all_interactions = []
    with open(interactions_file) as inf:
        for line in inf:
            parts = line.strip().split(" ")
            parts = [x.lower() for x in parts]
            all_interactions.append(set([parts[0], parts[2]]))
    return all_interactions


def evaluate_int_presence(interactions, abstract, chemicals, pubmed_id):

    chemicals = {x.split(":")[1] for x in set(chemicals)}
    for interaction in interactions:
        all_tokens = set([x for x in nltk.word_tokenize(abstract)])
        geneA, geneB = list(interaction)
        if geneA in all_tokens and geneB in all_tokens:
            print("\t".join(["MATCH", pubmed_id, geneA, geneB]))
        if geneA \
           in chemicals and geneB in chemicals:
            print("\t".join(["MATCH", pubmed_id, geneA, geneB]))

            
def parse_synonyms(syn_path):

    syn_map = defaultdict(list)
    with open(syn_path, "r", encoding="utf-8") as sp:
        for line in sp:
            parts = line.strip().split("\t")
            for el in parts[1].split(","):
                syn_map[parts[0]].append(el)
    return syn_map


def enrich_hit_list(hit_list, synonyms):

    final_hit_list = []
    for el in hit_list:
        ia, ib = el
        final_hit_list.append(set([ia, ib]))
        if ib in synonyms:
            syn_list = synonyms[ib]
            for el in syn_list:
                final_hit_list.append(set([ia, el]))

        if ia in synonyms:
            syn_list = synonyms[ia]
            for el in syn_list:
                final_hit_list.append(set([el, ib]))
    return final_hit_list
        
            
if __name__ == "__main__":
    import glob
    import pubmed_parser as pp
    import argparse
    from collections import defaultdict
    
    parser = argparse.ArgumentParser()    
    parser.add_argument("--text_base",default="../data_texts/pubmed.txt", type = str)
    parser.add_argument("--annotation_type",default="chemicals", type = str)
    parser.add_argument("--xml_file",default="../pubmed_xml/pubmed22n0088.xml.gz", type = str)
    parser.add_argument("--hit_list",default="../hitlists/interactions_v2.txt", type = str)
    parser.add_argument("--synonyms_map",default="./synonyms.tsv", type = str)
    parser.add_argument("--database",default="medline", type = str)
    args = parser.parse_args()

    hit_list = parse_hit_list(args.hit_list)
    synonyms = parse_synonyms(args.synonyms_map)
    hit_list = enrich_hit_list(hit_list, synonyms)
    weighted_links = {}
    pmid_to_mesh = defaultdict(set)
    
    try:

        if args.database == "medline":
            dict_out = pp.parse_medline_xml(args.xml_file)
            
        else:
            dict_out = pp.parse_pubmed_paragraph(args.xml_file)

        for enx, paper in enumerate(dict_out):

            if "text" in paper.keys():

                # introduce as abstract a given paragraph -> to not need to change things downstream
                paper['abstract'] = paper['text']
                
            if not 'abstract' in paper.keys():
                continue

            if not paper['abstract']:
                continue

            #print(paper['abstract'])
            sentence = paper['abstract']
            
            pid = paper['pmid']

            chemicals = set()
            if "mesh_terms" in paper:
                if type(paper['mesh_terms']) == float or type(paper['mesh_terms']) == float:
                    continue

                chemicals1 = paper['chemical_list'].split(";")
                chemicals2 = paper['mesh_terms'].split(";")
                
                chemicals = list(set(chemicals1+chemicals2))
                chemicals = [x for x in chemicals if x != ""]
            
                if len(chemicals) == 0:
                    continue
                    
                if paper['delete']:
                    continue

            evaluate_int_presence(hit_list, sentence, chemicals, pid)
            
    except Exception as es:
        print(es,"invalid gzipped PubMed base.")
