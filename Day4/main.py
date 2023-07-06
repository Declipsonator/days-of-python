import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


def slow_scroll():
    try:
        driver.execute_async_script(
            """
            let scrollDistance = 1600;  // Increased scroll distance to 800 pixels
            let delay = 150;  // Decreased delay to 200 milliseconds
            let timeout = 2000;  // Timeout after 1 second (1000 milliseconds)

            let callback = arguments[arguments.length - 1];
            let currentScroll = 0;
            let startTime = new Date().getTime();

            function scrollDown() {
                window.scrollBy(0, scrollDistance);  // Use scrollBy instead of scrollTo

                let currentTime = new Date().getTime();
                if (window.pageYOffset < (document.body.scrollHeight || document.documentElement.scrollHeight) && (currentTime - startTime) < timeout) {
                    setTimeout(scrollDown, delay);
                } else {
                    callback((document.body.scrollHeight || document.documentElement.scrollHeight));
                }
            }

            scrollDown();
            """
        )
    except Exception:
        pass


# Using selenium for fun
def scrape(reddit, num_posts):
    """
    :param reddit: The reddit to scrape. Example: "r/math"
    :param num_posts: The # of posts to return. If a reddit doesn't have enough it will return as much as it has.
    :return: array of jsons of reddit posts
    """

    driver.get('https://reddit.com/' + reddit)
    elements = WebDriverWait(driver, 100).until(
        lambda x: x.find_elements(By.XPATH, "//span[text()='Posted by']"))
    last_elements_count = len(elements)

    while len(elements) < + num_posts + 5:
        slow_scroll()
        time.sleep(1)
        elements = driver.find_elements(By.XPATH, "//span[text()='Posted by']")
        if len(elements) <= last_elements_count:
            break
        last_elements_count = len(elements)

    slow_scroll()
    elements = driver.find_elements(By.XPATH, "//span[text()='Posted by']")

    if len(elements) > num_posts + 5:
        elements = elements[5:num_posts + 5]

    elements = [thing.find_element(By.XPATH, "../../../../..") for thing in elements]

    posts = []

    for i in range(0, len(elements)):
        post = elements[i]
        try:
            votes = int(post.find_element(By.XPATH, "./div[2]/div/div").get_attribute("innerHTML").replace("Vote", "0"))
            link = post.find_element(By.XPATH, "./div[3]/div[2]/div/a").get_attribute("href")
            author = post.find_element(By.XPATH, "./div[3]/div/div/div/div/div/a").get_attribute("innerHTML")
            post_date = post.find_element(By.XPATH, "./div[3]/div/div/div/span[2]").get_attribute("innerHTML")
            title = post.find_element(By.XPATH, "./div[3]/div[2]/div/a/div/h3").get_attribute("innerHTML")
            media_stuff = [img.find_elements(By.XPATH, "./figure/div/img") for img in
                           post.find_elements(By.XPATH, "./div[3]/div[3]/div/div[2]/div/div/div/div[1]/ul/*")]
            media = []
            for thing in media_stuff:
                if len(thing) > 0:
                    media.append(thing[0].get_attribute("src"))
            posts.append({"votes": votes, "author": author, "post_date": post_date, "title": title, "media": media,
                          "link": link})

        except Exception as e:
            print(e)

    return posts


print(json.dumps(scrape('r/rateme', 50)))
driver.quit()
