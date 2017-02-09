import requests
import random
from io import BytesIO
from PIL import Image


def main():
    page = random.randint(1, 200056)
    museum_uri = "http://metmuseum.org"
    base_uri = "/api/collection/collectionlisting"
    image_uri = "http://images.metmuseum.org/CRDImages/"
    params = {
        "artist": "",
        "department": "",
        "era": "",
        "geolocation": "",
        "material": "Oil paint",
        "offset": "",
        "pageSize": 0,
        "perPage": 1,
        "offset": 1,
        "page": 1,
        "q": "",
        "showOnly": "openaccess",
        "sortBy": "Relevance",
        "sortOrder": "asc"
    }
    response = requests.get("{0}{1}".format(museum_uri, base_uri), params=params).json()
    page = random.randint(1, response["totalResults"])
    params["page"] = page
    params["offset"] = page
    response = requests.get("{0}{1}".format(museum_uri, base_uri), params=params).json()
    print response["results"][0]["url"]
    objects = response["results"]
    for obj in objects:
        uri = obj["largeImage"].replace("web-large", "original")
        url = "{0}{1}".format(image_uri, uri)
        print url
        image_response = requests.get(url, stream=True)
        print image_response
        image = Image.open(image_response.raw)
        image.save("image.jpg")

    # ?artist=&department=&era=&geolocation=&material=&offset=0&pageSize=0&perPage=20&q=&showOnly=openaccess&sortBy=Relevance&sortOrder=asc
    # ?artist=&department=&era=&geolocation=&material=&offset=0&pageSize=0&perPage=20&q=van+gogh&showOnly=openaccess&sortBy=Relevance&sortOrder=asc

main()
