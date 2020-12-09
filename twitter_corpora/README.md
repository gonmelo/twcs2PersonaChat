# Data:

## Conversational Data:

The conversational data comes from the [Customer Support on Twitter Corpus](https://www.kaggle.com/thoughtvector/customer-support-on-twitter) from Kaggle.


Inside the 'twitter' folder you can several folder with the name of different brands. All these folders contain two files:

- *A CSV file* with all the conversation threads for that specific brand.
- *A JSON file*: with (*query*, *answer*, *context*) triplets in which the *query* is a message that triggers a tweet from the brand, the *answer*. The *context* is a list of all messages exchanged between the brand and the user before the *query* message.

**Note:** When creating the triplets for the JSON file we decided to exclude all triplets in which the brand redirects the user to *direct messages* and we all triplets in which the *query* is not written in english.


### Technical Corpora:

| XBox Corpus                  |       |
| ---------------------------- |:-----:|
| nº of triplets               | 15332 |
| Avg query size               | 19.85 |
| Avg answer size              | 19.04 |
| Avg context size (words)     | 33.51 |
| Avg context size (sentences) | 1.704 |

| Playstation Corpus           |       |
| ---------------------------- |:-----:|
| nº of triplets               | 11977 |
| Avg query size               | 19.01 |
| Avg answer size              | 15.66 |
| Avg context size (words)     | 16.08 |
| Avg context size (sentences) | 0.889 |

| Apple Corpus                 |       |
| ---------------------------- |:-----:|
| nº of triplets               | 38078 |
| Avg query size               | 18.65 |
| Avg answer size              | 22.39 |
| Avg context size (words)     | 16.58 |
| Avg context size (sentences) | 0.790 |

### Airline Corpora:

| British Airlines Corpus      |       |
| ---------------------------- |:-----:|
| nº of triplets               | 22167 |
| Avg query size               | 21.95 |
| Avg answer size              | 20.96 |
| Avg context size (words)     | 22.85 |
| Avg context size (sentences) | 1.040 |

| Delta Airlines Corpus        |       |
| ---------------------------- |:-----:|
| nº of triplets               | 28405 |
| Avg query size               | 20.64 |
| Avg answer size              | 17.96 |
| Avg context size (words)     | 21.27 |
| Avg context size (sentences) | 1.054 |

| Southwest Airlines Corpus    |       |
| ---------------------------- |:-----:|
| nº of triplets               | 20708 |
| Avg query size               | 18.90 |
| Avg answer size              | 19.97 |
| Avg context size (words)     | 13.11 |
| Avg context size (sentences) | 0.636 |

| American Airlines Corpus    |       |
| ---------------------------- |:-----:|
| nº of triplets               | 28986 |
| Avg query size               | 20.33 |
| Avg answer size              | 18.29 |
| Avg context size (words)     | 18.78 |
| Avg context size (sentences) | 0.915 |
