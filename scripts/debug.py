import requests


def try_get_page():
    url = "https://bcy.net/illust/toppost100?type=week&date=20230612"
    res = requests.get(url)


    # save response html to file
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    pass


if __name__ == '__main__':
    try_get_page()