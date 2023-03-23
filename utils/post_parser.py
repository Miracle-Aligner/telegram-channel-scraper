from selenium import webdriver
from dateutil.parser import parse
from selenium.webdriver.common.by import By


class Post (object):
    """
    Provides methods to parse post elements
    """
    def __init__(self, post_web_element):
        """
        Inits Post instance.

        :param post_web_element: driver element for a specific post
        """
        self.post_web_element = post_web_element

    def get_date(self):
        """
        Extracts the date from web element object.

        :return: Dictionary that includes datetime element
        """
        date_element = self.post_web_element.find_element(By.CLASS_NAME, "time")
        date = parse(date_element.get_attribute('datetime'))
        return {"datetime": date}

    def is_reply(self):
        """
        Finds out if post is a reply and if so provides a link to the post that was replied to.

        :return: Dictionary that includes bool is_reply flag and a reply_to str with url of the post replied to.
        """
        reply_elements = self.post_web_element.find_elements(By.CLASS_NAME, "tgme_widget_message_reply")
        is_reply = False
        reply_to = ''
        if len(reply_elements) != 0:
            is_reply = True
            reply_to = reply_elements[0].get_attribute('href')

        return { 'is_reply': is_reply,
                 'reply_to': reply_to}

    def is_forwarded(self):
        """
        Finds out if post is forwarded and if so provides a link to the original post.

        :return: Dictionary that includes bool is_forwarded flag and a forwarded_from str with url of an original post.
        """
        forwarded_elements = self.post_web_element.find_elements(By.CLASS_NAME, "tgme_widget_message_forwarded_from_name")
        is_forwarded = False
        forwarded_from = ''
        if len(forwarded_elements) != 0:
            is_forwarded = True
            forwarded_from = forwarded_elements[0].get_attribute('href')

        return { 'is_forwarded': is_forwarded,
                 'forwarded_from': forwarded_from}

    def is_edited(self):
        """
        Finds out if post was edited.

        :return: Dictionary that includes bool is_edited flag.
        """
        post_meta_element = self.post_web_element.find_element(By.CLASS_NAME, "tgme_widget_message_meta")
        date_element = self.post_web_element.find_element(By.CLASS_NAME, "time")
        is_edited = False

        if post_meta_element.text != date_element.text:
            is_edited = True

        return {'is_edited': is_edited}

    def get_views(self):
        """
        Get post's views.

        :return: Dictionary that includes views str property
        """
        post_views_element = self.post_web_element.find_element(By.CLASS_NAME, "tgme_widget_message_views")
        return {"views": post_views_element.text}

    def get_text(self):
        """
        Get post's text.

        :return: Dictionary that includes text str and lang str which is language code according to polyglot module.
                 If the language is undetectable lang equals "unknown".
        """
        post_text_elements = self.post_web_element.find_elements(By.CLASS_NAME, "tgme_widget_message_text")
        text = ''
        lang = ''
        if len(post_text_elements) != 0:
            from polyglot.detect import Detector
            try:
                text = post_text_elements[0].text
                lang = Detector(text).languages[0].code
            except:
                lang = 'unknown'

        return {
            'text': text,
            'lang': lang
        }

    def get_media(self):
        """
        Get post's media metadata.

        Note: video length param is present in a case when the video is a single attachment.
        Otherwise, video length equals None.

        :return: Dictionary that includes:
                 has_photo bool: does post have a photo attached
                 photo_urls list: list of urls of attached photos
                 has_video bool: does post have a photo attached
                 videos_meta list: list of objects with links to thumbnail and video length.
        """
        import re
        has_photo = False
        has_video = False
        photo_class = 'tgme_widget_message_photo_wrap'
        video_class = 'tgme_widget_message_video_thumb'
        video_duration_class = 'message_video_duration'
        url_pattern = r'url\("(.+?)"\)'

        photo_urls = []
        photo_elements = self.post_web_element.find_elements(By.CLASS_NAME, photo_class)
        if len(photo_elements) != 0:
            has_photo = True
            for photo in photo_elements:
                photo_style = photo.get_attribute('style')
                url_match = re.search(url_pattern, photo_style)
                photo_urls.append(url_match.group(1))

        video_duration = 0
        videos = []
        video_elements = self.post_web_element.find_elements(By.CLASS_NAME, video_class)
        if len(video_elements) != 0:
            has_video = True
            for (i, video) in enumerate(video_elements):
                video_length_el = self.post_web_element.find_elements(By.CLASS_NAME, video_duration_class)
                video_thumbnail_style = video.get_attribute('style')
                url_match = re.search(url_pattern, video_thumbnail_style)
                video_length = video_length_el[i].get_attribute('textContent') if len(video_length_el) > 0 else None
                videos.append({
                    'length': video_length,
                    'thumbnail_link': url_match.group(1)
                })

        return {
                    'has_photo': has_photo,
                    'photo_urls': photo_urls,
                    'has_video': has_video,
                    'videos_meta': videos
                }

    def get_post_id(self):
        """
        Eztracts post's id.

        :return: Dictionary that includes post_id integer.
        """
        import re
        post_element_class = 'tgme_widget_message'
        url_pattern = r'\d+'

        post_element = self.post_web_element.find_element(By.CLASS_NAME, post_element_class)
        element_style = post_element.get_attribute('data-post')
        url_match = re.search(url_pattern, element_style)

        return {
                    'post_id': url_match.group(0)
                }