r"""
Command Line Interface
=======================
   Commands:
   - preprocess: Pre-process the original CSV file, with multiple steps available.
   - getMetadata: Fetch meta-data related to the original dataset.
   - personify: Generate the Persona-Chat formatted file.
"""
import click
from preprocessor import preprocess
from metadataExtractor import getMetadata
from personifier import personify
import pandas as pd

df = pd.read_csv("twitter_corpora/twitter/twcs.csv")


@click.group()
def cli():
    pass


@cli.command(name="preprocess")
@click.option("--emojis", default=True, help="Remove emojis")
@click.option("--emoticons", default=True, help="Remove emoticons")
@click.option("--urls", default=True, help="Tag URLs -> (URL)")
@click.option("--html_tags", default=True, help="Remove html tags")
@click.option("--acronyms", default=True, help="Convert acronyms to meaning")
@click.option("--spelling", default=False, help="Spellcheck")
@click.option("--usernames", default=False, help="Tag usernames ")
def preprocessCSV(
    emojis: str,
    emoticons: str,
    urls: str,
    html_tags: str,
    acronyms: str,
    spelling: str,
    usernames: str,
) -> None:
    preprocess(
        df, emojis, emoticons, urls, html_tags, acronyms, spelling, usernames,
    )


@cli.command(name="getMetadata")
def extractMetadata() -> None:
    getMetadata(df)


@cli.command(name="personify")
@click.option("--brand", default=None, help="Name of the brand ")
@click.option("--limit", default=-1, help="Max number of conversations")
@click.option(
    "--filename", default="personaChatCS.json", help="Name of the generated file"
)
def personifyCS(brand: str, limit: int, filename: str) -> None:
    preprocessed = pd.read_csv("preprocessed.csv")
    personify(preprocessed, filename, brand, limit)


if __name__ == "__main__":
    cli()
