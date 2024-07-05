# download and parse pubmed.
mkdir -p ../pubmed_xml
mkdir -p ../pubmed_xml_oa;
cd ../pubmed_xml;

# The updated files.
#wget -rv --no-parent --no-directories ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles > ../downloadout.log 2> ../downloaderr.log;

# Donwnload the baseline.
#wget -rv --no-parent --no-directories ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline > ../downloadout.log 2> ../downloaderr.log;

cd ../pubmed_xml_oa;
wget -rv --no-parent --no-directories ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/xml > ../downloadout.log 2> ../downloaderr.log
rm *.md5;

wget -rv --no-parent --no-directories ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/xml > ../downloadout.log 2> ../downloaderr.log

wget -rv --no-parent --no-directories ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_other/xml > ../downloadout.log 2> ../downloaderr.log
rm *.md5;

echo "Done";
