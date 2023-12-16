# DISCLAIMER
# This application is provided "as is" without warranty of any kind, either express or implied,
# including, but not limited to, the implied warranties of merchantability and fitness for a
# particular purpose. The entire risk as to the quality and performance of the application is
# with you. Should the application prove defective, you assume the cost of all necessary
# servicing, repair or correction.

# CREDITS
# This application was developed by M. Farhad.
# M. Farhad is solely responsible for the development and maintenance of this application.
# M. Farhad  is not responsible for any issues, problems or damages that may arise from the
# use of this application.
# All the libraries used is solely owned by their respective owners. M. Farhad does not
# claim ownership of any of the libraries used in this application.


import sys
from gnews import GNews
from newspaper import Article
import os
import pandas as pd
import spacy
from spacy.util import is_package
import nltk

# Check if the Spacy model is installed
if not is_package("en_core_web_sm"):
    spacy.cli.download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

# Check if the NLTK punkt tokenizer is installed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_digits(corpus):
    # Extract digits from a corpus with context using Spacy NLP
    result = {}

    doc = nlp(corpus)

    for token in doc:
        if token.like_num:
            try:
                digit = float(token.text)
                context = token.sent.text
                result[digit] = context
            except ValueError:
                pass

    return result


def crawl_news(keyword, limit):
    google_news = GNews()

    # CONFIGURE THE GOOGLE NEWS PARAMETERS
    # --------------------------------
    google_news.max_results = limit  # number of responses across a keyword
    # google_news.period = "7d"  # News from last 7 days
    # google_news.country = "Malaysia"  # News from a specific country
    # google_news.language = "english"  # News in a specific language
    # google_news.exclude_websites = ["yahoo.com"] # Exclude news from specific website i.e Yahoo.com and CNN.com
    # google_news.start_date = (2020, 1, 1)  # Search from 1st Jan 2020
    # google_news.end_date = (2020, 3, 1)  # Search until 1st March 2020

    News = google_news.get_news(keyword)

    if not News:
        print("Nothing to scrape here :(. Try another keyword.")
    else:
        # Send a GET request to the URL
        for i, web in enumerate(News):
            print(f"Scraping: {web['title']}")
            print(
                f"Publisher: {web['publisher']}\n"
                f"Published Date: {web['published date']}\n"
                f"URL: {web['url']}\n\n"
            )
            try:
                article = Article(web["url"])
                article.download()
                article.parse()
                article.nlp()
                web["content"] = article.text
                web["keywords"] = article.keywords
                web["digit_context_pairs"] = extract_digits(article.text)
                web["summary"] = article.summary
            except Exception as e:
                print(f"Error parsing article: {e}")
                web["content"] = ""
                web["keywords"] = []
                web["digit_context_pairs"] = {}
                web["summary"] = ""

            News[i] = web

        try:
            # create a dataframe
            df = pd.DataFrame(News)

            # export the dataframe to a CSV file
            df.to_csv("data.csv", index=False)

            # print success message
            print("CSV file 'data.csv' exported successfully!")
        except Exception as e:
            # print error message
            print(f"Error exporting to CSV file: {e}")


if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python main.py [keyword] [limit]")
        sys.exit(1)

    # Get the arguments from sys.argv
    keyword = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) == 3 else 5

    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")

    # Call the CrawlNews function with the provided arguments
    news = crawl_news(keyword, limit)
