import re
import json
from selenium import webdriver


def try_get_page():
    url = "https://bcy.net/illust/toppost100?type=week&date=20230612"

    # You need to have the correct WebDriver executable (geckodriver for Firefox) in your PATH
    driver = webdriver.Chrome()

    driver.get(url)

    # Wait for JavaScript to execute and modify the HTML
    # You may need to wait for more than 5 seconds depending on the site
    driver.implicitly_wait(5)

    html = driver.page_source

    # Save the resulting HTML to a file
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(html)

    driver.quit()


def convert_unicode_chars(input_string):
    return re.sub(r'\\\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), input_string)


def get_data():
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Use regular expression to match the JSON string pattern
    matches = re.search(r'window\.__ssr_data\s*=\s*JSON\.parse\(\s*\n*\s*"(.+?)"\s*\n*\s*\)', html)

    if matches:
        # Extract the matched JSON string
        json_string = matches.group(1)
        # convert "\"" to """
        json_string_conv = json_string.replace('\\"', '"')
        json_string_conv = json_string_conv.replace('\\\\"', '"')
        json_string_conv = json_string_conv.replace('}"', '}')
        json_string_conv = json_string_conv.replace('"{', '{')

        # convert unicode characters to utf-8
        json_string_conv2 = convert_unicode_chars(json_string_conv)

        # convert the JSON string to a dictionary
        data = json.loads(json_string_conv2)

        # dump the dictionary to a JSON file
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    else:
        print("No JSON string found.")


def try_chain():
    try_get_page()
    get_data()


if __name__ == '__main__':
    try_chain()
