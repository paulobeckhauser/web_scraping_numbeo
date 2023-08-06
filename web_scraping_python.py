from bs4 import BeautifulSoup
import requests
import pandas as pd

class webScraping:

    def __init__(self) -> None:
        self.DataDict = dict()
        self.DataDict["CountryName"] = list()

    def getCountryNameList(self, countryURL = "https://www.numbeo.com/cost-of-living/"):

        res = requests.get(countryURL).text
        soup = BeautifulSoup(res, "html.parser")

        countrylist = list()

        for a in soup.find_all('a', href = True):
            if 'country_result' in a['href']:
                countrylist.append(a["href"].split("=")[1])

        return countrylist
    
    def CountryNameOperation(self, countryName):

        countryName = countryName.replace("%28", "(")
        countryName = countryName.replace("%29", "(")
        countryName = countryName.replace("+", " ")
        
        return countryName

    def getCountriesCostOfLiving(self, countryURL, countryName):

        self.DataDict["CountryName"].append(countryName)
        res = requests.get(countryURL).text
        soup = BeautifulSoup(res, "html.parser")
        table = soup.find("table", class_ = "data_wide_table")
        for row in table.find_all("tr"):
            column = row.find_all("td")
            if column != []:
                name = column[0].text.strip()
                price = column[1].text.strip()

                if name not in [i for i in self.DataDict.keys()]:
                    self.DataDict[name] = list()
                    self.DataDict[name].append(price)

                else:
                    self.DataDict[name].append(price)

    def dataMerge(self):

        #countryList = self.getCountryNameList()
        countryList = ['Brazil', 'Germany', 'Switzerland', 'United States']
        counter = 1
        for countryName in countryList:
            countryName = self.CountryNameOperation(countryName)
            url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country={}&displayCurrency=USD".format(countryName)
            self.getCountriesCostOfLiving(url, countryName)
            
            counter += 1

        return self.DataDict
    

    def getDataFrame(self):
        dataDict = self.DataDict
        counterDict = dict()
        
        for i in dataDict:
            if str(len(dataDict[i])) not in [ky for ky in counterDict.keys()]:

                counterDict[str(len(dataDict[i]))] = 1
            else:
                counterDict[str(len(dataDict[i]))] += 1

        maxValue = max(counterDict, key = counterDict.get)

        lastDict = dict()
        for i in dataDict:
            if len(dataDict[i]) == int(maxValue):
                lastDict[i] = dataDict[i]

        return pd.DataFrame(lastDict)
    
WS = webScraping()

WS.dataMerge()

data = WS.getDataFrame()

data.to_csv('cost.csv', index=False)