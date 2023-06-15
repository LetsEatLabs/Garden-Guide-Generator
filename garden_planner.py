import garden_schema as gs # garden_schema.py, actually calls GPT-4 API
import json


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

if __name__ == "__main__":

    with open("test_data.json", "r") as f:
        data = json.loads(f.read())

        for d in data:
            print(data[d])