from chat_elements import ACRONYMS, EMOTICONS
import pandas as pd
import numpy as np
import random
import json
import copy
import re

import nltk
import spacy
import string
from spellchecker import SpellChecker
from tqdm import tqdm

pd.options.mode.chained_assignment = None
tqdm.pandas()

spell = SpellChecker()

user2tag = {r"@\d+": "John", r"@[a-zA-z]+": "Agent"}


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # smileys
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def remove_emoticons(text):
    emoticon_pattern = re.compile(u"(" + u"|".join(k for k in EMOTICONS) + u")")
    return emoticon_pattern.sub(r"", text)


def tag_urls(text):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    return url_pattern.sub(r"(URL)", text)


def remove_html_tags(text):
    html_pattern = re.compile("<.*?>")
    return html_pattern.sub(r"", text)


def convert_acronyms(text):
    new_text = []
    for w in text.split():
        if w.upper() in ACRONYMS:
            new_text.append(ACRONYMS[w.upper()].lower())
        else:
            new_text.append(w)
    return " ".join(new_text)


def correct_spelling(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)


def tag_usernames(text):
    for user in user2tag:
        text = re.sub(user, user2tag[user], text)
    return text


def preprocess(
    df, emojis, emoticons, urls, html_tags, acronyms, spelling, usernames,
):
    if emojis:
        print("Removing emojis...")
        df["text"] = df["text"].progress_apply(lambda text: remove_emojis(text))
    if emoticons:
        print("Removing emoticons...")
        df["text"] = df["text"].progress_apply(lambda text: remove_emoticons(text))
    if html_tags:
        print("Removing html tags...")
        df["text"] = df["text"].progress_apply(lambda text: remove_html_tags(text))
    if urls:
        print("Tagging URLs...")
        df["text"] = df["text"].progress_apply(lambda text: tag_urls(text))
    if usernames:
        print("Tagging usernames...")
        df["text"] = df["text"].progress_apply(lambda text: tag_usernames(text))
    if acronyms:
        print("Converting acronyms...")
        df["text"] = df["text"].progress_apply(lambda text: convert_acronyms(text))
    if spelling:
        print("Spellchecking...")
        df["text"] = df["text"].progress_apply(lambda text: correct_spelling(text))

    df.to_csv(
        r"/afs/l2f/home/gnvm/lightning-convai/data/preprocessed.csv",
        index=False,
        header=True,
    )
