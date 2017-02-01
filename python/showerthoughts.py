from __future__ import print_function
import json
import requests
import subprocess

def harvest_titles(jsonobj):
    '''
        Create a list of post titles from the response.
        These are the "shower thoughts" used in the fortune file.
    '''
    lst = []
    try:
        for post in jsonobj["data"]["children"]:
            # Encode the post titles with ascii for compatibility.
            title = post["data"]["title"].encode('ascii', 'ignore')
            lst.append(title)
    except KeyError: # Either no data or no children.
        pass
    return lst

def main():
    print("Grabbing shower thoughts.")
    api_uri = "https://www.reddit.com/r/showerthoughts/top.json?t=all,limit=100"
    r = requests.get(api_uri).json()
    db = harvest_titles(r)
    while len(db) < 500:
        # Pagination in the reddit API is determined by whatever the last object returned was.
        after = r["data"]["children"][-1]["data"]["name"]
        print("Next: ", after)
        # This grabs the last post's "name" field and sticks it in the querystring.
        r = requests.get("{0}{1}{2}".format(api_uri, "&after=", after)).json()
        titles = harvest_titles(r)
        if len(titles) < 1: # If an error or no posts returned (API throttling)
            break
        db += titles
    f = open("showerthoughts", "w")
    for title in db:
        f.write(title + "\n")
        f.write("%\n") # Fortune files are delimited by lines with a single %.
    f.close()
    try:
        # Build the file offset table. Used by fortune.
        subprocess.check_call(["strfile", "-c", "%", "showerthoughts", "showerthoughts.dat"])
    except IOError as e:
        print("Had a problem building the fortune file.")
        print(e)
    print("Wrote titles to file.")


if __name__ == '__main__':
    main()
