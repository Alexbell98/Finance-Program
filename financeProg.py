import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json
from pandas_datareader import data as wb
from datetime import date
from bs4 import BeautifulSoup as soup

file = pd.read_csv(r'C:\Users\alexa\OneDrive\Documents\Data Science\Stocks.csv')

file = file.replace(np.nan, '')

length = len(file['Stocks'])

Stockfile = file['Stocks']

StockNew = []

CryptoNew = []

First = file['FirstName']
Last = file['LastName']
Email = file['Email']
Crypto = file['Crypto']

today = date.today()

for n in range(length):
    Stocks = Stockfile[n].split(',')
    StockNew.append(Stocks)
    Cryptos = Crypto[n].split(',')
    CryptoNew.append(Cryptos)
    

for n in range(len(StockNew)):
    length = len(StockNew[n])
    for entry in range(length):
        if StockNew[n][entry] == " ":
            del StockNew[n][entry]

for n in range(len(CryptoNew)):      
    length = len(CryptoNew[n])
    for entry in range(length):
        if CryptoNew[n][entry] == " ":
            del CryptoNew[n][entry]

for n in range(len(StockNew)):
    length = StockNew[n]
    for each in range(len(length)):
        StockNew[n][each] = StockNew[n][each].replace(" ", "")

for n in range(len(CryptoNew)):
    length = CryptoNew[n]
    for each in range(len(length)):
        CryptoNew[n][each] = CryptoNew[n][each].replace(" ", "")
    

def find_stock_symbol(query):
    url = "http://d.yimg.com/aq/autoc?query=" + query + "&region=US&lang=en-US"

    with urlopen(url) as url:
        url_data = json.loads(url.read().decode())
        stock_symbol = url_data['ResultSet']['Result'][0]['symbol']

    return stock_symbol
    

class User:

    ID = 0

    def __init__(self, First, Last, Email, Stocks, Crypto):
        self.FirstName = First
        self.LastName = Last
        self.Email = Email
        self.Portfolio = Stocks
        self.Crypto = Crypto
        self.ID += 1
        self.Tickers = {}
        self.Opening = {}
        self.Days = {}
        self.Initial = {}
        self.Current = {}
        
        

    def findTicker(self):
        Stocks = self.Portfolio

        Crypto = self.Crypto

        StockTick = []

        CryptoTick = []

        new = []

        for n in Stocks:
            Ticks = find_stock_symbol(n)
            self.Tickers[n] = Ticks
            StockTick.append(Ticks)

        for n in Crypto:
            fauxDict = {}
            Cry = n.lower()
            url = "https://coinmarketcap.com/currencies/" + Cry + "/"
            uopen = urlopen(url)
            page = uopen.read()
            uopen.close()
            pagesoup = soup(page, "html.parser")
            rawtext = pagesoup.findAll("script", {"type":"application/ld+json"})
            rawtext = rawtext[0].prettify()
            start = rawtext[0:38]
            end = rawtext[-13:]
            polished = rawtext.replace(start, '')
            polished = polished.replace(end, '')
            Polished = polished.split(',')
            length = len(Polished)
            for pol in range(length):
                alle = Polished[pol].split(':')
                if len(alle) == 3:
                    alk = alle[1] + alle[2]
                    new.append([alle[0], alk])
                else:
                    new.append([alle[0], alle[1]])
        
                    
            for el in range(len(new)):
                key = new[el][0][1:-1]
                value = new[el][1][1:-1]
                fauxDict[key] = value

            PreTicker = fauxDict.get("currency")

            GBP = "-GBP"

            PostTicker = PreTicker + GBP

            CryptoTick.append(PostTicker)

            self.Tickers[n] = PostTicker
        
        finalTicks = StockTick + CryptoTick    
    

    def GetData(self):
        Tickers = self.Tickers

        for key, values in Tickers.items():
            data = wb.DataReader(values, data_source = 'yahoo', start = '2021-02-05', end = today)['Adj Close']
            length = len(data)
            self.Opening[key] = data[0]
            Days = []
            for n in range(1,length):
                Days.append(data[n])
            self.Days[key] = Days

    def SetInitial(self):
         
        length = len(self.Days.keys())
        keys = self.Days.keys()
        Sum = 0

        while True:
            try:
                AccountTotal = float(input("How much is the whole portfolio worth? (£GBP) : "))
                break
            except ValueError:
                print("This is not a valid input")

        while Sum != AccountTotal:
            Money = []
            Counter = 0
            for n in keys:
                self.Initial[n] = float(input("How much do you want to invest in " + n + " (GBP):"))
                Money.append(self.Initial[n])
                Counter += 1
                Summary = sum(Money)
                print("Remaining Value is:", (AccountTotal - Summary), "\nAmount of Stocks left to Appropriate:", (length - Counter))

            Sum = sum(self.Initial.values())

            if Sum == AccountTotal:
                print("Thank you for appropriating funds")

            else:
                print("Appropriations were not made as needed")

             
            

    def Formulas(self):
        Current = self.Initial

        Stocks = self.Days

        for key, values in Stocks.items():
            Curr = Current[key]
            values = np.array(values)
            length = len(values)
            for n in range(length):
                if n < (length - 1):
                    Curr = Curr * (values[n+1]/ values[n])
            self.Current[key] = Curr

    def ShowTotal(self):
        Earnings = self.Current.values()
        Initial = sum(self.Initial.values())

        Total = round(sum(Earnings), 2)

        Per = round(((Total -Initial)/Initial),2)*100

        if Total - Initial > 0:
            Name = "Increase"
        else:
            Name = "Decrease"   

        account = print("Hello,", self.FirstName,"The total amount of the portfolio is", Total, "\n The Net Percentage of Portfolio is", Per, Name)

        return account
                 

    def Account(self):
        Keys = []
        Values = []
        Initial = []
        Final = []
        Prof = []
        for n in self.Initial.items():
            key, values = n[0], n[1]
            Keys.append(key)
            Initial.append(values)

        for n in self.Current.values():
            Final.append(n)

        for n in range(len(Keys)):
            Init = Initial[n]
            Current = Final[n]
            Net = ((Current - Init)/Init) * 100
            Net = round(Net, 2)
            Values.append(Net)
            ProfLoss = Current - Init
            Prof.append(ProfLoss)
            


        Dataf = {"Stocks" : Keys, "Open Value": Initial, "Current": Final, "Net(%)": Values, "Profit(£}": Prof}
        Data = pd.DataFrame(Dataf)

        print(Data)
            
        
        


alex = User(First[0], Last[0], Email[0], StockNew[0], CryptoNew[0])

alex.findTicker()
alex.GetData()
alex.SetInitial()
alex.Formulas()
alex.ShowTotal()
alex.Account()





            


            
            
    
