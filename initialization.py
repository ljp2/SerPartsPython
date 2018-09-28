from zipcode import Zipcode
from location import Location
import params
import setup


#----------------------------------------------------------------------
def init():
    """"""
    for location in Location.locations.values():
        location.demand_external = 0.0
        location.demand = location.demand_internal
        location.prob_inventory_above_reserve = params.PDTUSA_LOW
        location.prob_part_available = params.PDTUSA_LOW
        
        location.setAlpha()
        location.setBeta()
        location.setEOQ()
        location.setKQmax
        location.setKEmax()
        location.setIstar()
        location.setImax()
        
        
        

    
if __name__ == '__main__':
    part_number = 'PN2'
    setup.setup(part_number)
    init()
