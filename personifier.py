# This code processes Twitter customer support corpus from kaggle.
#
# First of all you need to download the original corpus and save the "twcs.csv" file into the data/twitter/ folder.


import pandas as pd
import numpy as np
import random
import json
import copy
import re
import langdetect
from tqdm import tqdm
from utilities import brands
from metadataExtractor import get_brand_mentions


def get_brand_tweets(dataframe, brand):
    """
    Filters out all tweets that dont belong to a specific brand
    :param dataframe: dataframe from kaggle with all the tweets.
    :param brand: brand that we want to keep.
    """
    return dataframe[dataframe["author_id"] == brand]


def get_begin_of_conversation(dataframe):
    """
    I assume that tweets that have the 'in_response_to_tweet_id' equal to NaN and
    that, at the same time, are inbound tweets, start a conversation with a specific brand.
    :param dataframe: dataframe from kaggle with all the tweets.
    """

    dataframe = dataframe[dataframe["in_response_to_tweet_id"].isnull()]
    return dataframe[dataframe["inbound"] == True]


# get_begin_of_conversation(df).head()
# As we ca observe some tweets have multiple replies... but since the 'response_tweet_id' field is a string we will need to convert that string into a list of ids.


def response_tweet_ids(string):
    return list(map(int, string.split(",")))


def get_brand_from_tweet(string):
    for brand in brands:
        if brand in string:
            return brand
    return None


# ## Helper Classes
#
# Some classes that will help structuring the conversations
class Conversation:
    def __init__(self, utterances=[], brand="", user=""):
        self.brand = brand
        self.user = user
        self.utterances = utterances

    def get_rand_utterance(self):
        return random.choice(self.utterances).text

    def add_utterance(self, utterance):
        self.utterances.append(utterance)


class Utterance:
    def __init__(self, speaker="", text=""):
        self.speaker = speaker
        self.text = text


# # Rebuild Conversations
#
# Now that we have some helper functions we can rebuild the conversations. Also, after observing some cases of tweets with multiple replies I arrived to the conclusion that this is the case in which the support agent writes several tweets in order to reply to the customer, but in all those cases the client replies only to the last tweet in order to continue the conversation.


def rebuild_conversations(boc_df, dataframe):
    """
    This funcion will loop over all "Begin of Conversation" tweets and concatenate all
    the consecutive tweets.
    :param boc_df: Dataframe with the tweets that represent "begin of conversations".
    :param dataframe: kaggle dataframe with all the tweets,
    """
    conversations = []
    for _, row in tqdm(
        boc_df.iterrows(), desc="Rebuilding conversations...", total=len(boc_df)
    ):
        conversation = Conversation()
        current_tweet = row
        conversation.utterances = [
            Utterance(row["author_id"], row["text"]),
        ]
        while type(current_tweet["response_tweet_id"]) is str:
            replie_ids = response_tweet_ids(current_tweet["response_tweet_id"])
            replies = dataframe[dataframe["tweet_id"].isin(replie_ids)].sort_values(
                by="created_at", ascending=True
            )
            conversation.utterances += [
                Utterance(speaker, text)
                for speaker, text in zip(replies["author_id"], replies["text"])
            ]
            current_tweet = replies.iloc[-1]

        brand_mentions = get_brand_mentions(
            "\n".join([utterance.text for utterance in conversation.utterances])
        )

        if (
            len(brand_mentions) > 0
            and is_in_english(conversation)
            and not has_empty_utterances(conversation)
        ):
            conversation.brand = brand_mentions[0]
            conversations.append(conversation)

    return conversations


def has_empty_utterances(conversation):
    for utterance in conversation.utterances:
        if pd.isnull(utterance.text):
            return True
    return False


def is_in_english(conversation):
    for utterance in conversation.utterances:
        try:
            if langdetect.detect(utterance.text) != "en":
                return False
        except:
            continue
    return True


# It simply takes too much time through all the brands and rebuild all the conversations. For that reason we will isolate specific brands and rebuild the conversations for them.


def filter_brand_bocs(boc_df, brandname):
    ids = []
    for i in tqdm(
        range(len(boc_df["tweet_id"])),
        desc="Filtering brands BOC...",
        total=len(boc_df),
    ):
        if (
            not pd.isnull(boc_df.iloc[i]["text"])
            and brandname in boc_df.iloc[i]["text"]
        ):
            ids.append(boc_df.iloc[i]["tweet_id"])

    return boc_df[boc_df["tweet_id"].isin(ids)]


def generate_personachat_json(
    conversations, filename, limit,
):
    entries = []

    for conversation in tqdm(
        conversations, desc="Creating CS Persona-Chat...", total=len(conversations)
    ):
        # para limitar nmr de entradas, podes apagar para fazer todo.
        if len(entries) == limit:
            break

        entry = {"personality": [], "utterances": []}
        utterances = []

        for i in range(1, len(conversation.utterances)):
            if conversation.utterances[i].speaker == "XboxSupport":
                dic = {
                    "candidates": [],
                    "history": [
                        utterance.text for utterance in conversation.utterances[0:i]
                    ],
                }
                for j in range(10):
                    c = random.choice(conversations)
                    u = c.get_rand_utterance()
                    dic["candidates"].append(u)
                dic["candidates"].append(conversation.utterances[i].text)
                utterances.append(dic)
        if len(utterances) != 0:
            entry["utterances"] = utterances
            entries.append(entry)

    with open(filename, "w") as outfile:
        json.dump(entries, outfile, indent=4)


def personify(df, filename, brand, limit):
    boc_df = get_begin_of_conversation(df)
    if brand:
        conversations = rebuild_conversations(filter_brand_bocs(boc_df, brand), df)
    else:
        conversations = rebuild_conversations(boc_df, df)

    generate_personachat_json(conversations, filename, limit)
