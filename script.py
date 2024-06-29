# ANSI escape code for red
red = "\033[91m"
# ANSI escape code for green
green = "\033[92m"
# ANSI escape code for yellow
yellow = "\033[33m"
# Reset color to default
reset = "\033[0m"

# def group_passengers_by_two(passengers):
#     adults = [passenger for passenger in passengers if passenger["passengerType"] == "ADULT"]
#     children = [passenger for passenger in passengers if passenger["passengerType"] == "CHILD"]

#     grouped_passengers = []

#     while adults and children:
#         grouped_passengers.append([adults.pop(0), children.pop(0)])
    
#     if len(children) > 0:
#         for i in range(len(grouped_passengers)):
#             if children and len(grouped_passengers[i]) < 3:
#                 grouped_passengers[i].append(children.pop(0))
    
#     return grouped_passengers

def group_passengers_by_three(passengers):
    adults = [passenger for passenger in passengers if passenger["passengerType"] == "ADULT"]
    children = [passenger for passenger in passengers if passenger["passengerType"] == "CHILD"]
    
    grouped_passengers = []
    
    # Step 1: Try to form groups of (ADULT + CHILD + ADULT)
    while len(adults) >= 2 and children:
        grouped_passengers.append([adults.pop(0), children.pop(0), adults.pop(0)])

    # Step 2: Form groups of (ADULT + CHILD) with remaining passengers
    while adults and children:
        grouped_passengers.append([adults.pop(0), children.pop(0)])

    # Step 4: If there are children left, try to add into existing groups
    if len(adults) == 0 and len(children) > 0:
        for i in range(len(grouped_passengers)):
            if children and len(grouped_passengers[i]) < 3:
                grouped_passengers[i].append(children.pop(0))
    
    # Step 3: If there are adults left, keep them alone in their groups
    if len(adults) > 0 and len(children) == 0:
        while adults:
            grouped_passengers.append([adults.pop(0)])

    if len(children) > 0:
        print('Fails, childrens keeping left alone')
        # TODO: Improve this case, should to be reagrouped by two
        # return group_passengers_by_two(passengers)
    
    return grouped_passengers

success = 0
warning = 0
errors = 0

# Total 2 passengers -> (A=1, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]
print(f"{green}Test case 1: Total 2 passengers -> (A=1, C=1){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=2, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 2: Total 3 passengers -> (A=2, C=1){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=1, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 3: Total 3 passengers -> (A=1, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 4 passengers -> (A=3, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"}
]
print(f"{green}Test case 4: Total 4 passengers -> (A=3, C=1){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 4 passengers -> (A=2, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"},
    {"id": 4, "passengerType": "CHILD"}
]
print(f"{red}Test case 4: Total 4 passengers -> (A=2, C=2)")
print(f"Fail: Child ID 4 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 5 passengers -> (A=4, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "CHILD"}
]
print(f"{green}Test case 5: Total 5 passengers -> (A=4, C=1){reset}")
print(f"{yellow}Improve: Adult ID 4 and 5 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 5 passengers -> (A=3, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"}
]
print(f"{green}Test case 6: Total 5 passengers -> (A=3, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 5 passengers -> (A=2, C=3)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"}
]
print(f"{red}Test case 7: Total 5 passengers -> (A=2, C=3)")
print(f"Fail: Child ID 4 and 5 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 6 passengers -> (A=5, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "CHILD"}
]
print(f"{green}Test case 8: Total 6 passengers -> (A=5, C=1){reset}")
print(f"{yellow}Improve: Adult ID 4, 4 and 5 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 6 passengers -> (A=4, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"}
]
print(f"{green}Test case 9: Total 6 passengers -> (A=4, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 6 passengers -> (A=3, C=3)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"}
]
print(f"{green}Test case 10: Total 6 passengers -> (A=3, C=3){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 6 passengers -> (A=2, C=4)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"}
]
print(f"{red}Test case 11: Total 6 passengers -> (A=3, C=3)")
print(f"Fail: Child ID 4 and 5 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 7 passengers -> (A=6, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "CHILD"}
]
print(f"{green}Test case 12: Total 7 passengers -> (A=6, C=1){reset}")
print(f"{yellow}Improve: Adult ID 3, 4, 5 and 6 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 7 passengers -> (A=5, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"}
]
print(f"{green}Test case 13: Total 7 passengers -> (A=5, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 7 passengers -> (A=4, C=3)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"}
]
print(f"{red}Test case 14: Total 7 passengers -> (A=4, C=3)")
print(f"Fail: Child ID 7  left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 7 passengers -> (A=3, C=4)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"}
]
print(f"{red}Test case 15: Total 7 passengers -> (A=3, C=4)")
print(f"Fail: Child ID 6 and 7 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 8 passengers -> (A=7, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "ADULT"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 16: Total 8 passengers -> (A=7, C=1){reset}")
print(f"{yellow}Improve: Adult ID 3, 4, 5, 6 and 7 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 8 passengers -> (A=6, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 17: Total 8 passengers -> (A=6, C=2){reset}")
print(f"{yellow}Improve: Adult ID 5, 6 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 8 passengers -> (A=5, C=3)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 18: Total 8 passengers -> (A=5, C=3){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 8 passengers -> (A=4, C=4)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{red}Test case 19: Total 8 passengers -> (A=4, C=4)")
print(f"Fail: Child ID 7 and 8 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 9 passengers -> (A=8, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "ADULT"},
    {"id": 8, "passengerType": "ADULT"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 20: Total 9 passengers -> (A=8, C=1){reset}")
print(f"{yellow}Improve: Adult ID 3, 4, 5, 6 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 9 passengers -> (A=7, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "ADULT"},
    {"id": 8, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 20: Total 9 passengers -> (A=7, C=2){reset}")
print(f"{yellow}Improve: Adult ID 5, 6 left alone (could be joined){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
print("\n")

# Total 9 passengers -> (A=6, C=3)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "ADULT"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 21: Total 9 passengers -> (A=6, C=3){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 9 passengers -> (A=5, C=4)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "ADULT"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{green}Test case 22: Total 9 passengers -> (A=5, C=4){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

# Total 9 passengers -> (A=4, C=5)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "ADULT"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{red}Test case 23: Total 9 passengers -> (A=4, C=5)")
print(f"Fail: Child ID 7, 8 and 9 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

# Total 9 passengers -> (A=3 C=6)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"},
    {"id": 6, "passengerType": "CHILD"},
    {"id": 7, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"},
    {"id": 8, "passengerType": "CHILD"}
]
print(f"{red}Test case 22: Total 9 passengers -> (A=5, C=4)")
print(f"Fail: Child ID 7, 8 and 9 left alone{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

errors += 1
print("\n")

print(f"Result for success: {success}")
print(f"Result for warning: {warning}")
print(f"Result for errors: {errors}")
