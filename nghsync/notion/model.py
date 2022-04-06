from dataclasses import dataclass


@dataclass
class Task:
    number: int
    name: str
    project_id: str
    status: str

    @classmethod
    def from_json(cls, j):
        name = ''.join([t['plain_text'] for t in j['properties']['Name']['title']])
        number = cls.get_number_from_name(name)
        project_id = None
        status = None

        if len(j['properties']['Project']['relation']):
            project_id = j['properties']['Project']['relation'][0]['id']

        if j['properties']['Status']['select']:
            status = j['properties']['Status']['select']['name']

        return cls(number, name, project_id, status)

    def get_number_from_name(name):
        name_parts = name.split(' ')
        id_candidates = [p for p in name_parts if '#' in p]
        if len(id_candidates) == 0:
            raise ValueError(f"Expected '#' not found in issue name '{name}'.")
        elif len(id_candidates) > 1:
            raise ValueError(f"More than 1 '#' found in issue name '{name}'.")
        id_num = id_candidates[0]
        number_str = id_num.replace('#', '').strip()
        number = int(number_str)
        return number


@dataclass
class Project:
    name: str
    project_id: str

    @classmethod
    def from_json(cls, j):
        name = ''.join([t['plain_text'] for t in j['properties']['Name']['title']])
        project_id = j['properties']['project']['id']
        return cls(name, project_id)
