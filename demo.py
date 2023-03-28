import os
from utils.channel_parser import ChannelParser

channels_to_parse = ['V_Zelenskiy_official', 'OGoMono', 'lachentyt']

for channel in channels_to_parse:
    parser = ChannelParser(channel, '2022-02-23 00:00:00', '2023-02-24 59:59:59')
    parser.scrape()

    path_to_save = os.path.abspath(f'./data/{channel}.json')
    parser.save_json(path_to_save)