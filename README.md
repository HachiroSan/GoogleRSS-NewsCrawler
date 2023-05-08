# GoogleRSS-NewsCrawler
GoogleRSS-NewsCrawler is a Python tool that enables you to scrape news articles from Google RSS feeds. With this tool, you can extract and store relevant data from various news sources such as the article's title, publisher, publication date, URL, content, and keywords. We also use natural language processing techniques to extract relevant information from the text, such as digits with context. The tool then exports the extracted data to a CSV file, making it easy for you to use and analyze the data.

To use the GoogleRSS-NewsCrawler, install the requirements.txt and run the scrape.py script with the following command-line arguments:

    python scrape.py [keyword] [limit]

Usage :-

* [keyword]: The keyword to search for news articles.
* [limit] (optional): Set limit news. Default will scrape all of the news available.

The tool will then extract relevant information from the RSS feeds, perform natural language processing on the articles' text, and export the data to a CSV file named data.csv.

To use the exported data, simply open the news.csv file in a spreadsheet program such as Microsoft Excel or Google Sheets.
