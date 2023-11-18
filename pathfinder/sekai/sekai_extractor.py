import requests
from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring, ParseError

# Constants
BASE_URL = "https://storage.sekai.best/sekai-assets/"


# --- Network Operations ---


def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Failed to fetch URL: {e}"


def generate_url(prefix: str, max_keys: int = 1000) -> str:
    """Generate an S3 URL with query parameters.
    输入文件目录prefix, 返回用来获取文件列表的url
    eg. https://sekai.best/asset_viewer/character/member
    prefix = "character/member"
    """
    params = {
        "delimiter": "/",
        "list-type": 2,
        "max-keys": max_keys,
        "prefix": prefix,
    }
    return f"{BASE_URL}?{urlencode(params)}"


# --- XML Parsing ---

def parse_xml(xml_content: str, namespace=None) -> list:
    """
    Parse XML to extract 'CommonPrefixes' or 'Key' values from 'Contents' elements.
    It first tries to find 'CommonPrefixes'. If none are found, it extracts 'Key' values from 'Contents'.
    """
    try:
        if namespace is None:
            namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        root = fromstring(xml_content)

        # Try to extract CommonPrefixes
        common_prefixes = [
            cp.find("s3:Prefix", namespace).text
            for cp in root.findall(".//s3:CommonPrefixes", namespace)
        ]

        if common_prefixes:
            return common_prefixes

        # If no CommonPrefixes, extract Key values from Contents
        return [
            contents.find("s3:Key", namespace).text
            for contents in root.findall(".//s3:Contents", namespace)
        ]
    except ParseError as e:
        return [f"XML Parsing failed: {e}"]
