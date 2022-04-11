"""Constants for the Detailed Hello World Push integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "itsmarta"
DEFAULT_NAME = "MARTA"
PLATFORMS = [Platform.SENSOR]

CONFIG_BREEZE_CARD = "breeze_card"
CONF_NUMBER = "number"
CONF_ROUTES = "routes"
CONF_STATIONS = "stations"

DEVICE_TRAINS_ID = "4c1c578b_78e3_4b01_a79d_5a38a07337e1"
DEVICE_BUSES_ID = "5f6a85b8_91a1_4669_901e_b70a59110180"

ATTRIBUTION = "Powered by MARTA"
ATTR_BALLANCE_PROT = "Balance Prtotected"
ATTR_EXPIRES = "Expires"
ATTR_TRIPS = "Stored Trips"
ATTR_VALUE = "Stored Value"

TEST_API_KEY = "99999999-6299-41a9-b099-912345678904"
TEST_BREEZE_CARD = "01234567890123456789"

MARTA_API_TIMEOUT = 10
SCAN_INTERVAL = timedelta(minutes=2)
DIRECTIONS_SWITCH = {
    "n": "Northbound",
    "s": "Southbound",
    "e": "Eastbound",
    "w": "Westbound",
}
STATION_NAMES = {
    "Airport Station",
    "Arts center Station",
    "Ashby Station",
    "Avondale Station",
    "Bankhead Station",
    "Brookhaven Station",
    "Buckhead Station",
    "Chamblee Station",
    "Civic Center Station",
    "College Park Station",
    "Decatur Station",
    "Doraville Station",
    "Dunwoody Station",
    "East Lake Station",
    "East Point Station",
    "Edgewood Candler Park Station",
    "Five Points Station",
    "Garnett Station",
    "Georgia State Station",
    # "GWCC/Mercedes-Benz Stadium Station",
    "Hamilton E Holmes Station",
    "Indian Creek Station",
    "Inman Park Station",
    "Kensington Station",
    "King Memorial Station",
    "Lakewood Station",
    "Lenox Station",
    "Lindbergh Station",
    "Medical Center Station",
    "Midtown Station",
    "North Ave Station",
    "North Springs Station",
    "Oakland City Station",
    "Omni Dome Station",
    "Peachtree Center Station",
    "Sandy Springs Station",
    "Vine City Station",
    "West End Station",
    "West Lake Station",
}
ROUTE_NUMBERS = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "8",
    "9",
    "12",
    "14",
    "15",
    "19",
    "21",
    "24",
    "25",
    "26",
    "27",
    "30",
    "32",
    "34",
    "36",
    "37",
    "39",
    "40",
    "42",
    "47",
    "49",
    "50",
    "51",
    "55",
    "58",
    "60",
    "66",
    "68",
    "71",
    "73",
    "74",
    "75",
    "78",
    "79",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "89",
    "93",
    "94",
    "95",
    "102",
    "103",
    "104",
    "107",
    "110",
    "111",
    "114",
    "115",
    "116",
    "117",
    "119",
    "120",
    "121",
    "123",
    "124",
    "125",
    "126",
    "132",
    "133",
    "140",
    "141",
    "142",
    "143",
    "148",
    "150",
    "153",
    "155",
    "162",
    "165",
    "172",
    "178",
    "180",
    "181",
    "183",
    "185",
    "186",
    "189",
    "191",
    "192",
    "193",
    "194",
    "195",
    "196",
    "201",
    "221",
    "295",
    "800",
    "809",
    "813",
    "816",
    "823",
    "825",
    "832",
    "850",
    "853",
    "856",
    "865",
    "867",
    "899",
}
