# Telegram Channel Scraper

This project provides a simple scraping tool for telegram channels' text and metadata.

## Contents 
1. [Installation](#installation)
2. [Usage](#usage)
3. [Class `ChannelParser`](#class-channelparser)
4. [Result](#result)

## Installation
1. Install Selenium. Comprehensive installation guide can be found [here](https://selenium-python.readthedocs.io/installation.html).
2. Install required packages using
`pip install -r requirements.txt`

You're all set!

## Usage
1. Import Channel parser:  
```from utils.channel_parser import ChannelParser```

2. Create ChannelParser instance:  
`parser = ChannelParser(channel_name, start_date)`

3. Perform scraping:  
`parser.scrape()`

4. Save result:  
`parser.save_json(path_to_save)`

Usage example also can be found in the [demo](https://github.com/Miracle-Aligner/telegram-channel-parser/blob/main/demo.py).
## Class `ChannelParser`

>     class ChannelParser(
>         channel_name,
>         start_date,
>         timezone='Europe/Kiev',
>         get_media=True,
>         get_text=True,
>         get_meta=True
>     )


Provides methods to scrape telegram channel texts + metadata, save a result in JSON.

Params:  
`channel_name`: Name of telegram channel to parse  
`start_date`: The date of the oldest massages to scrap  
`timezone`: Preferable timezone. The list of acceptable timezones corresponds to pytz.all_timezones  
`get_media`: Boolean. If True, collects meta-data about photos and videos in post.  
`get_text`: Boolean. If True, collects posts' texts.  
`get_meta`: Boolean. If True, collects meta-data about post, which includes: date, views,  
                 is reply / is forward / is edited flags.  


#### Methods

##### Method `save_json`

>     def save_json(
>         self,
>         path
>     )


Saves scraping_result object into JSON file.

:param `path`: Absolute file path for saving  
:return: String, describing save status.

    
##### Method `scrape`
>     def scrape(
>         self
>     )

Scrapes telegram channel content according to user-given channel name, flags and starting date.

:return: Scraped result in a form of a list


## Result
Result can be presented either in a form of a list or in a form of JSON file.

---
### Scraped data
The data that will be scraped according to flags you provided to ChannelParser constructor:

`get_text = True`  

`text`: text of particular post.    
`lang`: language code according to polyglot module. If the language is undetectable equals "unknown".    
<br><br>
`get_media = True`

`has_photo`: boolean flag. True if post has attached photo.  
`photo_urls`: list of links to attached photos.   
`has_video`: boolean flag. True if post has attached video.  
`videos_meta`: list of meta information of attached videos.  
`length`: length of attached video.    
`thumbnail_link`: link to thumbnail of attached video.

<br><br>
`get_meta = True`  

`channel_url`: link to scraped channel.   
`post_id`: post's unique for particular channel id.  
`datetime`: date of publication in a datetime format.  
`views`: string wit a views quantity.  
`is_reply`: boolean flag. True if post is a reply.  
`reply_to`: link to post that was replied to.  
`is_forwarded`: boolean flag. True if post is forwarded.  
`forwarded_from`: link to the original post.  
`is_edited`: boolean flag. True if post is edited.

<br><br>

---

### JSON Schema
The result presented in a form of JSON file with following JSON Schema:

```
{
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
        "channel_url": {
          "type": "string"
        },
        "post_id": {
          "type": "string"
        },
        "has_photo": {
          "type": "boolean"
        },
        "photo_urls": {
          "type": "array",
          "items": {}
        },
        "has_video": {
          "type": "boolean"
        },
        "videos_meta": {
          "type": "array",
          "items": [{
            "length": {
              "type": "string"
            },
            "thumbnail_link": {
              "type": "string"
            },
          }]
        },
        "text": {
          "type": "string"
        },
        "lang": {
          "type": "string"
        },
        "datetime": {
          "type": "string"
        },
        "views": {
          "type": "string"
        },
        "is_reply": {
          "type": "boolean"
        },
        "reply_to": {
          "type": "string"
        },
        "is_forwarded": {
          "type": "boolean"
        },
        "forwarded_from": {
          "type": "string"
        },
        "is_edited": {
          "type": "boolean"
        }
      }
    }
  ]
}
```
<br>

---
### Result sample

```
[
    {
        "channel_url": "https://t.me/s/lachentyt",
        "post_id": "27971",
        "has_photo": true,
        "photo_urls": [
            "https://cdn4.telegram-cdn.org/file/mEDe3JuXH-HhDIEo_XvIP2Wji2HQ_B8CbSPGW50swUCUZdF_k0-8dN3vOonKA76Ff-rUE1QaFJUvfUxjg8s7Zac_q6bpSA76LXiEpDaCZQ8QJFAdK3n7pHTrvGAdpAYX1E4fKMnaU0y5f347FdLRfBXAsYMxt_PivSIdP9Y2yoY1r5SAWCZJ1r0xmWJPgY5IEkOgJbCBW_oBy8O4NrnTxwtgfzujaLsfdO_WTJsPXy_U0_N-Pq6OGNa4zanwKDuP-iaw8g4-gKLO-NvAHT1K8DStiJRmK7hjhBJdQBPUF6cwheYAnuEGTHcsbiztaHg2-gPooMCz2VIgdY0JZgk2Tw.jpg"
        ],
        "has_video": false,
        "videos_meta": [],
        "text": "Україна подала до Фінляндії запит на винищувачі F/A-18, – Helsingin Sanomat.\n\nЙдеться про тристоронні переговори між Фінляндією, Україною та США.",
        "lang": "uk",
        "datetime": "2023-03-23 10:02:59+00:00",
        "views": "124.3K",
        "is_reply": false,
        "reply_to": "",
        "is_forwarded": false,
        "forwarded_from": "",
        "is_edited": false
    }
]
```
