from pymongo import MongoClient
from datetime import datetime
import cloudscraper
import pandas as pd
import os

db_url = 'mongodb+srv://affected_notification_request_prd_user:UXHwBpyoIGWVNr1P@itinerarios.yiqqc.mongodb.net/affected_notification_request_prd_db?retryWrites=true&w=majority&appName=ITINERARIOS'
db_name = 'affected_flights_request_prd_db'
db_collection = 'affectations'

client = MongoClient(db_url)

scraper = cloudscraper.create_scraper()

def find_affected_flights():
    db = client[db_name]
    collection = db[db_collection]
    # query = {"departureDate": {"$gte": "2024-07-17"}, "affectedPnrs": {"$ne": []}}
    query = {"flightNumber": 285, "departureDate": "2025-01-01", "origin": "ANF"}
    documents = collection.find(query)
    return list(documents)

def fetch_data_from_reservation_order(pnr):
    try:
        url = "https://reservation-order.skyairline.com/v1/order/find-by-pnr"
        payload = {"pnr": pnr }
        response = scraper.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        response.close()  # Explicitly close the response
        return data
    except Exception as err:
        print(f'Error into fetch_data_from_reservation_order for pnr: {pnr}')
        print(err)
        return None

def find_affected_flight_in_order(old_flight, itinerary_parts):
    hash_old_flight = f"{old_flight['origin']}-{old_flight['destination']}-{old_flight['departureDate']}-{old_flight['carrier']}-{str(old_flight['flightNumber']).zfill(4)}"
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            if (segment['hash'] == hash_old_flight):
                return segment
    return None

affected_flights = find_affected_flights()

for i, flight in enumerate(affected_flights):
    print(f"Current Flight {i + 1} of total {len(affected_flights)}:")

    for j, pnr in enumerate(flight['affectedPnrs']):

        data_from_reservation_order = fetch_data_from_reservation_order(pnr)

        if data_from_reservation_order:
            print(f"- Order: {data_from_reservation_order['orderId']} / total segments: {len(data_from_reservation_order.get('itineraryParts', []))}")

            itinerary_parts = data_from_reservation_order.get('itineraryParts', [])

            affected_flight_in_order = find_affected_flight_in_order(flight['oldFlight'], itinerary_parts)

            if affected_flight_in_order:
                print(affected_flight_in_order)
