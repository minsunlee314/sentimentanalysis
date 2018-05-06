from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
import time
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


def main():
    binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
    browser = webdriver.Firefox(executable_path='./geckodriver.exe', firefox_binary=binary)

    startdate = dt.date(year=2018, month=2, day=1)
    untildate = dt.date(year=2018, month=2, day=2)
    enddate = dt.date(year=2018, month=4, day=1)
    totalfreq = []
    while not enddate == startdate:
        url = 'https://twitter.com/search?q=Nubank%20since%3A' + str(startdate) + '%20until%3A' + str(
            untildate) + '&amp;amp;amp;amp;amp;amp;lang=eg'
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        lastHeight = browser.execute_script("return document.body.scrollHeight")

        while True:
            dailyfreq = {'Date': startdate}
            #     i=0 i는 페이지수
            wordfreq = 0
            tweets = soup.find_all("p", {"class": "TweetTextSize"})
            wordfreq += len(tweets)

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            newHeight = browser.execute_script("return document.body.scrollHeight")
            if newHeight != lastHeight:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                tweets = soup.find_all("p", {"class": "TweetTextSize"})
                wordfreq = len(tweets)
            else:
                dailyfreq['Frequency'] = wordfreq
                wordfreq = 0
                totalfreq.append(dailyfreq)
                startdate = untildate
                untildate += dt.timedelta(days=1)
                dailyfreq = {}
                break
            #         i+=1
            lastHeight = newHeight
    df = pd.DataFrame(totalfreq)
    for index, row in enumerate(df.iterrows()):
        date_str = row[1][0].strftime("%Y%m%d")
        df.set_value(index, 'Date', date_str)
    print(df)
    plt.figure(figsize=(20, 10))
    plt.xticks(rotation=90)
    # plt.plot(df['Date'], df['Frequency'])
    plt.scatter(df['Date'], df['Frequency'])
    plt.show()


if __name__ == "__main__":
    # calling main function
    main()
