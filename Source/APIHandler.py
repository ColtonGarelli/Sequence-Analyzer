import requests
import urllib3


# UniProt is a source for protein sequences+information

class UniProtAPI:
    """
    The UniprotAPI class communicates with the UniProt RESTful API to query the database,
    parse response information, and create a Sequence object for each set of response information (protein info).
    """

    base_url = "https://www.uniprot.org/uniprot/?query="
    query_url = {"something": "url text", "something else": "another url"}
    column_url = {"a key": "a column with useful info"}
    format_url = "&format="

    def url_constructor(self):
        """
        Creates a URL based on user input for desired sequence parameters.
        :return:
        """
        some_url = "https://www.uniprot.org/uniprot/?query=insulin&" \
                   "sort=score&columns=id,protein names,length&format=tab"

        another_url = "http://www.uniprot.org/uniprot/?query=arabidopsis%20thaliana&sort=score&" \
                      "columns=id,protein names,&format=tab"

        ebi_url = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&protein=Auxin%20Response%20Factor"

        this_request = requests.get(another_url)
        print(this_request.text)

        url = "https://www.uniprot.org/uniprot/?query=insulin&sort=score&columns=entry name,protein names,length&format=tab"
        request = requests.get(url)
        print(request.text)

