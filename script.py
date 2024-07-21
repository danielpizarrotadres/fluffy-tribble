from pymongo import MongoClient
from datetime import datetime
import cloudscraper
import pandas as pd
import os

green = "\033[92m"
reset = "\033[0m"

db_url = 'mongodb+srv://affected_notification_request_prd_user:UXHwBpyoIGWVNr1P@itinerarios.yiqqc.mongodb.net/affected_notification_request_prd_db?retryWrites=true&w=majority&appName=ITINERARIOS'
db_name = 'affected_flights_request_prd_db'
db_collection = 'affectations'

client = MongoClient(db_url)

scraper = cloudscraper.create_scraper()

def find_affected_flights():
    db = client[db_name]
    collection = db[db_collection]
    query = {"departureDate": {"$gte": "2024-07-17"}, "affectedPnrs": {"$ne": []}}
    # query = {"flightNumber": 285, "departureDate": "2025-01-01", "origin": "ANF"}
    documents = collection.find(query).limit(1000)
    return list(documents)

def fetch_order(pnr):
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

def fetch_reservation(pnr):
    try:
        url = "https://sws-integration-retrieve-pnr.skyairline.com/v1/pnr"
        params = {"pnr": pnr}
        response = scraper.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        response.close()
        return data
    except Exception as err:
        print(f'Error into fetch_data_from_sws_retrieve_pnr for pnr: {pnr}')
        print(err)
        return None

def fetch_common_order(pnr):
    try:
        url = "https://reservation-order.skyairline.com/v1/order/common"
        headers = {
            'Content-Type': 'application/json',
            'authorization': '090C613FF55946E3B65506D4EC190364',
            'x-api-key': '8D194F87CCEF48B7AE58B3C0AD770C0D',
        }
        payload = {"pnr": pnr}
        response = scraper.put(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        response.close()
        return data
    except Exception as err:
        print(f'Error into fetch_common_order for pnr: {pnr}')
        print(err)
        return None

def find_flight(flight, itinerary_parts):
    hash_flight = f"{flight['origin']}-{flight['destination']}-{flight['departureDate']}-{flight['carrier']}-{str(flight['flightNumber']).zfill(4)}"
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            if (segment['hash'] == hash_flight) and segment['departureDate'] == flight['scheduledDepartureTime']:
                return segment
    return None

affected_flights = find_affected_flights()
data_for_excel = []

for i, flight in enumerate(affected_flights):
    print(f"{green}Current Flight {i + 1} of total {len(affected_flights)}:{reset}")
    for j, pnr in enumerate(flight['affectedPnrs']):
        temp_data = {
            "Pnr": pnr,
            "Affected Flight": "",
            "New Flight (Protector)": "",
            "Order Sync": "Success"
        }
        reservation_order = fetch_order(pnr)
        if reservation_order:
            print(f"    - Pnr: {pnr} / Order: {reservation_order['orderId']} / total flights: {len(reservation_order.get('itineraryParts', []))}")
            itinerary_parts = reservation_order.get('itineraryParts', [])
            affected_flight = find_flight(flight['oldFlight'], itinerary_parts)
            if affected_flight:
                temp_data['Affected Flight'] = affected_flight['hash']
                reservation = fetch_reservation(pnr)
                if reservation:
                    itinerary_parts = reservation.get('itineraryParts', [])
                    new_flight = find_flight(flight['newFlight'], itinerary_parts)
                    if new_flight:
                        print(f"{green}Pnr has affected flight in order and new flight in host:{reset}")
                        temp_data['New Flight (Protector)'] = new_flight['hash']
                        response = fetch_common_order(pnr)
                        if response:
                            temp_data['Order Sync'] = "Success"
                        else:
                            temp_data['Order Sync'] = "Failed"

                        data_for_excel.append(temp_data)

output_directory = '/home/daniel/dev/py-helpers'
output_file = os.path.join(output_directory, "affected_flights.xlsx")

try:
    df = pd.DataFrame(data_for_excel)
    df.to_excel(output_file, index=False, sheet_name="Affected Flights-Finished")
    print(f"Excel file saved successfully at {output_file}")
except Exception as e:
    print(f"Failed to save Excel file: {e}")
