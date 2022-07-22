# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 21:48:07 2021

@author: Alistair
"""

"""
Have deleted everything related to dling images (something to add future?)
write req.txt also say need to install pandoc

Requirements text
directory stuff
pip install lxml
pypandoc
bs4
letters page name
https://pypi.org/project/pandoc/
"""

import requests, pypandoc
from bs4 import BeautifulSoup
from sys import argv

def main():
    if len(argv) > 1:
        issue_url = argv[1]
    else:
        issue_url = None
    dl_issue = mag_dl(issue_url)
    dl_issue.worker()

class mag_dl():
    def __init__(self,issue_url=None):
        self.toc = []
        self.art_prefix = "https://lrb.co.uk"
        self.articles_str = ""
        self.issue_info = ""
        if issue_url is None:
            self.issueurl = self.latest_url()
        else:
            self.issueurl = issue_url

    def create_toc(self):
        tocdl = requests.get(self.issueurl)
        self.get_issue_info(tocdl.text)
        soup = BeautifulSoup(tocdl.text, 'lxml')
        toc = soup.find(class_="toc-grid-items")
        links = toc.find_all('a')
        for i in links:
            self.toc.append({"writer":i.h3.text,"works":i.h4.text,"link":i["href"]})
        

    def add_article(self, url, auth):
        articletxt = []
        
        art_text = requests.get(url)
        soup = BeautifulSoup(art_text.text, 'lxml')
            
        if soup.find('span', {'class' : 'title'}) != None:
            art_title = soup.find('span', {'class' : 'title'}).text
        elif soup.find('span', {'class' : 'kicker'}) != None:
            art_title = soup.find('span', {'class' : 'kicker'}).text
        else:
            art_title = "NA"

        print(art_title)
        arthead = "# " + auth + " - " + art_title
        articletxt.append(arthead)
        
        if soup.find_all(class_="article-reviewed-item") != None:
            books_rev = self.get_reviewed_books(art_text.text)
            articletxt.append(books_rev)
            
        article = soup.find(class_="article-copy")
        pars = article.find_all('p')

        for i in pars:
            articletxt.append(i.text)
            
        join_txt = "\n\n".join(articletxt)
        
        self.articles_str = self.articles_str + "\n\n" + join_txt
        
    def create_art_text(self):
        for art in self.toc:
            self.add_article(self.art_prefix+art['link'],art['writer'].strip())
            
    def generate_exargs(self):
        
        extra_args = []
        extra_args.append("--metadata=author:London Review of Books")
        extra_args.append("--metadata=title:"+self.issue_info)
        
        return extra_args
    
    def create_epub(self):
        filenm =  self.issue_info + ".epub"
        pypandoc.convert_text(self.articles_str,'epub', format='md',\
                               outputfile=filenm, extra_args=self.generate_exargs())
    
    def latest_url(self):
        homepage = requests.get("https://www.lrb.co.uk/")
        soup = BeautifulSoup(homepage.text, 'lxml')
        coverimg = soup.find(class_="in-this-issue-imagelink")
        return self.art_prefix + coverimg['href']
    
    def get_issue_info(self,issue_html):
        soup = BeautifulSoup(issue_html, 'lxml')
        issue_info = soup.find(class_="toc-title")
        issue_str = issue_info.text
        issue_str = issue_str.replace(" · "," ")
        issue_str = issue_str.replace(".","")

        self.issue_info = issue_str
        
    def get_reviewed_books(self,issue_html):
        soup = BeautifulSoup(issue_html, 'lxml')
        
        booklst = []
        
        books_rev = soup.find_all(class_="article-reviewed-item")
        for i in books_rev:
            bookstr = i.text
            bookstr_split = bookstr.split('.')
            booklst.append(bookstr_split[0])
        
        final_lst = "\n\n".join(booklst)
        
        return final_lst

    def worker(self):
        self.create_toc()
        self.create_art_text()
        self.create_epub()

if __name__ == '__main__':
    main()