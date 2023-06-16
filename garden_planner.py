import garden_schema as gs # garden_schema.py, actually calls GPT-4 API
import json, os

from pathlib import Path

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


#####
def get_test_schema():
    """
    Just generates some test data and saves it as a JSON so we can test the templating 
    without repeated calls to OpenAI.

    Output: test_data.json
    """

    plants = ["radishes", "potatoes", "turnips", "thyme"]
    garden_object = {}

    for plant in plants:
        plant_data = gs.get_plant_data(plant, "8b")
        garden_object[plant] = plant_data

    with open("test_data.json", "w") as f:
        jdata = json.dumps(garden_object)

        f.write(jdata)
#####
def sanitize_json(data):
    """
    Goes through the JSON and makes sure that all the values are valid JSON.
    """

    for key, value in data.items():
            try:
                data[key] = json.loads(value)
            except (TypeError, json.JSONDecodeError):
                # If it's a non-string value or not a valid JSON string, continue
                pass
                
    return data

#####

if __name__ == "__main__":

    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('template.html')

    with open("test_data.json", "r") as f:
        data = json.loads(f.read())

        data = sanitize_json(data)

        filename = os.path.join(root, 'output.html')
        with open(filename, 'w') as fh:
            fh.write(template.render(plants=data))

        htmldoc = HTML(string=open("output.html", "r").read(), base_url="")
        

        Path("out.pdf").write_bytes(htmldoc.write_pdf())