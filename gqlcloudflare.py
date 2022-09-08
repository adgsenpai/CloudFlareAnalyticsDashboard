# This script gqlcloudflare runs cloudflare graphql queries
import requests
import json
import pandas as pd
import pycountry

def send_query(gqlquery, email, gqlapikey):
    request = requests.post('https://api.cloudflare.com/client/v4/graphql', json={'query': gqlquery}, headers={
                            'X-Auth-Email': email, 'Authorization': 'Bearer '+gqlapikey, 'Content-Type': 'application/json'})
    return request.json()


def RetriveWebAnalytics():
    with open('graphqlscripts/WebAnalyticQuery.graphql', 'r') as file:
        gqlquery = file.read().replace('\n', '')
    
    #FULL IN YOUR CLOUDFLARE DETAILS HERE
    gqlapikey = 'APIKEY'
    email = 'EMAIL'
    zonetag = 'ZONEID'
    
    gqlquery = gqlquery.replace('ZONETAG', zonetag)

    datapulled = send_query(gqlquery, email, gqlapikey)

    # save to file
    with open('WebAnalyticQuery.json', 'w') as file:
        json.dump(datapulled, file, indent=4, sort_keys=True)
    return datapulled

# pretty print json


def ppjson(jsondata):
    print(json.dumps(jsondata, indent=4, sort_keys=True))


def GetTotalDataServedToday():

    with open('WebAnalyticQuery.json', 'r') as file:
        data = json.load(file)
    bytes = data['data']['viewer']['zones'][0]['httpRequests1dGroups'][0]['CountryData']['TotalBytesTransfered']
    # convert bytes to GB
    GB = bytes / 1000000000
    # round to 2 decimal places
    GB = round(GB, 2)
    return GB


def GetTotalRequestsToday():

    with open('WebAnalyticQuery.json', 'r') as file:
        data = json.load(file)
    requests = data['data']['viewer']['zones'][0]['httpRequests1dGroups'][0]['CountryData']['TotalRequests']
    return requests


def GetTotalPageViewsToday():

    with open('WebAnalyticQuery.json', 'r') as file:
        data = json.load(file)
    pageviews = data['data']['viewer']['zones'][0]['httpRequests1dGroups'][0]['CountryData']['TotalPageViews']
    return pageviews


def GetUniqueDevicesToday():

    with open('WebAnalyticQuery.json', 'r') as file:
        data = json.load(file)
    devices = data['data']['viewer']['zones'][0]['httpRequests1dGroups'][0]['UniqueIP']['UniqueDevices']
    return devices


def CompileDF():    
    with open('WebAnalyticQuery.json', 'r') as file:
        data = json.load(file)
    # create df
    df = pd.DataFrame(data['data']['viewer']['zones']
                      [0]['httpRequests1dGroups'])
    return df


def ReturnUniqueDevicesDF():
    df = CompileDF()
    # create df with unique devices
    df2 = pd.DataFrame(df['UniqueIP'].tolist())
    # also add date column
    date = df['date'].tolist()
    # loop through date and add to df
    for i in range(len(date)):
        df2.at[i, 'date'] = date[i]['date']

    # calculate monthly unique devices
    df2['month'] = pd.DatetimeIndex(df2['date']).month
    df2['year'] = pd.DatetimeIndex(df2['date']).year
    df2['monthyear'] = df2['month'].astype(str) + '-' + df2['year'].astype(str)
    df2 = df2.groupby(['monthyear']).sum()
    df2 = df2.drop(['month', 'year'], axis=1)
    return df2


def GetAnalyticsDF():
    df = CompileDF()
    # create df with browser information
    df3 = pd.DataFrame(df['CountryData'].tolist())
    # also add date column
    date = df['date'].tolist()
    # loop through date and add to df
    for i in range(len(date)):
        df3.at[i, 'date'] = date[i]['date']

    # calculate monthly unique devices
    df3['month'] = pd.DatetimeIndex(df3['date']).month
    df3['year'] = pd.DatetimeIndex(df3['date']).year
    df3['monthyear'] = df3['month'].astype(str) + '-' + df3['year'].astype(str)
    df3 = df3.groupby(['monthyear']).sum()
    df3 = df3.drop(['month', 'year'], axis=1)

    # convert bytes to GB
    df3['TotalGBTransfered'] = df3['TotalBytesTransfered'] / 1000000000
    # round to 2 decimal places
    df3['TotalGBTransfered'] = df3['TotalGBTransfered'].round(2)


    return df3


def GetBroswerDataDF():
    df = CompileDF()
    # create df with browser information
    df4 = pd.DataFrame(df['CountryData'].tolist())

    # work with BroswerTypes column
    df5 = pd.DataFrame(df4['BroswerTypes'].tolist())

    # also add date column
    date = df['date'].tolist()
    # loop through date and add to df
    for i in range(len(date)):
        df5.at[i, 'date'] = date[i]['date']
    # create new empty df
    df6 = pd.DataFrame()


    # loop through df5[0]
    for i in range(len(df5[0])):
        # print(df5[0][i])
        df6 = pd.concat([df6, pd.DataFrame.from_records(
            [df5[0][i]])], ignore_index=True)
        
    # loop through df5[1]
    for i in range(len(df5[1])):
        # print(df5[1][i])
        df6 = pd.concat([df6, pd.DataFrame.from_records(
            [df5[1][i]])], ignore_index=True)

    # loop through df5[2]
    for i in range(len(df5[2])):
        # print(df5[2][i])
        df6 = pd.concat([df6, pd.DataFrame.from_records(
            [df5[2][i]])], ignore_index=True)

        
    # create a new dataframe and get the total of each browser
    df7 = df6.groupby(['uaBrowserFamily']).sum()
    
    return df7

def GetCountryData():
    df = CompileDF()['CountryData']

    newDF = pd.DataFrame()
    for i in range(len(df)):
        newDF = pd.concat([newDF, pd.DataFrame.from_records(
            [df[i]['Countries']])], ignore_index=True)
    
    finalDF = pd.DataFrame()

    # loop by each row
    for i in range(len(newDF)):
        # loop by each column
        for j in range(len(newDF.columns)):
            # if not none
            if newDF[j][i] != None:
                # add to final df
                try:
                    finalDF = pd.concat([finalDF, pd.DataFrame.from_records(
                        [newDF[j][i]])], ignore_index=True)
                except:
                    pass

    # sum all the rows
    finalDF = finalDF.groupby(['clientCountryName']).sum()

    # remove index and set it as a column
    finalDF = finalDF.reset_index()

    # convert clientCountryName from country code to country name
    for i in range(len(finalDF)):
        try:
            finalDF.at[i, 'clientCountryName'] = pycountry.countries.get(alpha_2=finalDF['clientCountryName'][i]).name
        except Exception as e:
            pass
    # return top 10 countries
    finalDF = finalDF.nlargest(10, 'requests')
    #remove index
    finalDF = finalDF.reset_index(drop=True)
    return finalDF    