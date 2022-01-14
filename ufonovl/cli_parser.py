import argparse
from ufonovl.reddit.feed import new_reddit_posts
from ufonovl.reddit.history import reddit_history

def cli_parser():
    utn_parser = argparse.ArgumentParser(description='An NLP pipeline that detects new textual information about UFOs/UAPs')

    utn_parser.add_argument('interval', action='store', choices=['new', 'old'], help="Process new or old reddit posts")

    args = utn_parser.parse_args()

    interval = args.interval

    if interval == "new":
        new_reddit_posts()

    elif interval == "old":
        reddit_history()