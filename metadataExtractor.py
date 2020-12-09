import pandas as pd
import re
from tqdm import tqdm


# ## Brand Volume
def get_brand_mentions(tweet):
    return re.findall("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)", tweet)


def count_brand_mentions(tweets):
    """
    This function goes through all the tweets extracting tweet mentions and counting
    how many times they appear.
    :param tweets: List with the all the tweets text.
    """
    brands = {}
    for tweet in tqdm(tweets, desc="Counting brand mentions...", total=len(tweets)):
        mentions = get_brand_mentions(tweet)
        for mention in mentions:
            brands[mention] = 1 if mention not in brands else brands[mention] + 1

    return sorted(brands.items(), key=lambda kv: kv[1], reverse=True)


def getMetadata(df):
    print("Number of turns: {}".format(len(df)))
    brand2count = count_brand_mentions(df["text"].tolist())
    print("Number of mentions of top 20 brands:")
    print(brand2count[:20])
