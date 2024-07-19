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

def find_flight(itinerary_parts, flight_number, origin, destination, departure_date):
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            departure_year, departure_month, departure_day = segment['departureDate'].split('T')[0].split('-')
            formatted_departure_date = f"{departure_year}-{departure_month}-{departure_day}"
            if (segment['flightNumber']['marketing'] == flight_number and
                segment['origin'] == origin and
                segment['destination'] == destination
                and formatted_departure_date == departure_date):
                return segment

def logger_flight(index, flight, affected_flights):
    print(f"Current Flight {index + 1} of total {len(affected_flights)}:")
    # print(f"ID: {flight['_id']}")
    # print(f"Origin {flight['origin']} / {flight['flightNumber']} / {flight['departureDate']}")
    # print(f"Old Flight: {flight['oldFlight']['origin']} / {flight['oldFlight']['destination']} / {flight['oldFlight']['scheduledDepartureTime']}  / {flight['oldFlight']['flightNumber']}")
    # print(f"New Flight: {flight['newFlight']['origin']} / {flight['newFlight']['destination']} / {flight['newFlight']['scheduledDepartureTime']}  / {flight['newFlight']['flightNumber']}")

# def logger_pnr(index, pnrs):
#     print(f"Current Pnr {index + 1} of total {len(pnrs)}:")

affected_flights = find_affected_flights()

for i, flight in enumerate(affected_flights):
    logger_flight(i, flight, affected_flights)

    for j, pnr in enumerate(flight['affectedPnrs']):
        # logger_pnr(j, flight['affectedPnrs'])
        
        data_from_reservation_order = fetch_data_from_reservation_order(pnr)

        if data_from_reservation_order:
            print(f"    Order: {data_from_reservation_order['orderId']} / total segments: {len(data_from_reservation_order.get('itineraryParts', []))}")
            itinerary_parts = data_from_reservation_order.get('itineraryParts', [])
            order_segment = find_flight(
                itinerary_parts,
                flight['newFlight']['flightNumber'],
                flight['newFlight']['origin'],
                flight['newFlight']['destination'],
                flight['departureDate']
            )
