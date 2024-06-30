from script import group_passengers_by_one

# Total 2 passengers -> (A=1, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]

result = group_passengers_by_one(passengers)

print(result)
