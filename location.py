import pandas as pd
import params
from math import exp

########################################################################
class Location:
    """"""
    locations = None
    all_locations_set = None

    #----------------------------------------------------------------------
    def __init__(self, location):
        self.location = location
        self.primary_zipcodes_demands = {}
        self.prob_inventory_above_reserve = params.PDTUSA_LOW
        self.prob_part_available = params.PDTUSA_LOW
        self.demand_internal = 0.0
        self.demand_internal_high = None
        self.demand_internal_low = None
        self.demand_external = None
        self.demand = None
        self.Istar = None
        
        
    def calculateIstar(self):
        x = 0
        p = exp(-self.demand)
        cump = p
        print(self.location, x, cump, p)
        while cump < params.PDTUSA_HIGH:
            x += 1
            p = p * self.demand / x
            cump += p
        print(self.location, x, cump, p)            
        self.Istar = x
    
        

