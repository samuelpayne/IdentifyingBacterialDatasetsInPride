import xml.etree.ElementTree as ET
import urllib.request as urllib2 #I'm importing it as a different name so that the code i copied online works without the lazy renaming things

#this is a rough set of functions used in identifying the taxonomy for a (genus, species)
#we are using NCBI's webservidces, and documentatio about those can be found 


"""

NCBI API:
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term=Homo%20sapiens
returns structured
<eSearchResult>
    <IdList>
        <Id>9606</Id>

Then
http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=9606&retmode=xml
returns structured 
<TaxaSet>
    <Taxon>
        <Lineage>cellular organisms; Eukaryota; ..... Hominoidea; Hominidae; Homininae; Homo</Lineage>

I can parse that quickly just looking for the second term

"""


def IsBacteriaTaxonomyQuery(Genus,Species):
    #1. using the input genus and species, get me a taxonomy ID
    # noting that some things are not appropriately formatted and therefore a return of '0' is a failure
    TaxonID = GetTaxonIDFromGenusSpecies(Genus, Species)
    if TaxonID == 0:
        #using the information given to me, I can't affirm that it is a bacterium
        #largely because you failed in giving me a good (Genus, Species)
        return 0 
    IsBacteria = TestIsBacteriaWithTaxonID(TaxonID)
    return IsBacteria


def TestIsBacteriaWithTaxonID(TaxonID):
    # Now get the lineage tree
    url2 = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=%s&retmode=xml'%TaxonID
    #print(url2)
    req = urllib2.Request(url2)
    resp = urllib2.urlopen(req).read()
    #for XML structure, see comment in markdown above
    root = ET.fromstring(resp)
    Taxon = root.find('Taxon')
    Lineage = Taxon.find("Lineage")
    if Lineage.text == None:
        #no lineage. Virsuses have this problem.
        return 0
    LineageArray = Lineage.text.split(";")
    if len(LineageArray) < 2:
        #there are some taxonomies which have a lineage 'unclassified sequences' instead of the nice
        # semi-colon separated list. So the text.split(";")
        return 0
    Kingdom = LineageArray[1].strip() # i do a strip, because the native value is ' Eukaryota' with a leading space
    if Kingdom == "Bacteria":
        return 1
    else:
        return 0
   

def GetTaxonIDFromGenusSpecies(Genus,Species):
    Space = "%20"
    FillString = "%s%s%s"%(Genus,Space,Species)
    #1. using a text string for genus and species, get the integer taxID
    url1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term=%s"%FillString
    #print(url1)
    req = urllib2.Request(url1)
    resp = urllib2.urlopen(req).read()
    root = ET.fromstring(resp)
    #for the xml structrue, see comment in markdown above
    IdList = root.find("IdList")
    Id = IdList.find("Id")
    if Id == None:
        #some entries in PRIDE have a species listed as 'human gut' or other nonsense
        #so this returns a blank IdList tag "<IdList/>" which does not have an <Id> child
        return 0
    TaxonID = Id.text
    return TaxonID

def GetTaxonIDFromSingleWord(word):
    #sometimes you don't have a genus and species. sometimes all you have is 'Brucella'
    #let's see if we can get something with that
    #0. Now sometimes people are silly and put things in parenthesis after your single word.
    ## people who enter Pachycladon(Enysii).  We just have to quit doing that. So let's strip it all out
    SingleWord = word
    ParenLocation = word.find("(")
    if ParenLocation > -1:
        #now parse that junk out
        SingleWord = SingleWord[:ParenLocation]


    #1. using a text string, get the integer taxID
    url1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term=%s"%SingleWord
    #print(url1)
    req = urllib2.Request(url1)
    resp = urllib2.urlopen(req).read()
    root = ET.fromstring(resp)
    #for the xml structrue, see comment in markdown above
    IdList = root.find("IdList")
    Id = IdList.find("Id")
    if Id == None:
        #some entries in PRIDE have a species listed as 'human gut' or other nonsense
        #so this returns a blank IdList tag "<IdList/>" which does not have an <Id> child
        return 0
    TaxonID = Id.text
    return TaxonID
