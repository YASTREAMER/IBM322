from bs4 import BeautifulSoup
import urllib.request
import os
import requests

import spacy
nlp =spacy.load("en_core_web_sm")

from spacy.lang.en.stop_words import STOP_WORDS



def RemovalText(RemovalFile):
    #open the text file  
    with open('removal.txt', 'r') as f: 
        #read the text file into a list of lines 
        lines = f.readlines() 
        
    #create an empty dictionary 
    file_dict = []
        
        #loop through the lines in the text file  
    for line in lines: 
        line=line.replace("\n","")
        file_dict.append(line)

    FileDict=file_dict

    return(file_dict)


def DataExtration(URL_ID,UrlAddress,file_dict):


    #This function is used to extract the data from the articles

    URL_str=os.path.join("/home/yash/Intership/BlackCoffer/ArticleData/",str(URL_ID))
    URL_str=str(URL_str)+".txt"
    try:
        # urllib.request.urlretrieve(UrlAddress,"HtmlTemp.txt")
        response = requests.get(UrlAddress).text
    except:
        print("Error 404 "+UrlAddress)

    # file = open("HtmlTemp.txt", "r")
    # contents = file.read()
    
    soup = BeautifulSoup(response, 'html.parser')

    title = soup.title.string

    f = open(URL_str, "w")

    f.writelines(title+"\n")

    for data in soup.find_all("p"):
        sum = data.get_text()

        #Removal of unwanted data
        for element in file_dict:
            if sum == element:
                IsTrue=True
                break
            else:
                IsTrue=False

        if IsTrue:
            continue
        else:
            f.writelines(sum+"\n")

    for data in soup.find_all("ol"):
        sum = data.get_text()

        #Removal of unwanted data
        for element in file_dict:
            if sum == element:
                IsTrue=True
                break
            else:
                IsTrue=False

        if IsTrue:
            continue
        else:
            f.writelines(sum+"\n")
 
    f.close()

    return(URL_str)


def StopWordRemoval(NameFile,Url):

    String=""
    Url=os.path.join("/home/yash/Intership/BlackCoffer/ArticleData/ProcessedData/",str(Url)+".txt")
    f=open(Url,"w")
    file = open(NameFile,"r")

    for line in file:
        String=""
        doc=nlp(line)
        for token in doc:
            if not token.is_stop and not token.is_punct:
                String=String+" "+str(token)
        f.writelines(String+"\n")


    return(Url)
    