config = {
    3: ['A-B-C', 'D-E-F', 'B-C-D', 'C-D-E'],
    2: ['A-B', 'B-C', 'D-E', 'E-F', 'C-D'],
    1: ['A', 'B', 'C', 'D', 'E', 'F']
}

def seat_search_engine(seat_rows, key):
    combination = config[key]
    available_seats = [seat for row in seat_rows for seat in row if seat['status'] == 'AVAILABLE']
    available_columns = [seat['column'] for seat in available_seats]
    for pattern in combination:
        required_columns = pattern.split('-')
        if all(column in available_columns for column in required_columns):
            matching_seats = [seat for seat in available_seats if seat['column'] in required_columns]
            return matching_seats
    return []
