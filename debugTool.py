import main
from bs4 import BeautifulSoup # actually the most beautiful things in the world
import time
import re
from openpyxl import Workbook
import req

def getLinkOfTitle(titleToSeach):
    cik = "0001061768"
    allLink = req.getNumber(cik)
    for link in allLink:  #Get all of the text file
        textFile = req.getTextFile(link)
        soup = BeautifulSoup(textFile.content,features="html.parser")
        title = req.getFillingDate(soup)
        if(title == titleToSeach):    
            temp = str(title).split("-")
            noDashIndex = ""
            for item in temp:
                noDashIndex+=item
            URL = "https://www.sec.gov/Archives/edgar/data/1061768/{fileNumberNoDash}/{fileNumber}.txt".format(fileNumberNoDash = noDashIndex,fileNumber = title)
            print(URL)
            break

def test(): # debugger
    cik = "0001061768"
    allLink = req.getNumber(cik)
    for link in allLink:  #Get all of the text file
        textFile = req.getTextFile(link)
        soup = BeautifulSoup(textFile.content,features="html.parser")
        title = req.getDate(soup)
        soup = soup.find("table")
        if(title == "30-09-2003"):
            if(soup != None):
                content = main.formatText(soup)
                for entry in content:
                    print(entry)

