from collections import OrderedDict

########################################################################
class Zipcode:
    """"""
    zipcodes = None
    all_zipcodes_set = None
    all_locations_set = None

    #----------------------------------------------------------------------
    def __init__(self, zipcode: str):
        self.zipcode = zipcode
        self.fct: float = None
        self.high: float = None
        self.low: float = None
        self.location_links = []  # this will be changed to an ordered dictionary during setup
        