import os


def parse_file(path):
    """
    Parses a file from the given path and extracts the vertex data.
    It returns the vertices as a list of lists, where each inner list represents a vertex and contains its coordinates.

    If the path does not point to a file, it returns None.
    """

    # Check if the given path points to a file
    vertices = []
    if (os.path.isfile(path) == False):
        return None

    # Open the file and iterate over its lines
    with open(path, 'r') as f:
        for line in f:
            # Split the line into tokens
            tokens = line.split()

            # If tokens were found and the first one is 'v',
            # this line contains vertex data, so we parse the coordinates
            if tokens and tokens[0] == 'v':
                # Append the coordinates of the vertex to the vertices list
                vertices.append([float(x) for x in tokens[1:]])
    return vertices


def averages(vertices, dimension, frequency=1):
    """
    Groups the vertices into sublists of size 10 and calculates the average coordinates for each group.
    Returns a list of the averages.
    """

    group_size = 10

    # Split the vertices into groups of 10
    groups = [vertices[i: i + group_size]
              for i in range(0, len(vertices), group_size)]
    group_avgs = []

    # Iterate over each group
    for group in groups:
        avg = [0] * dimension
        for vertex in group:
            for i in range(dimension):
                avg[i] += vertex[i]
        avg = [a / len(group) * frequency for a in avg]
        group_avgs.append(avg)
    return group_avgs


def write_to_file(filename, data, headers):
    """
    Writes the given data to a file with the given filename.
    The data is written as CSV, with the given headers at the top.
    """

    with open(filename, 'w') as f:
        f.write(headers + '\n')
        for row in data:
            f.write(','.join(str(x) for x in row) + '\n')


def run_simulation(dimension, context, path, save_path):
    """
    Runs a simulation that parses vertex data from a file, calculates averages and writes them to a CSV file.
    """

    if dimension == 1:
        header = 'x'
    elif dimension == 2:
        header = 'x,y'
    elif dimension == 3:
        header = 'x,y,z'

    filename = os.path.basename(path)
    vertices = parse_file(path)
    if (vertices is not None):
        freq = context.scene.settings.frequency
        if freq is None:
            freq = 1
        avgs = averages(vertices, dimension, freq)
        file_path = f'{save_path}/{filename}{dimension}-dimension.csv'
        write_to_file(file_path, avgs, header)
