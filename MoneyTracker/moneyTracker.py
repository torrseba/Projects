import os
import json
import time
import pyfiglet
import pandas as pd
import datetime as dt
#from openpyxl import load_workbook

#TODO manually add to blacklist
#TODO manually add transaction

MONTH = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
CATEGORIES = ["Free Money", "Payroll","VENMO","Services", "Merchandise","Restaurants","Supermarkets","TOTAL IN","Gasoline","TOTAL OUT","TOTAL", "Travel/ Entertainment"]

def updateBlacklist(section, param1, param2OPTIONAL):
    with open("blacklist.json", 'r+') as jsonfile:
        filedata = json.load(jsonfile)
        if section == "blacklist":
            filedata[section][len(filedata[section])] = param1
        else:
            filedata[section][param1] = param2OPTIONAL
        jsonfile.seek(0)
        json.dump(filedata, jsonfile, indent=4)

def addTransaction(dateMMDDYYYY, Category, Amount, Description):
    date = dateMMDDYYYY.split("/")
    with open(str(date[2]) + ".json", 'r+') as jsonfile:
        filedata = json.load(jsonfile)
        filedata[str(date[2])][MONTH[int(date[0])-1]][len(filedata[str(date[2])][MONTH[int(date[0])-1]])] = {"Category":Category, "Amount":Amount, "day":int(date[1]), "Description":Description}
        jsonfile.seek(0)
        json.dump(filedata, jsonfile, indent=4)
        time.sleep(.1)
        #print(filedata)
    updateExcel(filedata)

def updateExcel(data):
    #print(data)
    for year in data:


        with pd.ExcelWriter('DineroTracker.xlsx', engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
            if str(year) not in writer.book.sheetnames:
                print("Creating sheet for year: " + str(year))
                df_source = pd.read_excel(writer, sheet_name='Sheet1')
                df_source.rename(columns={2024: year}, inplace=True)
            else:
                print("Opening sheet for year: " + str(year))
                df_source = pd.read_excel(writer, sheet_name=str(year))
                        
            
            #print(df_source)
            df_source = df_source.set_index(int(year))
            #print(df_source)

            with open(str(year) + ".json", 'r+') as jsonfile:
                filedata = json.load(jsonfile)
                for month in data[year]:
                    if(len(data[year][month]) > 0):
                        for category in list(df_source.index)[:-3]:
                            df_source.loc[category, month] = 0.0
                        for transaction in filedata[str(year)][month]:
                            df_source.loc[filedata[str(year)][month][transaction]["Category"],month] += float(filedata[str(year)][month][transaction]["Amount"])


            df_source.to_excel(writer, sheet_name=str(year), index=True)


    print("Updated Excel:")
    print(df_source)



def saveDataToJSON(data):
    print("Saving to JSON...")
    for year in data:
        if (str(year) + ".json") in os.listdir(os.getcwd()):
            print("Appending data to existing file: " + str(year) + ".json")
            with open(str(year) + ".json", 'r+') as jsonfile:
                filedata = json.load(jsonfile)
                for month in data[year]:
                    for transaction in data[year][month]:
                        if data[year][month][transaction] not in filedata[str(year)][month].values():
                            print("transaction appended: " + str(data[year][month][transaction]))
                            filedata[str(year)][month][len(filedata[str(year)][month])] = data[year][month][transaction]
                jsonfile.seek(0)
                json.dump(filedata, jsonfile, indent=4)
        else:
            print("Creating file: " + str(year) + ".json")
            open(str(year) + ".json", 'a').close()
            with open(str(year) + ".json", 'r+') as jsonfile:
                infodump = {year:{}}
                infodump[year] = data[year]
                jsonfile.seek(0)
                json.dump(infodump, jsonfile, indent=4)


def discoverCard(file):
    data = {}
    discover = pd.read_csv('csv/' + file)
    for i in range(int(discover.loc[0]["Trans. Date"].split("/")[2]), int(discover.loc[len(discover)-1]["Trans. Date"].split("/")[2])+1):
        data[i] = {}
        for j in range(0,12):
            data[i][MONTH[j]] = {}
    print(discover)
    ####
    with open('blacklist.json', 'r+') as blacklistJ:
        blacklist = json.load(blacklistJ)
        for index, row in discover.iterrows():
            length = len(data[int(row["Trans. Date"].split("/")[2])][MONTH[int(row["Trans. Date"].split("/")[0])-1]]) #length of current month's JSON object
            if(row["Category"] in blacklist["blacklist"].values()):
                print("Skipping blacklisted category: " + row["Category"])
            elif(row["Category"] in blacklist["nameChange"]):
                data[int(row["Trans. Date"].split("/")[2])][MONTH[int(row["Trans. Date"].split("/")[0])-1]][length] = {"Category":blacklist["nameChange"][row["Category"]], "Amount":0-row["Amount"], "day":int(row["Trans. Date"].split("/")[1]), "Description":row["Description"]}
            elif(row["Category"] not in CATEGORIES):
                print(CATEGORIES)
                value = input(row["Category"] + " not in CATEGORIES. Enter Category manually from list above:")
                data[int(row["Trans. Date"].split("/")[2])][MONTH[int(row["Trans. Date"].split("/")[0])-1]][length] = {"Category":value, "Amount":0-row["Amount"], "day":int(row["Trans. Date"].split("/")[1]), "Description":row["Description"]}
                blacklist["nameChange"][row["Category"]] = value
            else:
                data[int(row["Trans. Date"].split("/")[2])][MONTH[int(row["Trans. Date"].split("/")[0])-1]][length] = {"Category":row["Category"], "Amount":0-row["Amount"], "day":int(row["Trans. Date"].split("/")[1]), "Description":row["Description"]}
        #print(data)
        blacklistJ.seek(0)
        json.dump(blacklist, blacklistJ, indent=4)
        return data

def savorOneCard(file):
    data = {}
    savorOne = pd.read_csv('csv/' + file, parse_dates=False)
    print(savorOne)
    print(savorOne.loc[len(savorOne)-1]["Transaction Date"])#.split("/")[2]+1)
    for i in range(int(savorOne.loc[0]["Transaction Date"].split("-")[0]), int(savorOne.loc[len(savorOne)-1]["Transaction Date"].split("-")[0])+1):
        data[i] = {}
        for j in range(0,12):
            data[i][MONTH[j]] = {}
    print(savorOne)
    ####
    with open('blacklist.json', 'r+') as blacklistJ:
        blacklist = json.load(blacklistJ)
        for index, row in savorOne.iterrows():
            length = len(data[int(row["Transaction Date"].split("-")[0])][MONTH[int(row["Transaction Date"].split("-")[1])-1]]) #length of current month's JSON object
            if(row["Category"] in blacklist["blacklist"].values()):
                print("Skipping blacklisted category: " + row["Category"])
            elif(row["Category"] in blacklist["nameChange"]):
                data[int(row["Transaction Date"].split("-")[0])][MONTH[int(row["Transaction Date"].split("-")[1])-1]][length] = {"Category":blacklist["nameChange"][row["Category"]], "Amount":0-row["Debit"], "day":int(row["Transaction Date"].split("-")[2]), "Description":row["Description"]}
            elif(row["Category"] not in CATEGORIES):
                print(CATEGORIES)
                value = input(row["Category"] + " not in CATEGORIES. Enter Category manually from list above:")
                data[int(row["Transaction Date"].split("-")[0])][MONTH[int(row["Transaction Date"].split("-")[1])-1]][length] = {"Category":value, "Amount":0-row["Debit"], "day":int(row["Transaction Date"].split("-")[2]), "Description":row["Description"]}
                blacklist["nameChange"][row["Category"]] = value
            else:
                data[int(row["Transaction Date"].split("-")[0])][MONTH[int(row["Transaction Date"].split("-")[1])-1]][length] = {"Category":row["Category"], "Amount":0-row["Debit"], "day":int(row["Transaction Date"].split("-")[2]), "Description":row["Description"]}
        #print(data)
        blacklistJ.seek(0)
        json.dump(blacklist, blacklistJ, indent=4)
        return data
    
def sofi(file):
    data = {}
    #datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
    sofi = pd.read_csv('csv/' + file)
    print(sofi)
    #print(int(sofi.loc[0]["Date"]))#.split("/")[2]))#, int(sofi.loc[len(sofi)-1]["Date"].split("/")[2]))
    for i in range(int(sofi.loc[0]["Date"].split("-")[0]), int(sofi.loc[len(sofi)-1]["Date"].split("-")[0])+1):
        data[i] = {}
        for j in range(0,12):
            data[i][MONTH[j]] = {}
    #print(sofi)

    with open('blacklist.json', 'r+') as blacklistJ:
        blacklist = json.load(blacklistJ)
        for index, row in sofi.iterrows():
            length = len(data[int(row["Date"].split("-")[0])][MONTH[int(row["Date"].split("-")[1])-1]]) #length of current month's JSON object
            if(row["Description"] in blacklist["blacklist"].values()):
                print("Skipping blacklisted category: " + row["Description"])
            elif(row["Description"] in blacklist["nameChange"]):
                data[int(row["Date"].split("-")[0])][MONTH[int(row["Date"].split("-")[1])-1]][length] = {"Category":blacklist["nameChange"][row["Description"]], "Amount":row["Amount"], "day":int(row["Date"].split("-")[2]), "Description":row["Type"]}
            elif(row["Description"] not in CATEGORIES):
                print(CATEGORIES)
                value = input(row["Description"] + " not in CATEGORIES. Enter Category manually from list above:")
                data[int(row["Date"].split("-")[0])][MONTH[int(row["Date"].split("-")[1])-1]][length] = {"Category":value, "Amount":row["Amount"], "day":int(row["Date"].split("-")[2]), "Description":row["Description"]}
                blacklist["nameChange"][row["Description"]] = value
            else:
                data[int(row["Date"].split("-")[0])][MONTH[int(row["Date"].split("-")[1])-1]][length] = {"Category":row["Description"], "Amount":row["Amount"], "day":int(row["Date"].split("-")[2]), "Description":row["Type"]}
        #print(data)
        blacklistJ.seek(0)
        json.dump(blacklist, blacklistJ, indent=4)
        return data



#finding files in pdf directory
path = os.getcwd() + '/csv'
dir = os.listdir(path)

#WELCOME STATEMENT
ascii_banner = pyfiglet.figlet_format("Expense Tracker")
print(ascii_banner)
welcome = input("Hello, welcome to Expense Tracker, wanna input some data manually? (y, n): ")
if(welcome.lower() == 'y'):
    print("Awesome! Would you like to: ")
    print("(1)\tUpdate the Blacklist (enter 'b')")
    print("(2)\tManually input a transaction (enter 't')")
    proceed = input("(3)\tClick any key to just proceed... ")
    if(proceed == 't'):
        dateMMDDYYYY = input("Enter the date of transaction (MM/DD/YYYY): ")
        print(CATEGORIES)
        Category = input("Enter the Category from available list: ")
        Amount = input("Enter the Amount: ")
        Description = input("Enter the Description: ")
        addTransaction(dateMMDDYYYY, Category, Amount, Description)

#iterating over files in pdf directory
for file in dir:
    print(file)
#confirm = input("We found the files above as the ones you want to append to the excel, are they correct? (y, n): ")
#confirm.lower()
time.sleep(.5)

for file in dir:
    if("discover" in file.lower()):
        data = discoverCard(file)
        saveDataToJSON(data)
        #print(data)
        updateExcel(data)
    elif("sofi" in file.lower()):
        data = sofi(file)
        saveDataToJSON(data)
        updateExcel(data)
    elif("capitalone" in file.lower()):
        data = savorOneCard(file)
        saveDataToJSON(data)
        updateExcel(data)




#addTransaction("3/29/2024", "Free Money", 9.55, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("2/29/2024", "Free Money", 8.78, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("1/31/2024", "Free Money", 5.91, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("12/31/2023", "Free Money", 6.12, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("11/30/2023", "Free Money", 7.36, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("10/29/2023", "Free Money", 7.56, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("9/29/2023", "Free Money", 7.25, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("8/29/2023", "Free Money", 6.05, "SOFI High Yield Savings Account MANUAL_INPUT")
#addTransaction("8/29/2023", "Free Money", 4, "SOFI Points MANUAL_INPUT")





