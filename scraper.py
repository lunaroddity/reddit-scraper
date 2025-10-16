from dotenv import load_dotenv
import os
import praw
import pandas as pd

load_dotenv()

# initialise reddit instance
reddit = praw.Reddit(
  client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
  client_id=os.getenv("REDDIT_CLIENT_ID"),
  user_agent=os.getenv("REDDIT_USER_AGENT")
)

aita = reddit.subreddit("AmItheAsshole")

# scrape data from subreddit of top 200 posts of all time
# for each post, scrape the text and the verdict (using the flair)
data = []
valid_flairs = ["Asshole", "Not the A-hole", "Everyone Sucks", "No A-holes Here"]

for submission in aita.top(limit=10):
    # include only submissions with the verdict flairs, UPDATE posts excluded
    # so as to maximise the number of unique authors
    # TODO: may not be 200 posts exactly since META and UPDATE posts excluded
    if submission.link_flair_text in valid_flairs:
      id = submission.id
      title = submission.title
      text = submission.selftext
      verdict = submission.link_flair_text
      url = submission.url

    # from the text, identify the age and gender of the author using regex

    # if not found, set to None (to be determined manually later)

    # data.append([id, title, text, gender, age, verdict, url])
    data.append([id, title, text, verdict, url])

# create a dataframe from the data
df = pd.DataFrame(data, columns=["id", "title", "text", "verdict", "url"])

# output separate files for each type of post
# csv with all the data
df.to_csv("aita_data.csv", index=False)

# txt file with utf-8 encoding for corpus creation
with open("aita_corpus.txt", "w", encoding="utf-8") as f:
  full_text = df.to_string(columns=["title", "text"], header=False, index=False, encoding="utf-8")
  f.write(full_text)