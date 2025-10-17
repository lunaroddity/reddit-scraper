# reddit-scraper
This repository contains code for a scraper for the r/relationship_advice subreddit.

## Information about the dataset and corpus
An initial scrape was performed on the top 300 posts of all time in the r/relationship_advice subreddit. To mitigate the influence of other users in a user's narration of an interpersonal conflict that they experienced, updates that were posted as separate posts were excluded, resulting in a final dataset of 148 posts.

The dataset `relationship_advice_data.csv` contains the following data:
1. **title**, a string
2. **body**, a string
3. **gender**, a string in the set ('m', 'f')
4. **age**, an integer
5. **url**, the url linking to the original post

In the r/relationship_advice subreddit, users self-report their age and gender, typically using the following format:
> I/my/me ([age][M/F])

Examples of declarations include: 'I (42M) broke up with...', 'my [27F] preference of...' or '...ignored me (35M)'

A regular expression (regex) was thus used to capture the age and gender data. However, as users may not have followed the typical format in reporting their age and gender, the data may not have been captured by the regex. Thus, the dataset **needs to undergo further manual classification**.

The corpus `relationship_advice_corpus.txt` contains the title and body of each post included in the dataset encoded in the UTF-8 format. 
