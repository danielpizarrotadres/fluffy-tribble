config = {
    3: ['A-B-C', 'D-E-F', 'B-C-D', 'C-D-E'],
    2: ['A-B', 'B-C', 'D-E', 'E-F', 'C-D'],
    1: ['A', 'B', 'C', 'D', 'E', 'F']
}

def seat_search_engine(seat_rows, key):
    combination = config[key]
    # Step 1: Create a list of tuples containing both the row and the column of each available seat
    available_seats = [seat for row in seat_rows for seat in row if seat['status'] == 'AVAILABLE']
    available_positions = [(seat['row'], seat['column']) for seat in available_seats]
    
    for pattern in combination:
        required_columns = pattern.split('-')
        # Step 2: Check if all required columns are available in at least one row
        for row_number in set(pos[0] for pos in available_positions):  # Unique rows with available seats
            if all((row_number, column) in available_positions for column in required_columns):
                # Step 3: Filter the matching seats based on both the row and the column
                matching_seats = [seat for seat in available_seats if (seat['row'], seat['column']) in [(row_number, col) for col in required_columns]]
                return matching_seats
    return []
