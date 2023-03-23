import os
from utils.channel_parser import ChannelParser

channels_to_parse = ['lachentyt']
for channel in channels_to_parse:
    parser = ChannelParser(channel, '2023-03-22')
    parser.scrape()

    path_to_save = os.path.abspath(f'./data/{channel}.json')
    parser.save_json(path_to_save)