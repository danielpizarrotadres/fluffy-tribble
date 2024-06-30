from tests import group_available_seats_by_row
from script import group_passengers_by_three

cabin_seats = [
    {"seat": "1A", "row": 1, "column": "A", "status": "NOT_AVAILABLE"},
    {"seat": "1B", "row": 1, "column": "B", "status": "NOT_AVAILABLE"},
    {"seat": "1C", "row": 1, "column": "C", "status": "AVAILABLE"},
    {"seat": "1D", "row": 1, "column": "D", "status": "AVAILABLE"},
    {"seat": "1E", "row": 1, "column": "E", "status": "AVAILABLE"},
    {"seat": "1F", "row": 1, "column": "F", "status": "AVAILABLE"},
    {"seat": "2A", "row": 2, "column": "A", "status": "AVAILABLE"},
    {"seat": "2B", "row": 2, "column": "B", "status": "NOT_AVAILABLE"},
    {"seat": "2C", "row": 2, "column": "C", "status": "AVAILABLE"},
    {"seat": "3D", "row": 2, "column": "D", "status": "NOT_AVAILABLE"},
    {"seat": "3E", "row": 2, "column": "E", "status": "NOT_AVAILABLE"},
    {"seat": "3F", "row": 2, "column": "F", "status": "NOT_AVAILABLE"}
]

passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]

available_seats = group_available_seats_by_row(cabin_seats)

group_passengers = group_passengers_by_three(passengers)

print('----------------------')
print("\n")

for i in available_seats:
    print(i)
    print("\n")

print('----------------------')
print("\n")

for i in group_passengers:
    print(i)
    print("\n")
    for j in available_seats:
        print(j)
        print("\n")
        if len(j) >= len(i):
            print("Yes")
        else:
            print("No")
        print("\n")
