import re
import json
import codecs
import re
import json


def get_data():
    # let's assume html is your HTML string

    # read html from file
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()

    pattern = r'window\.__ssr_data\s=\sJSON.parse\("(.*?)"\)'

    match = re.search(pattern, html)
    if match:
        json_string = match.group(1)
        # Unescape backslashes in the extracted string.
        json_string = json_string.replace('\\\\', '\\')
        data = json.loads(json_string)
        print(data)


def get_data2():
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()

    pattern = r'window\.__ssr_data\s=\sJSON.parse\("(.*?)"\)'
    match = re.search(pattern, html)

    if match:
        json_string = match.group(1)
        json_string = codecs.decode(json_string, 'unicode_escape')
        json_string = json_string.replace('\\\\', '\\')
        json_string = json_string.replace('\\"', '"')

        try:
            data = json.loads(json_string)
            print(data)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")

def process_dict(d):
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, str):
            new_dict[k] = bytes(v, 'latin1').decode('unicode_escape')
        elif isinstance(v, dict):
            new_dict[k] = process_dict(v)
        else:
            new_dict[k] = v
    return new_dict

def try_parse():
    data = get_data2()
    # Convert dictionary to JSON string
    data2 = process_dict(data)
    json_str = json.dumps(data)

    # Convert JSON string to byte string
    byte_str = json_str.encode('utf-8')

    # Decode byte string to normal utf-8 string
    utf8_str = byte_str.decode('unicode_escape')

    # Convert utf-8 string back to dictionary
    decoded_dict = json.loads(utf8_str)

    print("D")


import json
import simplejson
import simplejson.errors
import re


def get_data3():
    # read html from file
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()

    pattern = r'window\.__ssr_data\s=\sJSON.parse\("(.*?)"\)'
    match = re.search(pattern, html)

    if match:
        json_string = match.group(1)
        # Unescape backslashes in the extracted string.
        json_string = json_string.replace('\\\\', '\\')

        # Attempt to parse the JSON string using the built-in json library
        try:
            data = json.loads(json_string)
            print(data)
        except json.JSONDecodeError as e:
            # If parsing fails, attempt to parse it using simplejson
            try:
                data = simplejson.loads(json_string)
                print(data)
            except simplejson.errors.JSONDecodeError as e:
                print('Failed to decode JSON:', str(e))



import codecs
def convert_unicode_chars(input_string):
    return re.sub(r'\\\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), input_string)



def get_data4():



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




if __name__ == '__main__':
    get_data4()
