##container for data on a PRIDE submission. Just so I can play around with it.

#a container for projects that I am interested in.
class PrideSubmission:
    #The JSON  is a dictionary and looks like
    #        {'projectDescription': 'Drought stress is a major problem around the world and although ', 
    #        'numAssays': 0, 'instrumentNames': ['Q Exactive'], 'projectTags': ['Biological'], 
    #        'accession': 'PXD005238', 'tissues': ['leaf'], 'species': ['Malus baccata'], 
    #         ... MORE STUFF ...
    #        }

    def __init__(self, JSONFromPride):
        self.Accession = JSONFromPride['accession']
        self.Description = JSONFromPride['projectDescription']
        self.TaxonID = [] #since the species is a list, this also has to be a list
        self.OrgList = JSONFromPride['species'] # this is a list, potentially of len 1. but a list none-the-less
        self.NumProteins = 0 #to be set later
        self.Instruments = JSONFromPride['instrumentNames']
        
    def SetNumProteins(self, num):
        self.NumProteins = num

    def SetTaxonID(self, id):
        self.TaxonID = id

    def GetOrgList(self):
        #using Get functions is a nice convention.
        return self.OrgList

    def GetAccession(self):
        return self.Accession

    def GetInstrument(self):
        return self.Instruments

    def GetDescription(self):
        return self.Description
        
