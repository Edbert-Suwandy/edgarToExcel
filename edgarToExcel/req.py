import requests
from bs4 import BeautifulSoup # actually the most beautiful things in the world
import time
import re

def req(URL):
    header = {'User-Agent': 'edbertat@gmail.com',"Accept-Encoding": "gzip","Host":"www.sec.gov"}
    data = requests.get(URL,headers=header)
    return [data.status_code,data]

def getNumber(cikNumber):
    """Get File Number

    Params:
        cikNumber (int)         : The cik number for the company in question with the leading zeros
    Return
        allLinks (list of int)  : A list of file number
    """
    URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13f&dateb=&owner=include&count=100&search_text=".format(cik = cikNumber)
    page = req(URL)[1]

    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find(id="seriesDiv")
    allA = soup.find_all('a')

    allLinks = []
    
    for href in allA:
        href = str(href).split('"')[1]
        if href.startswith("/Archives"):
            temp = href.split('/')[-1]
            temp = temp.split("-")
            temp.pop(-1)
            fileNum = ""
            i = 0
            while(i < temp.__len__()-1):
                fileNum+=temp[i]
                fileNum+="-"
                i+=1
            fileNum+=temp[temp.__len__()-1]

            
            # print(fileNum) #DEBUGGING PRINT

            allLinks.append(fileNum)
    
    return allLinks

def getTextFile(fileIndex):
    start = time.time_ns()

    temp = str(fileIndex).split("-")
    noDashIndex = ""
    for item in temp:
        noDashIndex+=item

    URL = "https://www.sec.gov/Archives/edgar/data/1061768/{fileNumberNoDash}/{fileNumber}.txt".format(fileNumberNoDash = noDashIndex,fileNumber = fileIndex)
    textFile = req(URL)[1]

    end = time.time_ns()
    if(end-start > 100):
        return textFile
    else:
        time.sleep(0.1-(end-start))
        return textFile


def getDate(soup):
    """Get Date

    Params:
        Soup (bs4 soup datatype)        : The soup to be parsed
    Return:
        The filling date (String)       : A string formated as (DD-MM-YYYY)
    """
    header = soup.find("acceptance-datetime")

    pattern = re.compile("FILED AS OF DATE:\t*?([0-9]{8})")

    matches = re.finditer(pattern,str(header))
    
    for match in matches:
        time = match.group(1)

    time = list(time)
    if(time.__len__() < 7):
        DAY = str(time[6])
    else:
        DAY = str(time[6]+time[7])

    MONTH = str(time[4]+time[5])
    YEAR = str(time[0]+time[1]+time[2]+time[3])
    time = str(DAY+"-"+MONTH+"-"+YEAR)
    return time

