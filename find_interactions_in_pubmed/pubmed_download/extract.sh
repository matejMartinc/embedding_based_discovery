
OUT_ID="RUN2"

ls ../pubmed_xml/*.gz | mawk '{print "python3 _pubmed.py --database medline --xml_file "$1}' | parallel --progress | grep 'MATCH' > ../outputs/abstracts$OUT_ID.tsv

# Parse the OA part
#bash parse_oa.sh

ls ../pubmed_oa_parsed_xml/*.gz | mawk '{print "python3 _pubmed.py --database pubmed --xml_file "$1}' | parallel --progress | grep 'MATCH' > ../outputs/full$OUT_ID.tsv
