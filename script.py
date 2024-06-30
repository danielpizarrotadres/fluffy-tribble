# ANSI escape code for red
red = "\033[91m"
# ANSI escape code for green
green = "\033[92m"
# ANSI escape code for yellow
yellow = "\033[33m"
# Reset color to default
reset = "\033[0m"

def group_passengers_by_one(passengers):
    grouped_passengers = []
    while passengers:
        grouped_passengers.append([passengers.pop(0)])
    return group_passengers_by_one

# This function prioritizes the join of two passengers: one adult and one child
# Si no alcanza a agruparse por 2, se dejan sueltos
def group_passengers_by_two_for_two(passengers):
    grouped_passengers = []

    aux = group_passengers_by_two(passengers)
    need_to_be_grouped_for_two_by_to_two = False

    for i in range(len(aux)):
        if len(aux[i]) == 3:
            need_to_be_grouped_for_two_by_to_two = True
            break

    if need_to_be_grouped_for_two_by_to_two == False:
        return aux

    adults = [passenger for passenger in passengers if passenger["passengerType"] == "ADULT"]
    children = [passenger for passenger in passengers if passenger["passengerType"] == "CHILD"]
    
    while adults and children:
        grouped_passengers.append([adults.pop(0), children.pop(0)])

    if len(children) > 0:
        ## Here the idea is priortize the order of ADULT + CHILD
        ## But exists 1 scenario (A=2, C=3) in which the child left alone
        ## Ask what should be the BUSINESS rules for that, i suppose try to find another adult alone
        ## But if there are no spaces for ADULT ALONE ??
        while children:
            grouped_passengers.append([children.pop(0)])

    if len(adults) > 0:
        while adults:
            grouped_passengers.append([adults.pop(0)])

    return grouped_passengers

def group_passengers_by_two(passengers):
    adults = [passenger for passenger in passengers if passenger["passengerType"] == "ADULT"]
    children = [passenger for passenger in passengers if passenger["passengerType"] == "CHILD"]

    grouped_passengers = []

    while adults and children:
        grouped_passengers.append([adults.pop(0), children.pop(0)])
    
    if len(children) > 0:
        for i in range(len(grouped_passengers)):
            if children and len(grouped_passengers[i]) < 3:
                grouped_passengers[i].append(children.pop(0))

    if len(adults) > 0:
        while adults:
            # This could be improved, by joining all adults in a single group
            grouped_passengers.append([adults.pop(0)])
    
    return grouped_passengers

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
        # TODO: Improve this case, should to be reagrouped by two
        return group_passengers_by_two(passengers)
    
    return grouped_passengers

success = 0
warning = 0
errors = 0

print("\n")
print("- Test cases for group_passengers_by_three function:")
print("\n")

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
print(f"{yellow}Reminder: This case prioritizes the formation of groups of 3 passengers. Explanation for the output of (1 ADT + CHD + 1ADT) and + (1 ADT) this last alone{reset}")
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
print(f"{green}Test case 4: Total 4 passengers -> (A=2, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 7: Total 5 passengers -> (A=2, C=3){reset}")
print(f"{warning}Reminder: En este caso no se cumple lo esperado de que esta funcionalidad tenga la prioridad de formacion de grupo de 3 passengers 1ADT + 1CHD + 1ADT{reset}")
for p in group_passengers_by_three(passengers):
    print(p)

warning += 1
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
print(f"{green}Test case 11: Total 6 passengers -> (A=2, C=4){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 14: Total 7 passengers -> (A=4, C=3){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 15: Total 7 passengers -> (A=3, C=4){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 19: Total 8 passengers -> (A=4, C=4) {reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 23: Total 9 passengers -> (A=4, C=5){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 22: Total 9 passengers -> (A=3, C=6){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
print("\n")

print(f"Result for success: {success}")
print(f"Result for warning: {warning}")
print(f"Result for errors: {errors}")

################################################################################

print("\n")
print("- Test cases for group_passengers_by_two_for_two function:")
print("\n")

success = 0
warning = 0
errors = 0

# Total 2 passengers -> (A=1, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]
print(f"{green}Test case 1: Total 2 passengers -> (A=1, C=1){reset}")
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{yellow}Improve: Adult ID 2 and 3 could be grouped {reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
print("\n")

# Total 4 passengers -> (A=2, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"},
    {"id": 4, "passengerType": "CHILD"}
]
print(f"{green}Test case 4: Total 4 passengers -> (A=2, C=2){reset}")
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
print(f"{green}Test case 4: Total 4 passengers -> (A=2, C=2){reset}")
for p in group_passengers_by_three(passengers):
    print(p)

success += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{green}Test case 7: Total 5 passengers -> (A=2, C=3){reset}")
print(f"{yellow}Reminder: En este caso no se cumple lo esperado de que esta funcionalidad tenga la prioridad de formacion de grupo de 2 passengers 1ADT + 1CHD{reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{yellow}Improve: Adult ID 3 and 4 left alone (could be joined){reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{green}Test case 11: Total 6 passengers -> (A=2, C=4){reset}")
print(f"{yellow} En este escenario, deberiamos buscar si los 2 niños restantes pueden ser agrupados con adultos{reset}")
print(f"{yellow} Si no se puede, pregunrar a negocio{reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{yellow}Improve: Adult ID 3, 4, and 5 left alone (could be joined){reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
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
print(f"{green}Test case 15: Total 7 passengers -> (A=3, C=4){reset}")
print(f"{yellow} En este escenario, deberiamos buscar si los 2 niños restantes pueden ser agrupados con adultos{reset}")
print(f"{yellow} Si no se puede, pregunrar a negocio{reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
print("\n")

sengers = [
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{green}Test case 19: Total 8 passengers -> (A=4, C=4) {reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

success += 1
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
for p in group_passengers_by_two_for_two(passengers):
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
print(f"{green}Test case 23: Total 9 passengers -> (A=4, C=5){reset}")
print(f"{yellow} En este escenario, deberiamos buscar si los 2 niños restantes pueden ser agrupados con adultos{reset}")
print(f"{yellow} Si no se puede, pregunrar a negocio{reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 22: Total 9 passengers -> (A=3, C=6){reset}")
print(f"{yellow} En este escenario, deberiamos buscar si los 2 niños restantes pueden ser agrupados con adultos{reset}")
print(f"{yellow} Si no se puede, pregunrar a negocio{reset}")
for p in group_passengers_by_two_for_two(passengers):
    print(p)

warning += 1
print("\n")

print(f"Result for success: {success}")
print(f"Result for warning: {warning}")
print(f"Result for errors: {errors}")
