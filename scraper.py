from dotenv import load_dotenv
import os
import re
import praw
import pandas as pd
# from sqlachemy import create_engine

load_dotenv()

# initialise reddit instance
reddit = praw.Reddit(
  client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
  client_id=os.getenv("REDDIT_CLIENT_ID"),
  user_agent=os.getenv("REDDIT_USER_AGENT")
)

data = []
relationship_advice = reddit.subreddit("relationship_advice")

# scrape data from subreddit of top 300 posts of all time
# for each post, scrape the necessary data
for submission in relationship_advice.top(limit=300):
  # update posts excluded as they do not involve framing of moral judgement
  is_update = re.match(r'(?:.*)update(?:.*)', submission.title, re.IGNORECASE)

  if not is_update:
    title = submission.title
    body = submission.selftext
    url = submission.url

  # identify the age and gender of the author using regex
    age = None
    gender = None
    age_gender = None

    # author's self-reported age and gender typically follows the first-person singular pronouns 'i', 'my' or 'me'
    # regex matches patterns like "I (25M)" or "my [f30]" or "me (m22)" etc.
    AGE_GENDER_RE = re.compile(
      r'(?:i|my|me)(?:\s*)(?:\(|\[)'
      r'(?P<gender1>[mf]*)(?:[^mf0-9])*(?P<age>\d{1,3})(?:[^mf0-9])*(?P<gender2>[mf]*)'
      r'(?:(\)|\]))',
      re.IGNORECASE
    )

    # only search body for author's age and gender if not found in title 
    age_gender = AGE_GENDER_RE.search(title)
    if age_gender is None:
      age_gender = AGE_GENDER_RE.search(body)
 
    # if age and/or gender reported in the typical format, extract them 
    if age_gender:
      age_str = age_gender.group('age')
      gender_str = age_gender.group('gender1') or age_gender.group('gender2')

      if age_str:
        age = int(age_str)
      
      if gender_str:
        gender = gender_str.lower()

    # data still needs to be manually classified as some authors may not report their age or gender in the typical format
    data.append([title, body, gender, age, url])

# create a dataframe from the data
df = pd.DataFrame(data, columns=["title", "body", "gender", "age", "url"])

# output the following files:
# csv with all data collected
df.to_csv("relationship_advice_data.csv", index=False)

# txt file encoded in the utf-8 format for the creation of a corpus
with open("relationship_advice_corpus.txt", "w", encoding="utf-8") as f:
  full_text = df[['title', 'body']].apply(lambda x: '\n'.join(x), axis=1).str.cat(sep='\n\n\n\n')
  f.write(full_text)

# possible extension: convert the dataframe into a sql table to allow for custom queries
# about author's age or gender to generate various filtered corpuses later, need to exclude null values first 
# engine = create_engine("sqlite://", echo=True)
# df.to_sql("relationship_advice_posts", engine, if_exists="replace", index=False)