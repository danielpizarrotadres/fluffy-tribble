cabin_seats = [
    {"seat": "1A", "row": 1, "column": "A", "status": "AVAILABLE"},
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

def get_available_seats(seats):
    rows = {}
    # Group seats by row
    for seat in seats:
        row = seat["row"]
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)
    
    result = []
    # For each row, group by availability status, but only include AVAILABLE seats
    for row, seats in rows.items():
        current_group = []
        last_status = seats[0]["status"]
        for seat in seats:
            if seat["status"] == "AVAILABLE":
                if seat["status"] == last_status:
                    current_group.append(seat)
                else:
                    if current_group:  # Ensure we don't add empty groups
                        result.append(current_group)
                    current_group = [seat]
                last_status = seat["status"]
            else:
                # If the current seat is not available, reset the current group
                if current_group:  # Ensure we don't add empty groups
                    result.append(current_group)
                current_group = []
                last_status = "NOT_AVAILABLE"  # Reset last_status to avoid adding NOT_AVAILABLE seats
        # Add the last group if it's not empty and contains AVAILABLE seats
        if current_group and last_status == "AVAILABLE":
            result.append(current_group)
    
    return result
