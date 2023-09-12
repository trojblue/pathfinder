# Importing required libraries
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

import unibox


def parse_xml(xml_content: str, namespace=None) -> list:
    """Parse XML to extract 'CommonPrefixes'."""
    if namespace is None:
        namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    root = ET.fromstring(xml_content)
    return [
        cp.find("s3:Prefix", namespace).text
        for cp in root.findall(".//s3:CommonPrefixes", namespace)
    ]


def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url)
    return (
        response.text
        if response.status_code == 200
        else f"Failed: {response.status_code}"
    )


def generate_url(prefix: str, max_keys: int = 1000) -> str:
    """
    Generate an S3 URL with query parameters.
    >>> generate_url("sound/", 600)
    >>> "https://storage.sekai.best/sekai-assets/?delimiter=%2F&list-type=2&max-keys=500&prefix=sound%2F"
    """
    base_url = "https://storage.sekai.best/sekai-assets/"
    delimiter = "/"
    list_type = 2

    params = {
        "delimiter": delimiter,
        "list-type": list_type,
        "max-keys": max_keys,
        "prefix": prefix,
    }
    return f"{base_url}?{urlencode(params)}"


def try_it():
    url = generate_url("sound/scenario/voice/")
    xml_content = fetch_url(url)
    common_prefixes = parse_xml(xml_content)
    print(common_prefixes)


def parse_xmls():
    xml_paths = unibox.traverses()

    pass


# Example usage
if __name__ == "__main__":
    parse_xmls()
