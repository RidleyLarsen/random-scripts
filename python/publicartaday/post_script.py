import facebook
import requests
import random
import json
from datetime import datetime
from PIL import Image

MUSEUM_URI = "http://metmuseum.org"
MUSEUM_API_URI = "/api/collection/collectionlisting"
MUSEUM_IMAGE_URI = "http://images.metmuseum.org/CRDImages/"


def load_config():
    '''
        Loads configuration file as JSON. See config.json.example for more details.
    '''
    f = open("config.json", "r")
    fr = f.read()
    f.close()
    return json.loads(fr)


def get_museum_response(params):
    '''
        Calls the Museum API with params and returns the response as JSON.
    '''
    return requests.get("{0}{1}".format(MUSEUM_URI, MUSEUM_API_URI), params=params).json()


def main():
    config = load_config()
    graph = facebook.GraphAPI(config["FB_ACCESS_TOKEN"])
    # Most of these params don't change. 'openaccess' == Public Domain.
    today = datetime.now().weekday()
    params = {
        "material": config["MATERIAL_DAYS"][str(today)],
        "pageSize": 0,
        "perPage": 1,
        "offset": 1,
        "page": 1,
        "showOnly": "openaccess"
    }
    # This requires two requests - one to get how many pieces there are, then another to get the random piece.
    response = get_museum_response(params)
    page = random.randint(1, response["totalResults"])
    params["page"] = page
    params["offset"] = page

    # Get the piece using the random number we generated.
    response = get_museum_response(params)
    obj = response["results"][0]
    obj_image_uri = obj["largeImage"].replace("web-large", "original")

    # Use the new "original" sized image uri to create the image URL.
    image_url = "{0}{1}".format(MUSEUM_IMAGE_URI, obj_image_uri)

    # This will be the posts's caption on Facebook (or other networks when added.)
    caption = u"{0} - {1} - {2}{3}".format(obj["title"], obj["description"], MUSEUM_URI, obj["url"])

    # Get, then save the image.
    image_response = requests.get(image_url, stream=True)
    image = Image.open(image_response.raw)
    image.save("image.jpg")

    # Read the image, then post it to the page's Facebook wall.
    f = open("image.jpg", "r")
    fr = f.read()
    f.close()
    graph.put_photo(fr, caption=caption)

if __name__ == '__main__':
    main()
