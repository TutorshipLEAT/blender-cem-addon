import os


def parse_file(path):
    vertices = []
    if (os.path.isfile(path) == False):
        return None
    with open(path, 'r') as f:
        for line in f:
            tokens = line.split()
            if tokens:
                if tokens[0] == 'v':
                    vertices.append([float(x) for x in tokens[1:]])
    return vertices


def averages(vertices, dimension, frequency=1):
    group_size = 10
    groups = [vertices[i: i + group_size]
              for i in range(0, len(vertices), group_size)]
    group_avgs = []
    for group in groups:
        avg = [0] * dimension
        for vertex in group:
            for i in range(dimension):
                avg[i] += vertex[i]
        avg = [a / len(group) * frequency for a in avg]
        group_avgs.append(avg)
    return group_avgs


def write_to_file(filename, data, headers):
    with open(filename, 'w') as f:
        f.write(headers+'\n')
        for row in data:
            f.write(','.join(str(x) for x in row)+'\n')


def run_simulation(dimension, context, path, save_path):
    if dimension == 1:
        header = 'x'
    elif dimension == 2:
        header = 'x y'
    elif dimension == 3:
        header = 'x y z'

    filename = os.path.basename(path)
    vertices = parse_file(path)
    if (vertices != None):
        freq = context.scene.settings.frequency
        if freq == None:
            freq = 1
        avgs = averages(vertices, dimension, freq)
        file_path = f'{save_path}/{filename}{dimension}-dimension.csv'
        write_to_file(file_path, avgs, header)
