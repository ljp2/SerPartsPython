import pandas as pd
from collections import namedtuple
from collections import OrderedDict

import params

from zipcode import Zipcode
from location import Location
      
########################################################################
LocationLink = namedtuple('LocationLink', ['location', 'cost', 'hours', 'miles'])
    

#----------------------------------------------------------------------
def readForecastFile(part_number: str):
    """
    Read the forecast
    Dummy high and low customer demand based on high customer count percentage
    accumulate demand by zipcode
    return demand by zipcode dataframe
    """
    df = pd.read_csv(params.FORECAST_FILENAME, delimiter='|')
    df = df[df.pn==part_number]
    high_priority_customers = dummyHighPriorityCustomers(df, params.high_customer_pct)
    addHighLowDemandColumns(df, high_priority_customers) 
    
    #
    # accumulate demands and create zipcodes
    # note: after grouping df_forecast index becomes zip_code
    # Determine Zipcode.all_zipcodes_set
    #
    df = df.groupby('zip_code').sum()
    Zipcode.zipcodes = {}
    for row in df.itertuples():
        zipcode = Zipcode(row.Index)
        zipcode.fct = row.fct
        zipcode.high = row.high
        zipcode.low = row.low
        Zipcode.zipcodes[row.Index] = zipcode
    Zipcode.all_zipcodes_set = set(df.index)    
    
    return df
    

#----------------------------------------------------------------------
def dummyHighPriorityCustomers(df, high_customer_pct):
    """
    dummy high priority custormers as high_customer_pct
    """
    x = df.groupby(['cust']).sum().sort_values(by=['fct'], ascending=False )
    highcnt = int(len(x) * high_customer_pct)
    high_priority_customers = set(x.nlargest(highcnt, 'fct').index) 
    return high_priority_customers


#----------------------------------------------------------------------
def addHighLowDemandColumns(df, high_priority_customers):
    """"
    add high low customer demand columns to dataframe
    """
    highs = []
    lows = []
    for row in df.itertuples():
        if row.cust in high_priority_customers :
            highs.append(row.fct)
            lows.append(0.0)
        else:
            lows.append(row.fct)
            highs.append(0.0)
    
    df['high'] = highs
    df['low'] = lows
    

#----------------------------------------------------------------------
def readTransportationLinksFile(df_forecast):
    """
    Read the transportation links file
    Set relevant locations for each zipcode
    Add location link information to zipcodes
    Set Zipcode.all_locations_set
    Set zipcode-location TransportationCosts
    """
    df = pd.read_csv(params.TRANSPORTATION_LINKS_FILENAME, delimiter='|')
    df = df[df.apply(axis=1, func=lambda x: x.zip_code in Zipcode.all_zipcodes_set)]
    #
    # create the locations for each zipcode then sort by increasing (cost, hrs, miles)
    # add the cost to the TransportationCosts dictionary
    #
    Zipcode.all_locations_set = set()
    for row in df.itertuples():
        Zipcode.zipcodes[row.zip_code].location_links.append( 
           LocationLink(row.nn_loc, row.link_cost, row.link_hour, row.link_miles)
        )
        Zipcode.all_locations_set.add(row.nn_loc)
        #TransportationCosts[ (row.zip_code, row.nn_loc) ] = row.link_cost
    #
    # for each zipcode sort the links
    # then change the locations list to an OrderedDict
    #
    for zipcode in Zipcode.zipcodes.values():
            zipcode.location_links.sort(key = lambda x: x[1:])   
            zipcode.location_links = OrderedDict([ (x[0], x[1:]) for x in zipcode.location_links])
        
            
            
#----------------------------------------------------------------------
def readLocationLinksFile():
    """
    read the locations_links.dat file 
    determine relevant neighborhood locations for each primary_location identified by the zipcodes
    add link information to locations
    """
    df = pd.read_csv(params.LOCATION_LINKS_FILENAME, delimiter='|')
    #
    # keep (eliminate others) locations that are locations for zipcodes
    #
    df = df[df.apply(axis=1, func=lambda x: x.primary_loc in Zipcode.all_locations_set)]
    #
    # create all locations
    #
    Location.all_locations_set = Zipcode.all_locations_set | set(df.nn_loc.unique())
    Location.locations = {}
    for location in Location.all_locations_set:
        Location.locations[location] = Location(location)
    #
    # determine all location->links
    #
    for row in df.itertuples():
        Location.locations[row.primary_loc].location_links.append( 
            LocationLink(row.nn_loc, row.link_cost, row.link_hour, row.link_miles)
            )
    #
    # for each location sort the links
    # then change the locations list to an OrderedDict
    #
    for location in Location.locations.values():
        location.location_links.sort(key = lambda x: x[1:])   
        location.location_links = OrderedDict([ (x[0], x[1:]) for x in location.location_links])    
        
        
#----------------------------------------------------------------------
def determinePrimaryZipcodes():
    """
    Determine the primary zipcodes for each location
    and calculate the location internal demands
    """
    for zipcode in Zipcode.zipcodes.values():
        primary_location = Location.locations[ next(iter(zipcode.location_links.keys())) ]  # works because zipcode.locations is OrderedDict
        primary_location.primary_zipcodes_demands[zipcode.zipcode] = zipcode.fct
        primary_location.demand_internal += zipcode.fct
        
        
def setup(part_number: str):
     #
    # get forecasts for part_number
    # add high/low priority customers to dataframe
    # create Zipcodes
    #
    df_forecast = readForecastFile(part_number)
    
    #
    # read the transportation_links.dat file
    # determine relevant locations for each zipcode
    # add link information to zipcodes
    #
    readTransportationLinksFile(df_forecast)
    
    #
    # read the locations_links.dat file 
    # determine relevant neighborhood locations for each location
    # add link information to locations
    #
    readLocationLinksFile()
    
    #
    # determine primary zipcodes for locations
    #
    determinePrimaryZipcodes()



    print('DONE')

    
    
if __name__ == '__main__':
    part_number = 'PN2'
    setup(part_number)
    
    


