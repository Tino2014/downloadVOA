#coding=utf-8
import urllib
import re
import os.path
from bs4 import BeautifulSoup


'''
Created on Jun 3, 2016

@author: zqlu
'''

def getHtml(url):
    page = urllib.urlopen(url)
    html= page.read()
    return html

def getMp3(html):
    '''
    exreg = r'a id=\"mp3\" href=\"(.+\.mp3)\"'
    mp3 = re.compile(exreg)
    mp3list = re.findall(mp3,html)
    '''
    mp3list = []
    soup = BeautifulSoup(html,'lxml')
    for i in soup.find_all('a',id='mp3'):
        mp3list.append(i.attrs["href"])
    return mp3list


def saveData(url):
    
    html = getHtml(url)
    soup = BeautifulSoup(html,'lxml')
    mp3list = getMp3(html)
    for mp3url in mp3list:
        # save as mp3name
        mp3name = mp3url.split('/')[-1]
        # save txt file
        txtname = mp3name + ".txt"
        if (os.path.exists(mp3name)):
            print "%s already exist, skip downloading..." % mp3name
        else:
            print "downloading %s..." % mp3name
            urllib.urlretrieve(mp3url, mp3name)
            print "downloading done..."
            
            if (os.path.exists(txtname)):
                print "%s already exist, skip writing..." % txtname
            else:
                print "saving the txt file..."
                fileObject = open(txtname,'w')
                for p in soup.findAll("p"):
                    fileObject.write(p.getText().encode("utf-8") )
                    #print type(p.getText())
                fileObject.close()
                print "saving the txt file done..."
                

def getAll(src):
    res = []
    html = getHtml(src)
    #print html
    soup = BeautifulSoup(html,'lxml')
    
    #print len(soup.find_all("a"))
    for i in soup.find_all("a"):
        #print i
        if i.find_parent('div',id="list") == None:
            continue
        else:
            content = i.attrs
            href = content["href"]
            href = '/'.join(src.split('/')[:-1]) + href
            res.append(href)
            print href
            
    if len(res) >= 20:
        #  if the mp3 number is larger than 20, then we just download 20 mp3s.
        res = res[:20]
    
    return res
    """
    print len(soup.find_all("div",id="list"))
    divtag = soup.find_all("div",id="list")[0]
    for child in divtag.children:
        print child
    """ 
    

        
        
        
        
    

#print html
if __name__ == '__main__':
    """
    src = "http://www.51voa.com/VOA_Special_English/clinton-calls-trump-unfit-to-lead-foreign-policy-69904.html"
    html = getHtml(src)
    mp3list = getMp3(html)
    saveData(mp3list, src)
    print mp3list
    """
    src = "http://www.51voa.com/VOA_Standard_1.html"
    urls = getAll(src)
    for url in urls:
        saveData(url)
    pass