import re
import unibox


def find_twitter_ids(htmls):
    twitter_ids = set()  # Using a set to store unique Twitter IDs

    # Regular Expression pattern for finding Twitter URLs in the HTML content
    twitter_url_pattern = re.compile(r"https://twitter\.com/([a-zA-Z0-9_]+)")

    for html in htmls:
        for line in html:
            matches = twitter_url_pattern.findall(line)
            twitter_ids.update(matches)

    return twitter_ids


def id_extract_driver():
    eshi_folder = r"D:\CSC\pathfinder\DATA\eshi100"

    tr = unibox.UniTraverser(eshi_folder, include_extensions=[".html"])
    tr.traverse()
    html_files = tr.get_traversed_fils(relative_unix=False)  # get a list of paths

    htmls = []
    for i in html_files:
        i_read = unibox.loads(i)  # reads in as a list of strings
        htmls.append(i_read)

    ids = find_twitter_ids(htmls)
    ids = set(ids)
    unibox.saves(list(ids), "eshi_twitter_ids.txt")
    pass


if __name__ == "__main__":
    id_extract_driver()
