from pymongo import MongoClient
from datetime import datetime
import cloudscraper
import pandas as pd

db_url = 'mongodb+srv://affected_notification_request_prd_user:UXHwBpyoIGWVNr1P@itinerarios.yiqqc.mongodb.net/affected_notification_request_prd_db?retryWrites=true&w=majority&appName=ITINERARIOS'
db_name = 'affected_flights_request_prd_db'
db_collection = 'affectations'

client = MongoClient(db_url)

data_for_excel = []

def find_affected_flights():
    db = client[db_name]
    collection = db[db_collection]
    # query = {"departureDate": {"$gte": "2024-07-17"}, "affectedPnrs": {"$ne": []}}
    query = {"flightNumber": 285, "departureDate": "2025-01-01", "origin": "ANF"}
    documents = collection.find(query)
    return list(documents)

def fetch_data_from_reservation_order(pnr):
    try:
        scraper = cloudscraper.create_scraper()
        url = "https://reservation-order.skyairline.com/v1/order/find-by-pnr"
        payload = {"pnr": pnr }
        print(payload)
        response = scraper.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        # TODO: Make something
        return None

def find_flight(itinerary_parts, flight_number, origin, departure_date):
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            departure_year, departure_month, departure_day = segment['departureDate'].split('T')[0].split('-')
            formatted_departure_date = f"{departure_year}-{departure_month}-{departure_day}"
        
            if (segment['flightNumber']['marketing'] == flight_number and
                segment['origin'] == origin and
                formatted_departure_date == departure_date):
                return segment

affected_flights = find_affected_flights()

for index, flight in enumerate(affected_flights):
    print(f"Current {index + 1}: {flight['origin']} {flight['flightNumber']} {flight['departureDate']} / Total pnrs: {len(flight['affectedPnrs'])}")

    for pnr in flight['affectedPnrs']:
        data_from_reservation_order = fetch_data_from_reservation_order(pnr)

        if data_from_reservation_order:
            itinerary_parts = data_from_reservation_order.get('itineraryParts', [])

            matching_segment = find_flight(itinerary_parts, flight['flightNumber'], flight['origin'], flight['departureDate'])

            if matching_segment:
                print(f"Matching segment for PNR {pnr}: {matching_segment}")

                data_for_excel.append({"PNR": pnr, "Flight": f"{flight['origin']} {flight['flightNumber']} {flight['departureDate']}"})


df = pd.DataFrame(data_for_excel)
df.to_excel("affected_flights.xlsx", index=False, sheet_name="Affected Flights")

