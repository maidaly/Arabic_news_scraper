#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 19:27:41 2018

@author: mai
"""
"""
    This script for scraping the most 3 visited  news websites in Egypt  
    (youm7.com, almasryalyoum.com, shorouknews.com) to get tech ,
    sport, political news titles and the summary if available. 
    it displays the news based on the arguments  passed to it.
    Usage:
        
        - the main arguments are news-site and news-type
        
        >>>python news-scraper.py <news-site> <news-type> 
        
         - the optional arguments are -sv to save the data 
           and -wc to show news wordcloud:
            
        >>>>python news-scraper.py <news-site> <news-type> -wc <yes> -save <yes>
            
    Examples:
        - to get the sport news from youm7.com without showing wordcloud
        
        >>>python news-scraper.py ym s  
        
        in this example we used ym as argument for youm7 it can also accept 
        ("ym","yom","ym7","y7","youm7","youm","y") as arguments for youm7
        "s" means that the news-type is sport and for tech-news we will use
        "t" and for political-news we will use "p". 
        
        - to get the political news from almasryalyoum.com and show wordcloud
        
        >>>python news-scraper.py msr p -wc yes
        
        we used ym as argument for youm7 it can also accept 
        ("msr","msry","msry","m") as arguments for almasryalyoum.com.
        "p" means that the news-type is political-news."wc" means that 
        show wordcloud.
        
        - to get the tech news from shorouknews.com and show wordcloud
        
        >>>python news-scraper.py sh t -wc yes
        
        here, "sh" is argument for shorouknews .it can also accept 
        ("sh","shrok","shrk","shourk","shr") as arguments for 
        shorouknews. "t" for tech-news.
        
        - to get the sport news from the 3 websites
        
        >>>python news-scraper.py all s
        
        "all" is argument for getting news from the 3 websites
        
        note:
            - if the passed arguments have syntax error, the script will
            return blank or nothing. So, Make sure that you passed the right 
            syntax.
                    
"""
import os
import argparse
import requests
import numpy as np
import pandas as pd 
from PIL import Image
import arabic_reshaper
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bidi.algorithm import get_display

headers = {}
headers['User-Agent']= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

mask_file = "/home/mai/Pictures/egypt_mask.png"
mask = np.array(Image.open(mask_file))
       
class Youm7 ():

    def __init__(self, news_type = 't'):
        self.news_type = news_type
        self.urls = {
                "sport": "https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A8\
                 %D8%A7%D8%B1-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9/298/1",
                "tech": "https://www.youm7.com/Section/%D8%B9%D9%84%D9%88%D9%85\
                 -%D9%88-%D8%AA%D9%83%D9%86%D9%88%D9%84%D9%88%D8%AC%D9%8A%D8%A7/328/1",
                "political": "https://www.youm7.com/Section/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9/319/1",
                "instant": "https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B9%D8%A7%D8%AC%D9%84%D8%A9/65/1"
                    }

    def display(self, date, title, summary):
        print(date+"\n\n" + title + "\n\n" + "ملخص الخبر"
              + "\n\n" + summary + "\n")
        print("\n\n\t\t\t\t******************************************\t\t\t\t\n\n")

    def scrap(self, url):
        req = requests.get(url, headers = headers)
        if(req.status_code == requests.codes.OK):
            page = req.text
            soup = BeautifulSoup(page, "html.parser")
            news = soup.find_all("div", {"class", "col-xs-12 bigOneSec"})
            title = []
            summary = []
            date = []
            for item in news:
                _title = item.h3.a.text.strip()
                _summary = item.p.text.strip()
                _date = item.span.text.strip()
                title.append(_title)
                summary.append(_summary)
                date.append(_date)
                self.display(_date, _title, _summary)
            news_dict = {"title":title, "summary":summary, "date": date}
            return (news_dict)
        else:
            req.raise_for_status()

    def get_news(self):
        if self.news_type == 's':
            print("اخبار اليوم السابع - رياضة\n")
            return(self.scrap(self.urls['sport']))
        if self.news_type == 't':
            print("اخبار اليوم السابع - تكنولوجياو علوم\n")
            return(self.scrap(self.urls['tech']))
        if self.news_type == 'p':
            print("اخبار اليوم السابع - سياسة\n")
            return(self.scrap(self.urls['political']))
        if self.news_type == 'i':
            print("اخبار اليوم السابع - عاجلة\n")
            return(self.scrap(self.urls['instant']))


class MasryYoum():

    def __init__(self, news_type = "t"):
        self.news_type = news_type
        self.urls = {
                "sport": "https://www.almasryalyoum.com/section/index/8",
                "tech": "https://www.almasryalyoum.com/section/index/9",
                "political": "https://www.almasryalyoum.com/section/index/3",
                "instant": ""
                    }

    def display(self, date, title):
        print(date+"\n\n" + title + "\n")
        print("\n\n\t\t\t\t******************************************\t\t\t\t\n\n")

    def scrap(self, url):
        req = requests.get(url, headers = headers)
        if(req.status_code == requests.codes.OK):
            page = req.text
            soup = BeautifulSoup(page, "html.parser")
            news_block = soup.find_all("div", {"class", "last_news"})[0]
            news = news_block.find_all("li")
            title = []
            date = []
            for item in news:
                _title = item.find_all("p")[1].text.strip()
                _date = item.find_all("p")[0].text.strip()
                title.append(_title)
                date.append(_date)
                self.display(_date, _title)
            news_dict = {"title":title, "date": date}
            return (news_dict)
        else:
            req.raise_for_status()

    def get_news(self):
        if self.news_type == 's':
            print("اخبار المصرى اليوم - رياضة\n")
            return(self.scrap(self.urls['sport']))
        if self.news_type == 't':
            print("اخبار المصرى اليوم - تكنولوجيا\n")
            return(self.scrap(self.urls['tech']))
        if self.news_type == 'p':
            print("اخبار المصرى اليوم - سياسة\n")
            return(self.scrap(self.urls['political']))


class Shorouk():

    def __init__(self, news_type = "t"):
        self.news_type = news_type
        self.urls = {
                "sport": "https://www.shorouknews.com/sports",
                "tech": "https://www.shorouknews.com/variety/Internet-Comm",
                "political": "https://www.shorouknews.com/egypt",
                    }

    def display(self, date, title):
        print(date+"\n\n" + title + "\n")
        print("\n\n\t\t\t\t******************************************\t\t\t\t\n\n")

    def scrap(self, url):
        req = requests.get(url, headers = headers)
        if(req.status_code == requests.codes.OK):
            page = req.text
            soup = BeautifulSoup(page, "html.parser")
            news_block = soup.find_all("ul", {"class", "listing"})[0]
            news = news_block.find_all("li")
            title = []
            date = []
            for item in news:
                _title = item.find("div", {"class", "text"}).a.text.strip()
                _date = item.span.text.strip()
                title.append(_title)
                date.append(_date)
                self.display(_date, _title)
            news_dict = {"title":title, "date": date}
            return (news_dict)
        else:
            req.raise_for_status()

    def get_news(self):
        if self.news_type == 's':
            print("اخبار الشروق - رياضة\n")
            return(self.scrap(self.urls['sport']))
        if self.news_type == 't':
            print("اخبار الشروق - تكنولوجيا\n")
            return(self.scrap(self.urls['tech']))
        if self.news_type == 'p':
            print("اخبار الشروق - سياسة\n")
            return(self.scrap(self.urls['political']))
            

def generate_text(news_object):
    text = ""
    
    """this words droped to not be counted in wordcloud, as they are frequent
      words but we do not need them in wordcloud
      the anolgay words in english(in, out, between, today, company.....)"""
      
    droped_words = ("من","الى","إلى","قبل","عن","أن","فى","في","الفريق","فريق","على","خلال"
                        ,"علي","مع","بعد","بين","مثل","أمام","التى","شركة","اليوم","الذى","ذلك")                   
    dict_ = news_object.get_news()
    for index in range(len(dict_['title'])):
        title = dict_['title'][index]+" ."
        modefied_title = ' '.join([i for i in title.split() if i not in droped_words])
        text += modefied_title
        if "summary" in dict_.keys():
            summary = dict_['summary'][index]+" ."
            modefied_summary = ' '.join([i for i in summary.split() if i not in droped_words]) 
            text += modefied_summary
    return(text)
            
def generate_cloud(text):
#    text = generate_text(object_.get_news())
    reshaped_text = arabic_reshaper.reshape(text)
    artext = get_display(reshaped_text)
    wordcloud = WordCloud(width=1500, height=1200, 
                colormap="Blues", mask=mask,
                background_color="black").generate(artext)
    plt.rcParams.update({'font.size': 17})
    plt.figure(figsize=(7,7),facecolor = 'white', edgecolor='blue')
    plt.imshow(wordcloud, cmap=plt.cm.gray, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.title(r'$\mathcal{Egypt \ News \ WordCloud}$')
    plt.show() 

def save_data (news_object):
    from datetime import datetime
    now_ = datetime.now()
    dict_ = news_object.get_news()
    pd.DataFrame(dict_).to_csv("news_{0}-{1}-{2}-{3}-{4}".format(now_.year,
                              now_.month, now_.day, now_.hour, now_.minute)+".csv")
      
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("news_site", type=str, help="news-website")
    parser.add_argument("news_type", type=str, help="news-type")
    parser.add_argument("-wc", "--wordcloud", type=str, default="no",
                        help="showcloud")
    parser.add_argument("-sv", "--save", type=str, default="no",
                        help="save-csv-file")
    args = parser.parse_args()
    if(args.news_site in ("ym","yom","ym7","y7","youm7","youm","y")):
        youm7 = Youm7(args.news_type)
        if(args.wordcloud == "yes"):
            text = generate_text(youm7)
            generate_cloud(text)
        if(args.save == "yes"):
            text = save_data(youm7)
        if ((args.wordcloud == "no") & (args.save == "no")):
            youm7.get_news()
    if(args.news_site in ("msr","msry","msry","m")):
        masry_youm = MasryYoum(args.news_type)
        if(args.wordcloud == "yes"):
            text = generate_text(masry_youm)
            generate_cloud(text)
        if(args.save == "yes"):
            text = save_data(youm7)
        if (args.wordcloud == "no" & args.save == "no"):
            masry_youm.get_news()
    if(args.news_site in ("sh","shrok","shrk","shourk","shr")):
        shrouq = Shorouk(args.news_type)
        if(args.wordcloud=="yes"):
            text = generate_text(shrouq)
            generate_cloud(text)
        if(args.save == "yes"):
            text = save_data(shrouq)
        if (args.wordcloud == None & args.save == None):
            shrouq.get_news()
    if(args.news_site in("all_news", "all")):
        youm7 = Youm7(args.news_type)
        masry_youm = MasryYoum(args.news_type)
        shrouq = Shorouk(args.news_type)
        if(args.wordcloud == "yes"):
            text = ""
            for ob in (youm7, masry_youm, shrouq):
                text += generate_text(ob)
            generate_cloud (text)
        if (args.wordcloud == "no"):
            youm7.get_news()
            masry_youm.get_news()
            shrouq.get_news()

if __name__ == '__main__':
    main()


                
                
                
