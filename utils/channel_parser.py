import json
import pytz
import datetime
from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.post_parser import Post


class ChannelParser (object):
    """
    Provides methods to scrape telegram channel texts + metadata, save a result in JSON.
    """
    def __init__(self,
                 channel_name,
                 start_date,
                 finish_date = None,
                 timezone = 'Europe/Kiev',
                 get_media = True,
                 get_text = True,
                 get_meta = True):
        """

        :param channel_name: Name of telegram channel to parse
        :param start_date: The date of the oldest messages to scrap
        :param finish_date: The date of the newest messages to scrap default None scraps to the newest one.
        :param timezone: Preferable timezone. The list of acceptable timezones corresponds to pytz.all_timezones
        :param get_media: Boolean. If True, collects meta-data about photos and videos in post.
        :param get_text: Boolean. If True, collects posts' texts.
        :param get_meta: Boolean. If True, collects meta-data about post, which includes: date, views,
                         is reply / is forward / is edited flags.
        """
        self.URL = "https://t.me/s/" + channel_name
        self.timezone = pytz.timezone(timezone)

        self.start_date = parse(start_date)
        self.start_date = self.timezone.localize(self.start_date)
        if finish_date is not None:
            self.finish_date = parse(finish_date)
            self.finish_date = self.timezone.localize(self.finish_date)
        else:
            self.finish_date = None

        self.get_media = get_media
        self.get_text = get_text
        self.get_meta = get_meta

    def scrape (self):
        """
        Scrapes telegram channel content according to user-given channel name, flags and starting date.

        :return: Scraped result in a form of a list
        """
        # Loading the preview page
        driver = webdriver.Chrome()
        driver.get(self.URL)

        # Scrolling to the top of a page to retrieve older posts made in boundaries [start_date, now]
        while self.start_date < parse(driver.find_element(By.CLASS_NAME, "tgme_widget_message_date")
                                            .find_element(By.TAG_NAME, "time").get_attribute('datetime')):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)

        # Getting all post elements
        posts_elements = driver.find_elements(By.CLASS_NAME, "tgme_widget_message_wrap")

        # Filtering posts that were made after user-entered scraping start date
        filtered_posts_elements = self._filter_elements(posts_elements)

        # Parsing filtered posts and saving results into list
        self.scraping_result = self._parse_posts(filtered_posts_elements)
        driver.close()

        return self.scraping_result

    def _filter_elements(self, elements):
        """
        Filters posts by start_date and finish_date (if specified) criteria.

        Elements are stored in a list in the descending date order.
        By enumerating through an elements list find the index of the last post that meets start_date criteria.
        The return result is a sliced by start_msg_idx initial list.

        :param elements: Posts elements that needs to be filtered.
        :return: List of posts filtered by start_date criteria.
        """
        start_msg_idx = None

        for i, element in enumerate(elements):
            message = Post(element)
            if self.start_date <= message.get_date()['datetime'].astimezone(self.timezone):
                start_msg_idx = i
                break

        if self.finish_date is None:
            return elements[start_msg_idx:]
        else:
            fin_msg_idx = None
            elements_half_filtered = elements[start_msg_idx:]
            elements_half_filtered.reverse()
            for i, element in enumerate(elements_half_filtered):
                message = Post(element)
                if self.finish_date >= message.get_date()['datetime'].astimezone(self.timezone):
                    fin_msg_idx = i
                    break
            return elements_half_filtered[fin_msg_idx:]

    def _parse_posts(self, posts_elements):
        post_objects = []
        for post_element in posts_elements:
            post = Post(post_element)

            post_dict = dict()

            post_id = post.get_post_id()
            post_dict.update({"channel_url": self.URL})
            post_dict.update(post_id)

            if self.get_media == True:
                media_data = post.get_media()
                post_dict.update(media_data)

            if self.get_text == True:
                post_text = post.get_text()
                post_dict.update(post_text)

            if self.get_meta == True:
                date = post.get_date()
                post_dict.update(date)

                views = post.get_views()
                post_dict.update(views)

                is_reply = post.is_reply()
                post_dict.update(is_reply)

                is_forwarded = post.is_forwarded()
                post_dict.update(is_forwarded)

                is_edited = post.is_edited()
                post_dict.update(is_edited)

            post_objects.append(post_dict)

        return post_objects

    def save_json(self, path):
        """
        Saves scraping_result object into JSON file.

        :param path: Absolute file path for saving
        :return: String, describing save status.
        """
        try:
            with open(path, "w", encoding='utf8') as outfile:
                json.dump(self.scraping_result, outfile, default=str, ensure_ascii=False, indent=4)
            return "Saved successfully."

        except:
            return "Error saving file."

