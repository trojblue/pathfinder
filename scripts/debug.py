import requests


def try_get_page():
    url = "https://bcy.net/illust/toppost100?type=week&date=20230612"
    res = requests.get(url)


    # save response html to file
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    pass




def load2():
    import json

    json_string = """
    {
       \"user\":{
          \"uid\":\"0\",
          \"area\":{}
       }
    }
    """

    # Convert the JSON string to a Python dictionary
    data = json.loads(json_string)

    # Now `data` is a Python dict
    print(data)

    json_object = json.loads(json_string)


if __name__ == '__main__':
    try_get_page()