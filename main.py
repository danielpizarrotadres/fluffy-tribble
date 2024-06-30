from tests import get_available_seats
from script import try_match_trios, try_match_doubles
from seat_search_engine import seat_search_engine

cabin_seats = [
    {"seat": "1A", "row": 1, "column": "A", "status": "AVAILABLE"},
    {"seat": "1B", "row": 1, "column": "B", "status": "AVAILABLE"},
    {"seat": "1C", "row": 1, "column": "C", "status": "NOT_AVAILABLE"},
    {"seat": "1D", "row": 1, "column": "D", "status": "NOT_AVAILABLE"},
    {"seat": "1E", "row": 1, "column": "E", "status": "NOT_AVAILABLE"},
    {"seat": "1F", "row": 1, "column": "F", "status": "NOT_AVAILABLE"},
    {"seat": "2A", "row": 2, "column": "A", "status": "NOT_AVAILABLE"},
    {"seat": "2B", "row": 2, "column": "B", "status": "NOT_AVAILABLE"},
    {"seat": "2C", "row": 2, "column": "C", "status": "NOT_AVAILABLE"},
    {"seat": "2D", "row": 2, "column": "D", "status": "NOT_AVAILABLE"},
    {"seat": "2E", "row": 2, "column": "E", "status": "NOT_AVAILABLE"},
    {"seat": "2F", "row": 2, "column": "F", "status": "NOT_AVAILABLE"}
]

passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"},
    {"id": 3, "passengerType": "CHILD"}
]


available_seats = get_available_seats(cabin_seats)

trios = try_match_trios(passengers)

doubles = try_match_doubles(passengers)

def assign_seats(groups, available_seats):
    availability = True
    seats_results = []
    all_available_seats = [group.copy() for group in available_seats]
    for passengers in groups:
        total_passengers = len(passengers)
        candidate_seats = []
        for seats in all_available_seats:
            if len(seats) >= total_passengers:
                candidate_seats.append(seats)
        total_candidates = len(candidate_seats)
        if total_candidates == 0:
            availability = False
            break
        matched_seats = seat_search_engine(candidate_seats, total_passengers)
        seats_results.append(matched_seats)
        for matched_seat in matched_seats:
            for seats_group in all_available_seats:
                if matched_seat in seats_group:
                    seats_group.remove(matched_seat)
                    break
    if availability:
        return seats_results
    else:
        return []

result = assign_seats(doubles, available_seats)
print(result)
