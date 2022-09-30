# Takes about 2 hours to run due to data extraction from the internet archive.
import matplotlib.pyplot as plt
import requests
import bs4
import json
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


res = requests.get('https://www.worldometers.info/coronavirus/')
soup = bs4.BeautifulSoup(res.text,'lxml')
l = []
l = soup.find_all("script")

k = []
for i in range(len(l)):
    if("series" in str(l[i])):
        k.append(l[i])

d = []
for i in range(len(k)):
    if("Daily New Cases" in str(k[i])):
        d.append(k[i])    

# print(d)
cases = str(d[0])
ind = cases.find("name: 'Daily Cases',")

par1 = cases.find("[", ind)
par2 = cases.find("]", ind)
data = cases[par1+1:par2]

final_data = data.split(",")

for i in range(len(final_data)):
    if(final_data[i] == "null"):
        final_data[i] = 0
    else:    
        final_data[i] = int(final_data[i])

final_data = [0,0,0,0,0,0,0] + final_data
# print(len(final_data))  
# print(len(final_data)) 

# ind_y = cases.find("text: 'Daily New Cases'") 
# print(cases[ind_y])
x1 = cases.find("[")
x2 = cases.find("]")
data_x = cases[x1+1:x2]

final_x = data_x.split(",")
final_x = ['"Jan 15"', '"Jan 16"', '"Jan 17"', '"Jan 18"', '"Jan 19"', '"Jan 20"', '"Jan 21"'] + final_x
# print(len(final_x))

final_x = final_x[:301]
final_data = final_data[:301]
print("Data of the x-axis (coronavirus cases)", final_x , "\n")
print("Data of the y-axis (coronavirus cases)",final_data, "\n")   
# 14177

#Note - here "final_data" is the list for the data of y-axis, and "final_x" is the list of the data of x-axis.

start_date = date.fromisoformat('2020-01-15')
new_date = start_date

query = '("coronavirus" OR "covid") AND date:' + new_date.isoformat()
payload = {   "q" : query,
           "output" : "json",
           "rows" : "200000"}

# l = []
news_data_x = []
news_data_y = []
while (new_date != date.fromisoformat('2020-11-11')):
    query = '("coronavirus" OR "covid") AND date:' + new_date.isoformat()
    payload["q"] = query
#     print (query)
    r = requests.get('https://archive.org/advancedsearch.php', params=payload)
#     print (r.url)
    request_data = json.loads(r.text)
    numFound = request_data['response']['numFound']
    news_data_x.append(new_date.isoformat())
    news_data_y.append(numFound)
#     l.append((new_date, numFound))
#     print (new_date.isoformat()+ ','+ str(numFound))
    new_date = new_date + timedelta(days = 1) 
print("news_data_x", news_data_x)
print("news_data_y", news_data_y)  

final_Data = []

list1 = []
t = int(len(final_data)/7)
for i in range (t):
    for j in range  (7*i, 7*(i+1)):
        list1.append(final_data[j])
    l2 = numpy.average(list1[7*i:7*(i+1)])
    final_Data.append(l2)


final_X = []
for i in range (int(len(final_x)/7)):
    
    final_X.append(final_x[i*7])

x = []
y = []
for i in range (len(final_X)):
    x.append(final_X[i])
    y.append(final_Data[i])
plt.xlabel('weeks')
plt.ylabel('Number of Daily Cases')
plt.title('Coronavirus Spread')
plt.plot(x,y)
plt.show()


news_data_Y = []
list2 = []
for i in range (int(len(news_data_y)/7)):
    for j in range  (7*i, 7*(i+1)):
        list2.append(news_data_y[j])
    l3 = numpy.average(list2[7*i:7*(i+1)])
    news_data_Y.append(l3)


news_data_X = []
for i in range (int(len(news_data_x)/7)):
    
    news_data_X.append(news_data_x[7*i])

x = []
y = []
for i in range (len(news_data_X)):
    x.append(final_X[i])
    y.append(news_data_Y[i])
plt.xlabel('weeks')
plt.ylabel('Number of Daily Cases')
plt.title('Coronavirus Spread')
plt.plot(x,y)
plt.show()



xData = np.array(final_data)#covid
yData = np.array(news_data_y)#news

fig = plt.figure()
ax1 = fig.add_subplot(211)

ax1.xcorr(xData, yData, usevlines=True, maxlags=50, normed=True,lw=2)

ax1.grid(True)
ax1.axhline(0, color='blue', lw=2)


corr, _ = pearsonr(xData, yData)
print('Pearsons correlation: %.3f' % corr)
plt.xlabel('Coronavirus Data')
plt.ylabel('News Data')
plt.title('Correlation')
plt.show()
