from script import group_passengers_by_one

# Total 2 passengers -> (A=1, C=1)
# passengers = [
#     {"id": 1, "passengerType": "ADULT"},
#     {"id": 2, "passengerType": "CHILD"}
# ]
# result = group_passengers_by_one(passengers)
# print(result)

cabin_seats = [
    {"seat": "1A", "row": 1, "column": "A", "status": "NOT_AVAILABLE"},
    {"seat": "1B", "row": 1, "column": "B", "status": "AVAILABLE"},
    {"seat": "1C", "row": 1, "column": "C", "status": "AVAILABLE"},
    {"seat": "1D", "row": 1, "column": "D", "status": "AVAILABLE"},
    {"seat": "1E", "row": 1, "column": "E", "status": "AVAILABLE"},
    {"seat": "1F", "row": 1, "column": "F", "status": "AVAILABLE"},
    {"seat": "2A", "row": 2, "column": "A", "status": "AVAILABLE"},
    {"seat": "2B", "row": 2, "column": "B", "status": "NOT_AVAILABLE"},
    {"seat": "2C", "row": 2, "column": "C", "status": "AVAILABLE"},
    {"seat": "3D", "row": 2, "column": "D", "status": "AVAILABLE"},
    {"seat": "3E", "row": 2, "column": "E", "status": "AVAILABLE"},
    {"seat": "3F", "row": 2, "column": "F", "status": "NOT_AVAILABLE"}
]

def group_seats_by_row_and_status(seats):
    rows = {}
    # Group seats by row
    for seat in seats:
        row = seat["row"]
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)
    
    result = []
    # For each row, group by availability status
    for row, seats in rows.items():
        current_group = []
        last_status = seats[0]["status"]
        for seat in seats:
            if seat["status"] == last_status:
                current_group.append(seat)
            else:
                result.append(current_group)
                current_group = [seat]
                last_status = seat["status"]
        result.append(current_group)
    
    return result

grouped_cabin_seats_by_row_and_status = group_seats_by_row_and_status(cabin_seats)
for group in grouped_cabin_seats_by_row_and_status:
    print(group)
    print("\n")
