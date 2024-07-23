from pymongo import MongoClient
from datetime import datetime
import cloudscraper
import pandas as pd
import os
import pendulum

green = "\033[92m"
reset = "\033[0m"
red = "\033[91m"

db_url = ''
db_name = ''
db_collection = ''

client = MongoClient(db_url)

scraper = cloudscraper.create_scraper()

def find_affected_flights():
    db = client[db_name]
    collection = db[db_collection]
    query = {"departureDate": {"$gte": "2024-07-22"}, "affectedPnrs": {"$ne": []}}
    # query = {"flightNumber": 285, "departureDate": "2025-01-01", "origin": "ANF"}
    # query = {"affectedPnrs": "YKWCDE"}
    documents = collection.find(query).sort("_id", 1).limit(1000)
    return list(documents)

def fetch_order(pnr):
    try:
        url = "https://reservation-order.skyairline.com/v1/order/find-by-pnr"
        payload = {"pnr": pnr }
        response = scraper.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        response.close()
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

def find_affected_flight(aux, flight, itinerary_parts):
    origin = flight['origin']
    departureDate = flight['departureDate']
    flightNumber = flight['flightNumber']
    if (aux):
        origin = aux['origin']
        departureDate = aux['departureDate']
        flightNumber = aux['flightNumber']
    hash_flight = f"{origin}-{flight['destination']}-{departureDate}-{flight['carrier']}-{str(flightNumber).zfill(4)}"
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            if (segment['hash'] == hash_flight):
                return segment
    return None

def host_is_unsync(affected_flight, itinerary_parts):
    origin = affected_flight['origin']
    departureDate = extract_date(affected_flight['departureDate'])
    flightNumber = affected_flight['flightNumber']['operating']
    hash_flight = f"{origin}-{affected_flight['destination']}-{departureDate}-{affected_flight['carrierCode']['operating']}-{str(flightNumber).zfill(4)}"
    for itinerary_part in itinerary_parts:
        for segment in itinerary_part['segments']:
            if (segment['hash'] == hash_flight):
                if (segment['departureDate'] != affected_flight['departureDate']):
                    return segment
    return None

def update_manual_notified(flight, pnr, syncStatus, mailStatus):
    db = client[db_name]
    affected_pnrs_collection = db['affected_pnrs']
    document = {
        "pnr": pnr,
        "affectationId": flight['_id'],
        "manualNotified": mailStatus,
        "sync": syncStatus,
    }
    affected_pnrs_collection.insert_one(document)

def send_notification(payload):
    try:
        url = "https://check-in-publisher.skyairline.com/v1/publish-message"
        response = scraper.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        response.close()
        return data
    except Exception as err:
        print(f'Error into send_notification for pnr: {pnr}')
        print(err)
        return None

def operational_window_interval():
    now = pendulum.now()
    later = now.add(hours=72)
    return now, later

def is_in_operational_window(departure_date):
    now, later = operational_window_interval()
    departure = pendulum.parse(departure_date)
    return now <= departure <= later

def extract_time(datetime_str):
    dt = datetime.fromisoformat(datetime_str)
    return dt.strftime("%H:%M")

def extract_date(datetime_str):
    dt = datetime.fromisoformat(datetime_str)
    return dt.strftime("%Y-%m-%d")

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

affected_flights = find_affected_flights()
data_for_excel = []

for i, flight in enumerate(affected_flights):
    print(f"{green}Current Flight {i + 1} of total {len(affected_flights)}:{reset}")
    for j, pnr in enumerate(flight['affectedPnrs']):
            temp_data = {
                "Pnr": pnr,
                "Affected Flight": "",
                "New Flight (Protector)": "",
            }
            reservation_order = fetch_order(pnr)
            if reservation_order:
                print(f"    - Pnr: {pnr} / Order: {reservation_order['orderId']} / total flights: {len(reservation_order.get('itineraryParts', []))}")
                itinerary_parts = reservation_order.get('itineraryParts', [])
                affected_flight = find_affected_flight(flight, flight['oldFlight'], itinerary_parts)
                if affected_flight:
                    temp_data['Affected Flight'] = affected_flight['hash']
                    reservation = fetch_reservation(pnr)
                    if reservation:
                        itinerary_parts = reservation.get('itineraryParts', [])
                        new_flight = host_is_unsync(affected_flight, itinerary_parts)
                        if new_flight:
                            print(f"{green}Pnr has affected flight in order and unsync schedule in host:{reset}")
                            temp_data['New Flight (Protector)'] = new_flight['hash']
                            data_for_excel.append(temp_data)
                            
                            in_operational_window = is_in_operational_window(new_flight['departureDate'])

                            is_before_operational_window = False

                            if in_operational_window == True:
                                is_before_operational_window = False

                            if in_operational_window == False:
                                is_before_operational_window = True                         

                            data = {
                                "routingKey": "communication.intinerary.changed",
                                "channel": "itinerary-history-request",
                                "message": {
                                    "homemarket": "CL",
                                    "language": "es",
                                    "pnr": pnr,
                                    "origin": new_flight['origin'],
                                    "destination": new_flight['destination'],
                                    "departureDate": new_flight['departureDate'],
                                    "passengers": reservation_order["passengers"],
                                    "orderContact": reservation_order['orderDetails']['orderContact'],
                                    "details": {
                                        "pnr": pnr,
                                        "agency": False,
                                        "retail": True,
                                        "groups": False,
                                        "before72": is_before_operational_window,
                                        "in72": in_operational_window,
                                        "mmbLink": "https://mmb.skyairline.com/es/chile",
                                        "wciLink": "https://check-in.skyairline.com/es/chile",
                                        "yellowAlertLink": "https://www.skyairline.com/chile/formularios/contactanos",
                                        "oldFlight": {
                                            "departureCity": affected_flight['origin'],
                                            "arrivalCity": affected_flight['destination'],
                                            "arrivalTime": extract_time(affected_flight['arrivalDate']),
                                            "departureDate": extract_date(affected_flight['departureDate']),
                                            "flightNumber": affected_flight['flightNumber']['operating'],
                                            "departureTime": extract_time(affected_flight['departureDate']),
                                            "duration": 0
                                        },
                                        "newFlight": {
                                            "departureCity": new_flight['origin'],
                                            "arrivalCity": new_flight['destination'],
                                            "arrivalTime": extract_time(new_flight['arrivalDate']),
                                            "departureDate": extract_date(new_flight['departureDate']),
                                            "flightNumber": new_flight['flightNumber']['operating'],
                                            "departureTime": extract_time(new_flight['departureDate']),
                                            "duration": 0
                                        }
                                    }
                                }
                            }

                            response = fetch_common_order(pnr)
                            if response:
                                print(f"{green}Pnr successfully sync{reset}")
                                temp_data['Order Sync'] = "Success"
                                print(f"    - Sending notification for pnr: {pnr}")
                                send_notification_response = send_notification(data)
                                print(f"    - Succesfully notification for pnr: {pnr}")
                                update_manual_notified(flight, pnr, True, True)
                            else:
                                print(f"{red}Could not sync pnr{reset}")
                                temp_data['Order Sync'] = "Failed"
                                update_manual_notified(flight, pnr, False, False)



output_directory = '/home/daniel/dev/py-helpers'
output_file = os.path.join(output_directory, "unsync-schedule.xlsx")

try:
    df = pd.DataFrame(data_for_excel)
    df.to_excel(output_file, index=False, sheet_name="Unsync schedule")
    print(f"Excel file saved successfully at {output_file}")
except Exception as e:
    print(f"Failed to save Excel file: {e}")
