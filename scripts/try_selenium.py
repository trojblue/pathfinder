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

if __name__ == '__main__':
    try_get_page()