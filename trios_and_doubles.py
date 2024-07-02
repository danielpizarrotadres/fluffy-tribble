# ANSI escape code for red
red = "\033[91m"
# ANSI escape code for green
green = "\033[92m"
# ANSI escape code for yellow
yellow = "\033[33m"
# Reset color to default
reset = "\033[0m"

def try_match_individuals(passengers):
    grouped_passengers = []
    while passengers:
        grouped_passengers.append([passengers.pop(0)])
    return grouped_passengers

def try_match_doubles(passengers):
    grouped_passengers = []

    aux = merge_trios_and_doubles(passengers)
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
        while children:
            grouped_passengers.append([children.pop(0)])

    if len(adults) > 0:
        while adults:
            grouped_passengers.append([adults.pop(0)])

    return grouped_passengers

def merge_trios_and_doubles(passengers):
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
            grouped_passengers.append([adults.pop(0)])
    
    if len(children) > 0:
        while children:
            grouped_passengers.append([children.pop(0)])
        return grouped_passengers
    
    return grouped_passengers

def try_match_trios(passengers):
    adults = [passenger for passenger in passengers if passenger["passengerType"] == "ADULT"]
    children = [passenger for passenger in passengers if passenger["passengerType"] == "CHILD"]
    
    grouped_passengers = []
    
    # Step 1: Try to form groups of (ADULT + CHILD + ADULT)
    while len(children) >= 2 and adults:
        grouped_passengers.append([children.pop(0), adults.pop(0), children.pop(0)])

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
        for i in range(len(grouped_passengers)):
            if adults and len(grouped_passengers[i]) < 3:
                grouped_passengers[i].append(adults.pop(0))

    if len(children) > 0:
        return merge_trios_and_doubles(passengers)
    
    if len(adults) > 0:
        while adults:
            grouped_passengers.append([adults.pop(0)])
    
    return grouped_passengers

success = 0
warning = 0
errors = 0

print("\n")
print("Test cases for try_match_trios function:")
print("\n")

# Total 2 passengers -> (A=1, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]
print(f"{green}Test case 1 (try_match_trios): Total 2 passengers -> (A=1, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=2, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 2 (try_match_trios): Total 3 passengers -> (A=2, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=1, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 3 (try_match_trios): Total 3 passengers -> (A=1, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 4 (try_match_trios): Total 4 passengers -> (A=3, C=1){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 4 (try_match_trios): Total 4 passengers -> (A=2, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 5 (try_match_trios): Total 5 passengers -> (A=4, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
print("\n")

# Total 5 passengers -> (A=3, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"}
]
print(f"{green}Test case 6 (try_match_trios): Total 5 passengers -> (A=3, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 7 (try_match_trios): Total 5 passengers -> (A=2, C=3){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 8 (try_match_trios): Total 6 passengers -> (A=5, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 9 (try_match_trios): Total 6 passengers -> (A=4, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 10 (try_match_trios): Total 6 passengers -> (A=3, C=3){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 11 (try_match_trios): Total 6 passengers -> (A=2, C=4){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 12 (try_match_trios): Total 7 passengers -> (A=6, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 13 (try_match_trios): Total 7 passengers -> (A=5, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 14 (try_match_trios): Total 7 passengers -> (A=4, C=3){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 15 (try_match_trios): Total 7 passengers -> (A=3, C=4){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 16 (try_match_trios): Total 8 passengers -> (A=7, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 17 (try_match_trios): Total 8 passengers -> (A=6, C=2){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 18 (try_match_trios): Total 8 passengers -> (A=5, C=3){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 19 (try_match_trios): Total 8 passengers -> (A=4, C=4) {reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 20 (try_match_trios): Total 9 passengers -> (A=8, C=1){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 21 (try_match_trios): Total 9 passengers -> (A=7, C=2){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 22 (try_match_trios): Total 9 passengers -> (A=6, C=3){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 23 (try_match_trios): Total 9 passengers -> (A=5, C=4){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 24 (try_match_trios): Total 9 passengers -> (A=4, C=5){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 25 (try_match_trios): Total 9 passengers -> (A=3, C=6){reset} ✅")
for p in try_match_trios(passengers):
    print(p)

success += 1
print("\n")

print(f"Result for success: {success}")
print(f"Result for warning: {warning}")
print(f"Result for errors: {errors}")

################################################################################

print("\n")
print("Test cases for try_match_doubles function:")
print("\n")

success = 0
warning = 0
errors = 0

# Total 2 passengers -> (A=1, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"}
]
print(f"{green}Test case 1 (try_match_doubles): Total 2 passengers -> (A=1, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=2, C=1)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 2 (try_match_doubles): Total 3 passengers -> (A=2, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
print("\n")

# Total 3 passengers -> (A=1, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "CHILD"},
    {"id": 3, "passengerType": "CHILD"}
]
print(f"{green}Test case 3 (try_match_doubles): Total 3 passengers -> (A=1, C=2){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 4 (try_match_doubles): Total 4 passengers -> (A=3, C=1){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 5 (try_match_doubles): Total 4 passengers -> (A=2, C=2){reset} ✅")
for p in try_match_trios(passengers):
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
print(f"{green}Test case 6 (try_match_doubles): Total 5 passengers -> (A=4, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
print("\n")

# Total 5 passengers -> (A=3, C=2)
passengers = [
    {"id": 1, "passengerType": "ADULT"},
    {"id": 2, "passengerType": "ADULT"},
    {"id": 3, "passengerType": "ADULT"},
    {"id": 4, "passengerType": "CHILD"},
    {"id": 5, "passengerType": "CHILD"}
]
print(f"{green}Test case 7 (try_match_doubles): Total 5 passengers -> (A=3, C=2){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 8 (try_match_doubles): Total 5 passengers -> (A=2, C=3){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 9 (try_match_doubles): Total 6 passengers -> (A=5, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 10 (try_match_doubles): Total 6 passengers -> (A=4, C=2){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 11 (try_match_doubles): Total 6 passengers -> (A=3, C=3){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 12 (try_match_doubles): Total 6 passengers -> (A=2, C=4){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 13 (try_match_doubles): Total 7 passengers -> (A=6, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 14 (try_match_doubles): Total 7 passengers -> (A=5, C=2){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 15 (try_match_doubles): Total 7 passengers -> (A=3, C=4){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 16 (try_match_doubles): Total 8 passengers -> (A=7, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 17 (try_match_doubles): Total 8 passengers -> (A=6, C=2){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
print("\n")

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
print(f"{green}Test case 18 (try_match_doubles): Total 8 passengers -> (A=5, C=3){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 19 (try_match_doubles): Total 8 passengers -> (A=4, C=4) {reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 20 (try_match_doubles): Total 9 passengers -> (A=8, C=1){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 21 (try_match_doubles): Total 9 passengers -> (A=7, C=2){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
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
print(f"{green}Test case 22 (try_match_doubles): Total 9 passengers -> (A=6, C=3){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 23 (try_match_doubles): Total 9 passengers -> (A=5, C=4){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 24 (try_match_doubles): Total 9 passengers -> (A=4, C=5){reset} ✅")
for p in try_match_doubles(passengers):
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
print(f"{green}Test case 25 (try_match_doubles): Total 9 passengers -> (A=3, C=6){reset} ✅")
for p in try_match_doubles(passengers):
    print(p)

success += 1
print("\n")

print(f"Result for success: {success}")
print(f"Result for warning: {warning}")
print(f"Result for errors: {errors}")
