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
# for each post, scrape the text and the verdict (using the flair)
for submission in relationship_advice.top(limit=300):
  # include only submissions with the verdict flairs, UPDATE posts excluded as they do not involve framing of moral judgement
  is_update = re.match(r'(?:.*)update(?:.*)', submission.title, re.IGNORECASE)

  if not is_update:
    title = submission.title
    text = submission.selftext
    url = submission.url

  # from the text, identify the age and gender of the author using regex
    age = None
    gender = None
    age_gender = None

    # look for age and gender in the title following first-person singular pronouns 'i', 'my' or 'me'
    # regex matches patterns like "I (25M)" or "my [f30]"
    AGE_GENDER_RE = re.compile(
      r'(?:i|my|me)(?:\s*)(?:\(|\[)'
      r'(?P<gender1>[mf]*)(?:[^mf0-9])*(?P<age>\d{1,3})(?:[^mf0-9])*(?P<gender2>[mf]*)'
      r'(?:(\)|\]))',
      re.IGNORECASE
    )

    # only search text if not found in title 
    age_gender = AGE_GENDER_RE.search(title)
    if age_gender is None:
      age_gender = AGE_GENDER_RE.search(text)
 
    if age_gender:
      age_str = age_gender.group('age')
      gender_str = age_gender.group('gender1') or age_gender.group('gender2')

      if age_str:
        age = int(age_str)
      
      if gender_str:
        gender = gender_str.lower()

    data.append([title, text, gender, age, url])

# create a dataframe from the data
df = pd.DataFrame(data, columns=["title", "text", "gender", "age", "url"])

# convert the dataframe into a sql table to allow for custom queries to generate various corpuses later
# engine = create_engine("sqlite://", echo=True)
# df.to_sql("relationship_advice_posts", engine, if_exists="replace", index=False)

# output separate files for each type of post
# csv with all the data
df.to_csv("relationship_advice_data.csv", index=False)

# txt file with utf-8 encoding for corpus creation
with open("relationship_advice_corpus.txt", "w", encoding="utf-8") as f:
  full_text = df[['title', 'text']].apply(lambda x: '\n'.join(x), axis=1).str.cat(sep='\n\n\n\n')
  f.write(full_text)