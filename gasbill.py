# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:21:28 2022

@author: ariana.ramos
"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import seaborn as sns


#set graph styles
sns.set(style="darkgrid")
sns.set_context("paper")

#%% [1] Measurement in m3 

# Measurement estimated by network operator:
#in m3
Mfeb21= 38899

# Actual measurement made in person:
Mfeb22= 40640

# Consumption ofr the period:
    
P2021= Mfeb22-Mfeb21

#%% conversion to kWh given by Total
totalkWh= 17901.02

myprice= 1769.59/17901.02*100
#my price in c€/ kWh



#%%  Synthetic load profile for 2021
#extracted from VREG website (Vlaamse Regulator van de Elektriciteits- en Gasmarkt)
# https://www.vreg.be/nl/verbruiksprofielen-en-productieprofielen

Data= pd.read_excel('slps_aardgas_2021.xlsx','Gaz Residential')

Data.index= Data.UTC

#Data contains estimated hourly gas profiles. 

#The column S41_6 contains the estimated gas use in kWh for every hour of the year. 

#Tip: to open this file your working directory in the bar at the top right of the screen 
#should contain the file

#%% Visualization entire period


myFmt = DateFormatter('%b') 
fig, ax = plt.subplots(figsize = (12,4))
ax.plot(Data.UTC, Data.S41_6) 
ax.legend(['Synthetic Gas Profile'])
ax.set(xlabel="Month", ylabel="kWh")
ax.set(title="Synthetic Gas Residential Profile 2021");
ax.xaxis.set_major_formatter(myFmt); 

#%% Select specified dates

# Make a function to extract specific dates
def Period(X,date1,date2):
    mask= (X.index >= date1) & (X.index <= date2)
    Xsub= X.loc[mask]
    return Xsub

#%% Select winter day vs summer day 

#winter Tuesday January 5
d1= '2021-01-05 00:00:00'
d2= '2021-01-05 23:00:00'

Jan5= Period(Data,d1,d2)

# Summer day in Tuesday July 6th 2021

d3= '2021-07-06 00:00:00'
d4= '2021-07-06 23:00:00'

Jul6= Period(Data, d3,d4)

#%% Visualize winter day vs summer day 


matplotlib.rc('font', size=14)

sns.set_context("talk", font_scale=0.80,)

myFmt = DateFormatter('%H:%M') 
fig, ax = plt.subplots(figsize = (12,4))
ax.plot(Jan5.index, Jan5.S41_6, '-s') 
ax.plot(Jan5.index, Jul6.S41_6, '-o') 
ax.legend(['Winter day', 'Summer day'])
ax.set(xlabel="Hour", ylabel="kWh")
ax.set(title="Energy Consumption per Cluster");
ax.xaxis.set_major_formatter(myFmt); 

#%% Calculating MY estimated load profile 

#multiply synthetic load profile by my total year consumption 

MyLoad=pd.DataFrame( [totalkWh*n for n in Data.S41_6])

MyLoad.index= Data.index

#%%  Visualizing MY estimated load profile

myFmt = DateFormatter('%b') 
fig, ax = plt.subplots(figsize = (12,4))
ax.plot(MyLoad) 
ax.legend(['Synthetic Gas Profile'])
ax.set(xlabel="Month", ylabel="kWh")
ax.set(title="Fig.1: My 'Synthetic' Gas Profile 2021");
ax.xaxis.set_major_formatter(myFmt); 

#%% Compare summer day vs winter day :
    

#winter Tuesday January 5
d1= '2021-01-05 00:00:00'
d2= '2021-01-05 23:00:00'

MyJan5= Period(MyLoad,d1,d2)

# Summer day in Tuesday July 6th 2021

d3= '2021-07-06 00:00:00'
d4= '2021-07-06 23:00:00'

MyJul6= Period(MyLoad, d3,d4)    

#%%


matplotlib.rc('font', size=14)

sns.set_context("talk", font_scale=0.80,)

myFmt = DateFormatter('%H:%M') 
fig, ax = plt.subplots(figsize = (12,4))
ax.plot(MyJan5.index, MyJan5.values, '-s') 
ax.plot(MyJan5.index, MyJul6.values, '-o') 
ax.legend(['Winter day', 'Summer day'])
ax.set(xlabel="Hour", ylabel="kWh")
ax.set(title="My Winter vs My Summer consumption");
ax.xaxis.set_major_formatter(myFmt); 


#%% Price information on my bill
# 'Le prix moyen TVA comprise sur la durée de la présente Regularisation s'élève à
# 9,885 c€ / kWh

estimate= totalkWh*0.09885

# Estimate cost at average price: 1769.51

#%% Prices I received on my 6th call after waiting more than 40 mins

# 1.89 c EUR/ kWh 
Feb21= 0.0189 

# 11.54 cEUR / kWh
Dec21= 0.1154



#%%% From email I received:  
#Prices of the different contract that apply are always on the website for the current period. 
#The files aren't retroactively visible but you can check there each month to find the current ones.


#%% From website 
#WRONG files in links, only 2022 prices available:
    
# https://totalenergies.be/fr/particuliers/produits-et-services/my-home/electricite-et-gaz/offre-electricite-gaz/cartes-tarifaires-historique


# Le prix de l'énergie est indexé mensuellement selon la formule tarifaire TTF_S41 + 0,145 c€/kWh (hors TVA). 
# TTF_S41 représente la moyenne arithmétique en c€/kWh des cotations TTF Day Ahead durant le mois de fourniture, 
#telles que publiées sur le site web https://www.powernext.com/spot-market-data, pondéré par le profil de consommation S41, 
# telles que publiées sur le site web http://www.synergrid.be.


# contracts signed or renewed before 1 Feb 2022:
# 13,57 c€ / kWh


    
#contracts signed or renewed before 1 feb 2020:
    # wrong information on website (directs to a page for 2022)
    
#%% Monthly prices according to the VREG

Vreg= pd.DataFrame({'month': ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'], 
                    'price': [4.67, 4.44, 4.51, 4.70, 5.03, 5.89, 6.40, 6.96, 10.17, 11.65, 11.43, 15.66]})

Creg= Vreg

fig, ax = plt.subplots(figsize = (12,4))
ax.plot(Vreg.month, Vreg.price)
ax.set(xlabel= 'Month', ylabel= 'c €/kWh')
ax.set(title='Fig.2: CREG Monthly Gas Price')
    
#%%
# add markup by total 0,174 c€/kWh
markup= 0.174

PriceTotal=pd.DataFrame([Vreg.price[n]+markup for n in range(len(Vreg))])


fig, ax = plt.subplots(figsize = (12,4))
ax.plot(Vreg.month, Vreg.price)
ax.plot(PriceTotal.values)
ax.set(xlabel= 'Month', ylabel= 'c€/kWh')
ax.set(title='VREG Monthly Gas Price')

#%% calculate monthly expense

#n= list(range(2,13))

topay=[]

for n in range(len(PriceTotal)):
    topay.append(MyLoad.loc[MyLoad.index.month==n]*PriceTotal.iloc[n])
    
#%%

Feb= MyLoad.loc[MyLoad.index.month==2]*PriceTotal.iloc[0]
Mar= MyLoad.loc[MyLoad.index.month==3]*PriceTotal.iloc[1]
Apr= MyLoad.loc[MyLoad.index.month==4]*PriceTotal.iloc[2]
May= MyLoad.loc[MyLoad.index.month==5]*PriceTotal.iloc[3]
Jun= MyLoad.loc[MyLoad.index.month==6]*PriceTotal.iloc[4]
Jul= MyLoad.loc[MyLoad.index.month==7]*PriceTotal.iloc[5]
Aug= MyLoad.loc[MyLoad.index.month==8]*PriceTotal.iloc[6]
Sept= MyLoad.loc[MyLoad.index.month==9]*PriceTotal.iloc[7]
Oct= MyLoad.loc[MyLoad.index.month==10]*PriceTotal.iloc[8]
Nov= MyLoad.loc[MyLoad.index.month==11]*PriceTotal.iloc[9]
Dec=MyLoad.loc[MyLoad.index.month==12]*PriceTotal.iloc[10]
Jan= MyLoad.loc[MyLoad.index.month==1]*PriceTotal.iloc[11]

#%% My gas bill

Bill= (sum(Feb.values)+sum(Mar.values)+sum(Apr.values)+sum(May.values)+sum(Jun.values)+sum(Jul.values)+sum(Aug.values)+ sum(Sept.values) + sum(Oct.values) + sum(Nov.values) + sum(Dec.values) + sum(Jan.values))/100

#%%
FP= sum(Feb.values)/100

MP=sum(Mar.values)
AP=sum(Apr.values)
MP=sum(May.values)
JP= sum(Jun.values)
JuP= sum(Jul.values)
AP=sum(Aug.values) 
SP= sum(Sept.values) 
OP= sum(Oct.values) 
NP= sum(Nov.values) 
DP= sum(Dec.values) 
JP= sum(Jan.values)

