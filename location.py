import pandas as pd
import params
from math import exp
from collections import OrderedDict

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
        self.EOQ = None
        self.alpha = None  # rate at which replenishment lead-time phases transition
        self.beta = None   # rate at which replenishment lead-time phases transition
        self.KQmax = None  # the upper bound on state dimension 2
        self.KEmax = None  # the upper bound on state dimension 3
        self.Istar = None  # largest inventory value at location that allows a replenishment or reserve restoration decision
        self.Imax = None   # the upper bound on state dimension 1
        self.location_links = []  # this will be changed to an ordered dictionary during setup
    
    def setAlpha(self, alpha=None):
        if alpha is not None:
            self.alpha = alpha
        else:
            self.alpha = 5.0
        
    def setBeta(self, beta=None):
        if beta is not None:
            self.beta = beta
        else:
            self.beta = 5.0
        
    def setEOQ(self, EOQ=None):
        if EOQ is not None:
            self.EOQ = EOQ
        else:
            self.EOQ = 1


    def setKQmax(self, KQmax=None):
        if KQmax is not None:
            self.KQmax = KQmax
        else:
            self.KQmax = 5

    
    def setKEmax(self, KEmax=None):
        if KEmax is not None:
            self.KEmax = KEmax
        else:
            self.KEmax = 4
    
        
    def setIstar(self, Istar= None):
        demand = self.demand_internal + self.demand_external
        if Istar is not None:
            self.Istar = Istar
        else:
            x = 0
            p = exp(-demand)
            cump = p
            while cump < params.PDTUSA_HIGH:
                x += 1
                p = p * demand / x
                cump += p        
            self.Istar = x + 1
            
            
    def setImax(self, Imax=None):
        if Imax is not None:
            self.Imax = Imax
        else:
            self.Imax = int(1.5 * self.Istar + self.EOQ + 1)
        print(self.location, (self.demand_internal+self.demand_external), self.Istar, self.Imax)
