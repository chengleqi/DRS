def normalize_state(state):
    # CPU usage normalization
    state[0] = min(state[0], 100)

    # Network receive and transmit normalization
    state[2] = min(state[2] / 40 * 10, 100)
    state[3] = min(state[3] / 40 * 10, 100)

    # IO read and write normalization
    state[4] = min(state[4] / 10240 * 100, 100)
    state[5] = min(state[5] / 10240 * 100, 100)

    state[6] = min(state[6], 100)

    return [round(item, 1) for item in state]

def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            state = [float(value) for value in line.strip().split()]
            data.append(state)
    return data

def calculate_averages(data):
    # Normalize the data
    normalized_data = [normalize_state(state) for state in data]

    # Calculate average values for each column
    averages = [sum(col) / len(normalized_data) for col in zip(*normalized_data)]
    return [round(avg, 1) for avg in averages]

# Path to the usage.txt file
file_path = 'usage.txt'

# Read, normalize, and calculate averages
usage_data = read_data(file_path)
averages = calculate_averages(usage_data)

# Print the average values with one decimal place
print("Average values after normalization:", averages)