import json

INSTANCE_MAP = {
    'point': 0,
    'polyline': 1,
    'polygon': 2,
    'boundingbox': 3,
    'rotatedbox': 4,
    'ellipse': 5,
    'cuboid': 6
}


def convert():
    '''
    Converts supperannote format into YOLO.
    Not sure about the ids and if points can have width and height
    '''

    # Erases the previous contents of YOLO.txt file.
    with open('./converter/YOLO.txt', 'w') as to_erase:
        to_erase.write('')

    instances = open('./converter/example.json')
    json_data = json.load(instances)
    instances = json_data['instances']
    for instance in instances:
        instance_type = instance['type']
        id = INSTANCE_MAP[instance_type]

        x = instance['x']
        y = instance['y']

        width = instance.get('width', 0)

        height = instance.get('width', 0)

        row = f'{id} {x} {y} {width} {height}\n'

        with open('./converter/YOLO.txt', 'a') as yolo:
            yolo.write(row)


convert()
