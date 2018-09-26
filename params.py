LOCATION_LINKS_FILENAME = 'C:/IBM/Data/location_links.dat'
TRANSPORTATION_LINKS_FILENAME = 'C:/IBM/Data/transportation_links.dat'
FORECAST_FILENAME = 'C:/IBM/Data/forecast.dat'

PDTUSA_HIGH = 0.99
PDTUSA_LOW = 0.95

high_customer_pct = 0.25

decisions = [
    'Z',   # no decision taken
    'Q',   # regular replenishment initiated for delivery to location j of size Qj
    'R',   # reserve part restoration from the location j neighborhood of locations
    'N',   # part demand from zip code z, with a primary inventory location j, is satisfied from a neighborhood of locations associated with zip code j
    'NQ',  # decisions Q and N are both taken
    'NR',  # decisions Q and R are both taken
    'NQR', # decisions Q, N, and R are all taken
    'QR',  # decisions Q and R are both taken
]