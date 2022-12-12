import json
from superannotate import SAClient


PROJ_NAME = 'incurso_application'
print('Provide TOKEN: ')
TOKEN = str(input())
list_of_images = [
    {'name': 'Bloodborne1',
     'url': 'https://image.api.playstation.com/vulcan/img/rnd/202010/2614/NVmnBXze9ElHzU6SmykrJLIV.png'},
    {'name': 'Bloodborne2',
     'url': 'https://m.media-amazon.com/images/M/MV5BMWQwZTQxMGUtZmQ5NS00YmZiLWIyOGQtZjg5ZmE4MzQyYTAxXkEyXkFqcGdeQXVyMTQyNTU3NTg@._V1_FMjpg_UX1000_.jpg'},
    {'name': 'Bloodborne3',
     'url': 'https://i.insider.com/57ab4ba5ce38f252008b5d56?width=700'}
]
attributes_list = [
    {
        "group_type": "radio",
        "name": "something",
        "attributes": [
            {
                "name": "whatever"
            }
        ],
        "default_value": "Default"
    }]


team_1 = SAClient(token=TOKEN)


def sa_init(team):
    '''
    Creates project, folder for some reason, annotation class,
    uploads images from the list. Everything that has to be done once. 
    '''
    team.create_project(
        project_name=PROJ_NAME,
        project_description='Incurso description. Help me. :D',
        project_type='Vector')

    team.create_folder(
        project=PROJ_NAME,
        folder_name="Bloodborne_pictures")

    team.create_annotation_class(
        project=PROJ_NAME,
        name='Bloodborne3',
        color='#7C1A05',
        class_type='tag',
        attribute_groups=attributes_list)

    team.attach_items(
        project=PROJ_NAME,
        attachments=list_of_images,
        annotation_status='NotStarted'
    )


# Since listed method .add_annotation_point_to_image()
# on https://doc.superannotate.com/docs/sdk-import-annotations
# Doesn't exist, had to create JSON file and add annotations by using it.
# UPD: I guess I also need to make a JSON file builder, which would requiest the data,
# Take metadata and unite it with instances JSON. And that unified JSON will be uploaded.
def build_json_to_upload(chose: int):
    '''
    Receives metadata of image, unites it with instances.json with 
    the instructions to form the Christmas tree(triangle).
    Created file gets the name automaticaly and is created at
    ./app/annotations/
    '''

    instances = open('./app/instances.json')
    data1 = json.load(instances)

    data = data1['instances']

    dictionary = {
        'metadata': annotations[chose]['metadata'],
        'instances': data,
        'tags': [],
        'comments': []
    }

    with open('./app/sample.json', 'w') as outfile:
        json.dump(dictionary, outfile)

    s = open('./app/sample.json')
    data = json.load(s)
    name = data['metadata']['name']

    with open(f'./app/annotations/{name}___objects.json', 'w') as outfile:
        json.dump(dictionary, outfile)


def christmas_tree(team):
    '''
    Uploads JSON applications into the project
    '''
    team.upload_annotations_from_folder_to_project(
        project=PROJ_NAME,
        folder_path='./app/annotations')


def set_status(team, status):
    '''
    Sets status on all the images in project
    '''
    team.set_annotation_statuses(PROJ_NAME, status)


def download_annotations(team):
    '''
    Downloads the anotations and saves them. 
    Added cause it's writen to save them in the task 
    I received. :D
    '''
    team.download_annotations(
        project=PROJ_NAME,
        path='./app/annotations_after/'
    )


def run_first_task(sa_instance):

    sa_init(sa_instance)

    annotations = sa_instance.get_annotations(project=PROJ_NAME)

    for i in range(len(annotations)):
        build_json_to_upload(i)

    christmas_tree(sa_instance)

    set_status(sa_instance, 'Completed')

    download_annotations(sa_instance)


run_first_task(team_1)
