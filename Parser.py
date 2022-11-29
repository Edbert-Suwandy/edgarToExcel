from bs4 import BeautifulSoup # actually the most beautiful things in the world
import re
from openpyxl import Workbook

def formatText(soup):
    """Format Text
    
    remove all the <C> and </C> chain except for the last one and remove all element which is empty from the soup (bs4 data type)
    and return a list which contains all the rows in the table (unseperated)

    Params:
        soup (bs4 datatype) : the soup to be parsed
    Return:
        text (list)         : A list of rows with content (unseperated)
    """
    cLong = soup.find_all("c") # Remove all the <C> </C> chain except the last one
    i = 0
    end = cLong.__len__()
    while(i < end): 
        soup = soup.find("c")
        i+=1
    
    text = soup.prettify()

    text = text.split("\n") # turn it into an array

    # remove the useless <C> and </C>
    text.pop(0)
    text.pop(-1)
    
    for i, element in enumerate(text):
        element = str(element)
        if(re.findall("[a-zA-Z]",element) == []): # remove all element that have no text
            while(text.count(element) != 0):
                text.remove(element)
        if(element.startswith("TOTAL REPORT")):
            text.remove(element)
    return text

def parseOldTextFileFormat(soup):
    """Parse Old Text File Format
    
    Parse the soup (bs4 datatype) into a 2d list of rows and each row is parsed for Company name, title of class ect

    Params:
        soup (bs4 data type)    : The soup to be parsed
    Return:
        table (2d list)         : A 2d list containing rows, where each rows is parsed for Issuer, Title Of Class, CUISP, Value, PRN/AMT, PRN, Discreatin ,and Sole
    """
    array = soup.find("table")
    content = formatText(array)
    table = []
    for element in content:
        fullRow = element.split("\t")
        row = []
        for element in fullRow:
            pattern = re.compile(r"^([a-zA-Z0-9&();.\- ]*?)\s[[^\s{1,}]+([a-zA-Z0-9%/*.$ ]*?)\s*?([a-zA-Z0-9]{9})\s*?([0-9,]{1,})\s*?([0-9,]{1,})\s*?(SH|SHRS|PRN|PUT|CALL)\s*?(CALL|PUT|)\s*?(SOLE)\s*?[a-zA-z/\s]*?([0-9,]{1,}|N/A)(\s*?([0-9])){0,}")
            matches = pattern.finditer(element) 
            for match in matches:
                for index in range(0,10):
                    row.append(match.group(index))
        table.append(row)
    return table

def parseNewTextFileFormat(soup):
    """Parse New Text File Format
    
    Parse the soup (bs4 datatype) into a 2d list of rows and each row is parsed for Company name, title of class ect

    Params:
        soup (bs4 data type)    : The soup to be parsed
    Return:
        table (2d list)         : A 2d list containing rows, where each rows is parsed for Issuer, Title Of Class, CUISP, Value, PRN/AMT, PRN, Discreatin ,and Sole
    """
    issuerList = soup.find_all("nameofissuer")
    titleOfClassList = soup.find_all("titleofclass")
    cuispList = soup.find_all("cusip")
    valueList = soup.find_all("value")
    prnAmtList = soup.find_all("sshprnamt")
    prnList = soup.find_all("sshprnamttype")
    discretionList = soup.find_all("investmentdiscretion")
    soleList = soup.find_all("sole")

    toParse = [issuerList,titleOfClassList,cuispList,valueList,prnAmtList,prnList,discretionList,soleList]
    
    table = []

    for count, entries in enumerate(toParse[0]):
        row = []
        for element in toParse:
            row.append(element[count].text)
        table.append(row)
    
    return table

def isOldTextFormat(soup):
    """Is Old Text Format

    Check if the given soup is formated in the old sec style of text file

    Params:
        soup (bs4 datatype) : The soup to be check
    Return:
        True if soup is in old sec text file format
        False if soup is in new sec text file format
    """
    table = soup.find("table")
    if(table != None):
        return True
    else:
        return False;

