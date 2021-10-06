# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 17:43:00 2021

@author: MCGUINRO
"""

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.backends.backend_pdf import PdfPages


#cars
nc=2.1e6
ec=3e4
tc=1.1e5
countc=2021
kc=-1*math.log(9/19)
cem=0.131 # from CAF
cef=0.15
ckm=56.54e9 # calculated by dividing car emissions by car emissions per km 
cocc=1.4

#LGVs
nv=2.8e5
ev=1000
tv=18e3
countv=2021
kv=-1*math.log(7/15)
vem=0.168
vef=0.653*(0.36/0.85)
vkm=11.04e9
vocc=1


#HGVs
nt=9e4
et=10
tt=6e3
countt=2021
kt=-1*math.log(5990/11990)
tem=0.482
tef=1.87*(0.42/0.85)
tkm=2.28e9
tocc=1

#buses
nb=10e3
eb=0
tb=500
bem=0.79
bef=1.96
bkm=1.42e9
bocc=17.3

#trains
trcurr=0.5
trem=2.35
tref=3.12
trkm=0.07e9
trocc=60

#Aviation
plem=1e9*(12*(1/0.783-1))
plef=5.78*(35/36)#planes L/km * Kerosenes kWh/L

#international shipping
shem=(49.4e15*0.017)/(3222e9)*1749e3#global amount of shipping emissions/total energy use for navigation * irish energy use for shipping

#domestic navigation and other
dnem=12*0.023e9
oem=12*0.013e9

#walking
wkm=2.48e9

#cycling
cycef=0.0093
cyckm=0.85e9

#electricity
el=np.linspace(2021,2050,30)
for i in range(30):
    if i<=9:
        el[i]=0.324-(0.324/9)*i
    if i>9:
        el[i]=0


#population
pop=np.linspace(2021,2050,30)
for i in range(30):
    pop[i]=1+((6.15-5)/5)*i/29

#reading in parameters from text file
parameterfile=open("Parameters.txt")
params={}
for line in parameterfile:
    line.strip()
    key_value=line.split("=")
    sep="#"
    if len(key_value)==2:
        params[key_value[0].strip()]=int((key_value[1].strip().split(sep,1))[0])
        

#uptake of zero emissions options
def fec(x):
    if x<params["newicecar"]:
        return 1/(1+19 *math.exp(-kc*(x-2021)))
    if x>=params["newicecar"]:
        return 1
    
def fev(x):
    if x<params["newicevan"]:
        return 1/(1+15 *math.exp(-kv*(x-2021)))
    if x>=params["newicevan"]:
        return 1
    
def fet(x):
    if x<params["newicetruck"]:
        return 1/(1+300*math.exp(-kt*(x-2021)))
    if x>=params["newicetruck"]:
        return 1

def feb(x):
    return 1



#fraction of new vehicles sales electric
xx=np.linspace(2021,2036,16)

yc=np.linspace(0,15,16)
for i in range(16):
   yc[i]=fec(xx[i])
   
yv=np.linspace(0,15,16)
for i in range(16):
    yv[i]=fev(xx[i])
    
yt=np.linspace(0,15,16)
for i in range(16):
    yt[i]=fet(xx[i])

fleet1=plt.figure(1)
plt.plot(xx,100*yc)
plt.plot(xx,100*yv)
plt.plot(xx,100*yt)
plt.grid()
plt.legend(["Cars","LGVs","HGVs"])
plt.title("Share of electric vehicles in new sales over time")
plt.xlabel("Year")
plt.ylabel("Percentage share of new vehicle sales electric")
#tc*integrate.quad(lambda x: fec(x),2021,xx+2021)[0]

#car fleet turnover
def fleet(xx):
    if ec+tc*integrate.quad(lambda x: fec(x),2021,xx+2021)[0]-(tc+((params["cardec"]/100)*nc/(30)))*integrate.quad(lambda x: fec(x),2001,2001+xx)[0]>=nc*(1-(params["cardec"]/100)*xx/30):
        return nc*(1-(params["cardec"]/100)*xx/30)
    else:
        return ec+tc*integrate.quad(lambda x: fec(x),2021,xx+2021)[0]-(tc+((params["cardec"]/100)*nc/30))*integrate.quad(lambda x: fec(x),2001,2001+xx)[0]
def fleeti(xx):
    if (nc-ec)+tc*integrate.quad(lambda x: (1-fec(x)),2021,xx+2021)[0]-(tc+((params["cardec"]/100)*nc/30))*integrate.quad(lambda x: (1-fec(x)),2001,2001+xx)[0]<=0:
        return 0
    else:
        return np.heaviside(params["endicecar"]-2021-xx,0)*((nc-ec)+tc*integrate.quad(lambda x: (1-fec(x)),2021,xx+2021)[0]-(tc+((params["cardec"]/100)*nc/30))*integrate.quad(lambda x: (1-fec(x)),2001,2001+xx)[0])


resultc=np.linspace(2021,2050,30)
for i in range(30):
    resultc[i]=round(fleet(i))
    
resultci=np.linspace(2021,2050,30)
for i in range(30):
    resultci[i]=round(fleeti(i))

carfleet=plt.figure(2)
plt.plot(np.linspace(2021,2050,30),resultc)
plt.plot(np.linspace(2021,2050,30),resultci)
plt.plot(np.linspace(2021,2050,30),(resultc+resultci))
plt.title("Composition of car fleet over time")
plt.xlabel("Year")
plt.ylabel("Fleet Size")
plt.legend(["E-cars","ICE cars","Total cars"])
plt.grid()


#van fleet turnover

def evv(xx):
    if ev+tv*integrate.quad(lambda x: fev(x), 2021, xx+2021)[0]-(tv+(params["vandec"]/100)*nv/30)*integrate.quad(lambda x: fev(x), 2005, xx+2005)[0]>=nv*(1-(params["vandec"]/100)*xx/30):
        return nv*(1-(params["vandec"]/100)*xx/30)
    else:
        return ev+tv*integrate.quad(lambda x: fev(x), 2021, xx+2021)[0]-(tv+(params["vandec"]/100)*nv/30)*integrate.quad(lambda x: fev(x), 2005, xx+2005)[0]

def ivv(xx):
    if (nv-ev)+tv*integrate.quad(lambda x: (1-fev(x)), 2021, xx+2021)[0]-(tv+(params["vandec"]/100)*nv/30)*integrate.quad(lambda x: (1-fev(x)), 2005, xx+2005)[0]<0:
        return 0
    else:
        return np.heaviside(params["endicevan"]-2021-xx,0)*((nv-ev)+tv*integrate.quad(lambda x: (1-fev(x)), 2021, xx+2021)[0]-(tv+(params["vandec"]/100)*nv/30)*integrate.quad(lambda x: (1-fev(x)), 2005, xx+2005)[0])


resultv=np.linspace(2021,2050,30)
for i in range(30):
    resultv[i]=round(evv(i))
    
resultvi=np.linspace(2021,2050,30)
for i in range(30):
    resultvi[i]=round(ivv(i))

vanfleet=plt.figure(3)
plt.plot(np.linspace(2021,2050,30),resultv)
plt.plot(np.linspace(2021,2050,30),resultvi)
plt.plot(np.linspace(2021,2050,30),(resultv+resultvi))
plt.title("Composition of van fleet over time")
plt.xlabel("Year")
plt.ylabel("Fleet size")
plt.legend(["E-LGVs","ICE LGVs","Total LGVs"])
plt.grid()

#truck fleet turnover

def evt(xx):
    if et+tt*integrate.quad(lambda x: fet(x), 2021, xx+2021)[0]-(tt+(params["truckdec"]/100)*nt/30)*integrate.quad(lambda x: fet(x), 2005, xx+2005)[0]>=nt*(1-(params["truckdec"]/100)*xx/30):
        return nt*(1-(params["truckdec"]/100)*xx/30)
    else:
        return et+tt*integrate.quad(lambda x: fet(x), 2021, xx+2021)[0]-(tt+(params["truckdec"]/100)*nt/30)*integrate.quad(lambda x: fet(x), 2005, xx+2005)[0]

def ivt(xx):
    if (nt-et)+tt*integrate.quad(lambda x: (1-fet(x)), 2021, xx+2021)[0]-(tt+(params["truckdec"]/100)*nt/30)*integrate.quad(lambda x: (1-fet(x)), 2005, xx+2005)[0]<0:
        return 0
    else:
        return np.heaviside(params["endicetruck"]-2021-xx,0)*((nt-et)+tt*integrate.quad(lambda x: (1-fet(x)), 2021, xx+2021)[0]-(tt+(params["truckdec"]/100)*nt/30)*integrate.quad(lambda x: (1-fet(x)), 2005, xx+2005)[0])


resultt=np.linspace(2021,2050,30)
for i in range(30):
    resultt[i]=round(evt(i))
    
resultti=np.linspace(2021,2050,30)
for i in range(30):
    resultti[i]=round(ivt(i))


truckfleet=plt.figure(4)
plt.plot(np.linspace(2021,2050,30),resultt)
plt.plot(np.linspace(2021,2050,30),resultti)
plt.plot(np.linspace(2021,2050,30),(resultt+resultti))
plt.title("Composition of truck fleet over time")
plt.xlabel("Year")
plt.ylabel("Fleet size")
plt.legend(["E-HGVs","ICE HGVs","Total HGVs"])
plt.grid()

#bus fleet turnover

def evb(xx):
    if tb*(xx)>=nb:
        return nb
    else:
        return tb*(xx)

def ivb(xx):
    if nb-tb*(xx)<0:
        return 0
    else:
        return np.heaviside(params["endicebus"]-2021-xx,0)*(nb-tb*(xx))
    
resultb=np.linspace(2021,2050,30)
for i in range(30):
    resultb[i]=round(evb(i))
    
resultbi=np.linspace(2021,2050,30)
for i in range(30):
    resultbi[i]=round(ivb(i))
 
busfleet=plt.figure(5)
plt.plot(np.linspace(2021,2050,30),resultb)
plt.plot(np.linspace(2021,2050,30),resultbi)
plt.plot(np.linspace(2021,2050,30),(resultb+resultbi))
plt.title("Composition of bus fleet over time")
plt.xlabel("Year")
plt.ylabel("Fleet size")
plt.legend(["E-buses","ICE buses","Total buses"])
plt.grid()

#train electrification
def trainelec(xx):
    if trcurr+0.5*xx/(params["railelec"]-2021)>=1:
        return 1
    else:
        return trcurr+0.5*xx/(params["railelec"]-2021)
def traindiesel(xx):
    if trcurr-0.5*xx/(params["railelec"]-2021)<0:
        return 0
    else:
        return trcurr-0.5*xx/(params["railelec"]-2021)


resulttr=np.linspace(2021,2050,30)
for i in range(30):
    resulttr[i]=trainelec(i)
resulttri=np.linspace(2021,2050,30)
for i in range(30):
    resulttri[i]=traindiesel(i)

trainelectrification=plt.figure(6)    
plt.plot(np.linspace(2021,2050,30),100*resulttr)
plt.plot(np.linspace(2021,2050,30),100*resulttri)
plt.title("Percentage share of train services electrified over time")
plt.xlabel("Year")
plt.ylabel("Share of electrified service")
plt.legend(["Electric","Diesel","Total"])
plt.grid()


#aviation decarbonisation
def planedecarb(xx):
    if params["incavsp"]==0:
        return 0
    else: 
        if xx<=9:
            return pop[xx]*plem*(1-params["planeavoid30"]/100)*(1-xx/10*params["planeeff30"]/100)
        elif plem*(1-params["planeavoid30"]/100)*(1-params["planeeff30"]/100)*(1-(xx-9)/(params["aviation"]-2030))<=0:
            return 0
        else:
            return pop[xx]*plem*(1-params["planeavoid30"]/100)*(1-params["planeeff30"]/100)*(1-(xx-9)/(params["aviation"]-2030))

templ=np.linspace(2021,2050,30)
for i in range(30):
    templ[i]=planedecarb(i)
    
#international shipping decarbonisation
def shipdecarb(xx):
    if params["incavsp"]==0:
        return 0
    else:
        if xx<=9:
            return pop[xx]*shem
        elif shem*(1-(xx-9)/(params["shipping"]-2030))<=0:
            return 0
        else:
            return pop[xx]*shem*(1-(xx-9)/(params["shipping"]-2030))

temsp=np.linspace(2021,2050,30)
for i in range(30):
    temsp[i]=shipdecarb(i)
    
#domestic navigation decarbonisation
def navdecarb(xx):
    if dnem*(1-xx/(2045-2021))<=0:
        return 0
    else:
        return pop[xx]*dnem*(1-xx/(2045-2021))

temdn=np.linspace(2021,2050,30)
for i in range(30):
    temdn[i]=navdecarb(i)

#other decarbonisation    
def otherdecarb(xx):
    if (oem)*(1-xx/(2040-2021))<=0:
        return 0
    else:
        return pop[xx]*(oem)*(1-xx/(2040-2021))

temo=np.linspace(2021,2050,30)
for i in range(30):
    temo[i]=otherdecarb(i)
    


#Distance travelled
ckmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        ckmt[i]=pop[i]*ckm*(1-(params["caravoid30"]+params["car2walk30"]+params["car2bike30"]+params["car2emobil30"]+params["car2bus30"]+params["car2train30"])/100)
    else:
        ckmt[i]=pop[i]*ckm*(1-(0.25+3*i/40)*(params["caravoid30"])/100-i/10*(params["car2walk30"]+params["car2bike30"]+params["car2emobil30"]+params["car2bus30"]+params["car2train30"])/100)

vkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        vkmt[i]=pop[i]*vkm*(1-(params["vanavoid30"]+params["van2ebike30"])/100)
    else:
        vkmt[i]=pop[i]*vkm*(1-i/10*(params["vanavoid30"]+params["van2ebike30"])/100)

tkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        tkmt[i]=pop[i]*tkm*(1-(params["truckavoid30"]+params["truck2rail30"])/100)
    else:
        tkmt[i]=pop[i]*tkm*(1-i/10*(params["truckavoid30"]+params["truck2rail30"])/100)

bkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        bkmt[i]=pop[i]*(bkm+(cocc/bocc *ckm *params["car2bus30"])/100)
    else:
        bkmt[i]=pop[i]*(bkm+i/10*(cocc/bocc *ckm *params["car2bus30"])/100)

trkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        trkmt[i]=pop[i]*(trkm+(cocc/trocc *ckm *params["car2train30"])/100)
    else:
        trkmt[i]=pop[i]*(trkm+i/10*(cocc/trocc *ckm *params["car2train30"]+1/50*tkm*params["truck2rail30"])/100)

wkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        wkmt[i]=pop[i]*(wkm+(cocc*ckm*params["car2walk30"])/100)
    else:
        wkmt[i]=pop[i]*(wkm+i/10*(cocc*ckm*params["car2walk30"])/100)

cyckmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        cyckmt[i]=pop[i]*(cyckm+(cocc*ckm*params["car2bike30"])/100)
    else:
        cyckmt[i]=pop[i]*(cyckm+i/10*(cocc*ckm*params["car2bike30"])/100)

microkmt=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        microkmt[i]=pop[i]*((cocc*ckm*params["car2emobil30"]+vkm*params["van2ebike30"])/100)
    else:
        microkmt[i]=pop[i]*(i/10*(cocc*ckm*params["car2emobil30"]+vkm*params["van2ebike30"])/100)

#Efficiency improvements
careffimp=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        careffimp[i]=(1-params["careff30"]/100)
    else:
        careffimp[i]=(1-i/10*params["careff30"]/100)
        
vaneffimp=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        vaneffimp[i]=(1-params["vaneff30"]/100)
    else:
        vaneffimp[i]=(1-i/10*params["vaneff30"]/100)

truckeffimp=np.linspace(2021,2050,30)
for i in range(30):
    if i>9:
        truckeffimp[i]=(1-params["truckeff30"]/100)
    else:
        truckeffimp[i]=(1-i/10*params["truckeff30"]/100)

#Emissions efficiencies of fleets
carintense=careffimp*(cef*el*resultc+cem*resultci)/(resultc+resultci)
vanintense=vaneffimp*(vef*el*resultv+vem*resultvi)/(resultv+resultvi)
truckintense=truckeffimp*(tef*el*resultt+tem*resultti)/(resultt+resultti)
busintense=(bef*el*resultb+bem*resultbi)/(resultb+resultbi)
trainintense=(tref*el*resulttr+trem*resulttri)
microintense=cycef*el

emissioneffs=plt.figure(7)
plt.plot(np.linspace(2021,2050,30),carintense)
plt.plot(np.linspace(2021,2050,30),vanintense)
plt.plot(np.linspace(2021,2050,30),truckintense)
plt.plot(np.linspace(2021,2050,30),busintense)
plt.plot(np.linspace(2021,2050,30),trainintense)
plt.grid()
plt.xlabel("Year")
plt.title("Emissions efficiencies of vehicle fleets over time")
plt.ylabel("Average fleet CO\u2082 efficiency, kgCO\u2082/km")
plt.legend(["Cars","LGVs","HGVs","Buses","Trains"])



#Total emissions by mode
temc=carintense*ckmt
temv=vanintense*vkmt
temt=truckintense*tkmt
temb=busintense*bkmt
temtr=trainintense*trkmt
temmicro=microintense*microkmt
emit1=plt.figure(8)
plt.plot(np.linspace(2021,2050,30),temc/1e9)
plt.plot(np.linspace(2021,2050,30),templ/1e9)
plt.plot(np.linspace(2021,2050,30),temv/1e9)
plt.plot(np.linspace(2021,2050,30),temb/1e9)
plt.plot(np.linspace(2021,2050,30),temt/1e9)
plt.plot(np.linspace(2021,2050,30),temsp/1e9)
plt.plot(np.linspace(2021,2050,30),temdn/1e9)
plt.plot(np.linspace(2021,2050,30),temo/1e9)
plt.plot(np.linspace(2021,2050,30),temtr/1e9)
plt.plot(np.linspace(2021,2050,30),temmicro/1e9)
plt.grid()
plt.xlabel("Year")
plt.ylabel("Annual emissions, MtCO\u2082")
plt.title("Annual emissions over time by mode")
plt.legend(["Cars","Planes","LGVs","Buses","HGVs","Shipping","Navigation","Other","Trains","E-mobility"])


emit2=plt.figure(9)
plt.stackplot(np.linspace(2021,2050,30),temc/1e9,templ/1e9,temv/1e9,temb/1e9,temt/1e9,temsp/1e9,temdn/1e9,temo/1e9,temtr/1e9,temmicro/1e9)
plt.xlabel("Year")
plt.ylabel("Total annual emissions, MtCO\u2082")
plt.title("Total annual emissions over time by mode")
plt.legend(["Cars","Planes","LGVs","Buses","HGVs","Shipping","Navigation","Other","Trains","E-mobility"])
    


cemc=np.linspace(2021,2030,30)
for i in range(30):
    cemc[i]=sum(temc[0:i])

cempl=np.linspace(2021,2030,30)
for i in range(30):
    cempl[i]=sum(templ[0:i])

cemv=np.linspace(2021,2030,30)
for i in range(30):
    cemv[i]=sum(temv[0:i])

cemb=np.linspace(2021,2030,30)
for i in range(30):
    cemb[i]=sum(temb[0:i])

cemt=np.linspace(2021,2030,30)
for i in range(30):
    cemt[i]=sum(temt[0:i])

cemsp=np.linspace(2021,2030,30)
for i in range(30):
    cemsp[i]=sum(temsp[0:i])
    
cemdn=np.linspace(2021,2030,30)
for i in range(30):
    cemdn[i]=sum(temdn[0:i])
    
cemo=np.linspace(2021,2030,30)
for i in range(30):
    cemo[i]=sum(temo[0:i]) 

cemtr=np.linspace(2021,2030,30)
for i in range(30):
    cemtr[i]=sum(temtr[0:i])
    
cemmicro=np.linspace(2021,2030,30)
for i in range(30):
    cemmicro[i]=sum(temmicro[0:i])

emit3=plt.figure(10) 
plt.stackplot(np.linspace(2021,2050,30),cemc/1e9,cempl/1e9,cemv/1e9,cemb/1e9,cemt/1e9,cemsp/1e9,cemdn/1e9,cemo/1e9,cemtr/1e9,cemmicro/1e9)
plt.xlabel("Year")
plt.ylabel("Cumulative emissions, MtCO\u2082")
plt.title("Cumulative emissions over time by mode")
plt.legend(["Cars","Planes","LGVs","Buses","HGVs","Shipping","Navigation","Other","Trains","E-mobility"],loc = "upper left")




temvct=pd.DataFrame([[2021,temc[0]/1e9,templ[0]/1e9,temv[0]/1e9,temb[0]/1e9,temt[0]/1e9,temsp[0]/1e9,temdn[0]/1e9,temo[0]/1e9,temtr[0]/1e9,temmicro[0]/1e9],
                     [2025,temc[4]/1e9,templ[4]/1e9,temv[4]/1e9,temb[4]/1e9,temt[4]/1e9,temsp[4]/1e9,temdn[4]/1e9,temo[4]/1e9,temtr[4]/1e9,temmicro[4]/1e9],
                     [2030,temc[9]/1e9,templ[9]/1e9,temv[9]/1e9,temb[9]/1e9,temt[9]/1e9,temsp[9]/1e9,temdn[9]/1e9,temo[9]/1e9,temtr[9]/1e9,temmicro[9]/1e9],
                     [2035,temc[14]/1e9,templ[14]/1e9,temv[14]/1e9,temb[14]/1e9,temt[14]/1e9,temsp[14]/1e9,temdn[14]/1e9,temo[14]/1e9,temtr[14]/1e9,temmicro[14]/1e9],
                     [2040,temc[19]/1e9,templ[19]/1e9,temv[19]/1e9,temb[19]/1e9,temt[19]/1e9,temsp[19]/1e9,temdn[19]/1e9,temo[19]/1e9,temtr[19]/1e9,temmicro[19]/1e9],
                    [2045,temc[24]/1e9,templ[24]/1e9,temv[24]/1e9,temb[24]/1e9,temt[24]/1e9,temsp[24]/1e9,temdn[19]/1e9,temo[19]/1e9,temtr[24]/1e9,temmicro[24]/1e9],
                    [2050,temc[29]/1e9,templ[29]/1e9,temv[29]/1e9,temb[29]/1e9,temt[29]/1e9,temsp[29]/1e9,temdn[29]/1e9,temo[29]/1e9,temtr[29]/1e9,temmicro[29]/1e9]],
    columns=["Year","Cars","Planes","LGVs","Buses","HGVs","Ships","Navigation","Other","Trains","E-mobility"])


temvct.plot(x='Year', kind='bar', stacked=True)
plt.ylabel("Total Annual Emissions, MtCO\u2082")
plt.title("Annual emmisions composition by mode in 5-year intervals")
emit4=plt.figure(11)

temcbvct=pd.DataFrame([["CB1",sum(temc[0:4])/1e9,sum(templ[0:4])/1e9,sum(temv[0:4])/1e9,sum(temb[0:4])/1e9,sum(temt[0:4])/1e9,sum(temsp[0:4])/1e9,sum(temdn[0:4])/1e9,sum(temo[0:4])/1e9,sum(temtr[0:4])/1e9,sum(temmicro[0:4])/1e9],
                     ["CB2",sum(temc[5:9])/1e9,sum(templ[5:9])/1e9,sum(temv[5:9])/1e9,sum(temb[5:9])/1e9,sum(temt[5:9])/1e9,sum(temsp[5:9])/1e9,sum(temdn[5:9])/1e9,sum(temo[5:9])/1e9,sum(temtr[5:9])/1e9,sum(temmicro[5:9])/1e9],
                     ["CB3",sum(temc[10:14])/1e9,sum(templ[10:14])/1e9,sum(temv[10:14])/1e9,sum(temb[10:14])/1e9,sum(temt[10:14])/1e9,sum(temsp[10:14])/1e9,sum(temdn[10:14])/1e9,sum(temo[10:14])/1e9,sum(temtr[10:14])/1e9,sum(temmicro[10:14])/1e9],
                     ["CB4",sum(temc[15:19])/1e9,sum(templ[15:19])/1e9,sum(temv[15:19])/1e9,sum(temb[15:19])/1e9,sum(temt[15:19])/1e9,sum(temsp[15:19])/1e9,sum(temdn[15:19])/1e9,sum(temo[15:19])/1e9,sum(temtr[15:19])/1e9,sum(temmicro[15:19])/1e9],
                     ["CB5",sum(temc[20:24])/1e9,sum(templ[20:24])/1e9,sum(temv[20:24])/1e9,sum(temb[20:24])/1e9,sum(temt[20:24])/1e9,sum(temsp[20:24])/1e9,sum(temdn[20:24])/1e9,sum(temo[20:24])/1e9,sum(temtr[20:24])/1e9,sum(temmicro[20:24])/1e9],
                    ["CB6",sum(temc[25:29])/1e9,sum(templ[25:29])/1e9,sum(temv[25:29])/1e9,sum(temb[25:29])/1e9,sum(temt[25:29])/1e9,sum(temsp[25:29])/1e9,sum(temdn[25:29])/1e9,sum(temo[25:29])/1e9,sum(temtr[25:29])/1e9,sum(temmicro[25:59])/1e9]],
    columns=["Carbon budget","Cars","Planes","LGVs","Buses","HGVs","Ships","Navigation","Other","Trains","E-mobility"])


temcbvct.plot(x='Carbon budget', kind='bar', stacked=True)
plt.ylabel("Total carbon budget emissions, MtCO\u2082")
plt.title("Cumulative emmisions by mode over each 5-year interval")
emit5=plt.figure(12)

#energy usage
#energy
petrolefc=(6.447+5.278+5.824)/300 * (34.8/3.6)*careffimp# kwh/km of petrol cars= L/km (from CAF) * kWh/L
dieselefc=(5.435+4.127+4.403)/300 * (38.6/3.6)*careffimp# kwh/km of diesel cars= L/km (from CAF) * kWh/L
dieselefv=(6.462+5.197+6.642)/300 * (38.6/3.6)*vaneffimp# kwh/km of diesel LGVs= L/km (from CAF) * kWh/L
dieseleft=(18.430+14.772+19.200)/300 * (38.6/3.6)*truckeffimp# kwh/km of diesel HGVs= L/km (from CAF) * kWh/L
dieselefb=(34.707+24.154+27.077)/300 * (38.6/3.6)# kwh/km of diesel buses= L/km (from CAF) * kWh/L
dieseleftr=trem/(0.264)#kWh/km of diesel train = kgCO2/km of train /(kgCO2/kWh of diesel fuel)

petrol=np.linspace(2021,2050,30)
for i in range(30):
    petrol[i]=(0.29*(resultci[i]/nc)*ckmt[i]*petrolefc[i])/1e9

diesel=np.linspace(2021,2050,30)
for i in range(30):
    diesel[i]=(0.71*(resultci[i]/nc)*ckmt[i]*dieselefc[i]+(resultvi[i]/nv)*vkmt[i]*dieselefv[i]+(resultti[i]/nt)*tkmt[i]*dieseleft[i]+(resultbi[i]/nb)*bkmt[i]*dieselefb+resulttri[i]*trkmt[i]*dieseleftr+(temdn[i]+temo[i])/(0.252))/1e9

electricityuse=np.linspace(2021,2050,30)
for i in range(30):
    electricityuse[i]=((resultc[i]/nc)*ckmt[i]*cef+(resultv[i]/nv)*vkmt[i]*vef+(resultt[i]/nt)*tkmt[i]*tef+(resultb[i]/nb)*bkmt[i]*bef+resulttr[i]*trkmt[i]*tref+microkmt[i]*cycef+0.5/(0.252)*(temdn[0]-temdn[i]+temo[0]-temo[i]))/1e9

heavyoil=np.linspace(2021,2050,30)
for i in range(30):
    heavyoil[i]=(temsp[i]/shem)*1.749
    
ammonia=np.linspace(2021,2050,30)
for i in range(30):
    if params["incavsp"]==0:
        ammonia[i]=0
    else:
        ammonia[i]=(1-temsp[i]/(pop[i]*shem))*1.749/(5.166*0.5/11)#this factor accounts for efficiency of producing and utilising green ammonia
    
kerosene=np.linspace(2021,2050,30)
for i in range(30):
    kerosene[i]=(templ[i])/(0.2519e9)
    
ekerosene=np.linspace(2021,2050,30)
for i in range(30):
    if params["incavsp"]==0:
        ekerosene[i]=0
    else:
        if i<=9:
            ekerosene[i]=(1-templ[i]/(pop[i]*plem*(1-params["planeavoid30"]/100)*(1-i/10*params["planeeff30"]/100)))*plem*(1-params["planeavoid30"]/100)*(1-i/10*params["planeeff30"]/100)/(0.2519e9)/(1/5)
        else:
            ekerosene[i]=(1-templ[i]/(pop[i]*plem*(1-params["planeavoid30"]/100)*(1-params["planeeff30"]/100)))*plem*(1-params["planeavoid30"]/100)*(1-params["planeeff30"]/100)/(0.2519e9)/(1/5)#I couldn't find an accurate estimate of this so have chosen 5kwh electricty to produce and utilise 1kwh of e-kerosene
#I couldn't find an accurate estimate of this so have chosen 6kwh electricty to produce and utilise 1kwh of e-kerosene

        

energy1=plt.figure(13)
plt.stackplot(np.linspace(2021,2050,30),petrol,diesel,electricityuse,kerosene,ekerosene,heavyoil,ammonia)
plt.xlabel("Year")
plt.ylabel("Energy use, TWh")
plt.title("Energy use over time by fuel")
plt.legend(["Petrol","Diesel", "Electricity","Kerosene","E-kerosene","Heavy oil", "Ammonia"],loc="upper left")


#Passenger mode share
modevct=pd.DataFrame([[2021,ckmt[0]*cocc/5e6,bkmt[0]*bocc/5e6,trkmt[0]*trocc/5e6,wkmt[0]/5e6,cyckmt[0]/5e6,microkmt[0]/5e6],
                     [2025,ckmt[4]*cocc/(5e6*pop[4]),bkmt[4]*bocc/(5e6*pop[4]),trkmt[4]*trocc/(5e6*pop[4]),wkmt[4]/(5e6*pop[4]),cyckmt[4]/(5e6*pop[4]),microkmt[4]/(5e6*pop[4])],
                     [2030,ckmt[9]*cocc/(5e6*pop[9]),bkmt[9]*bocc/(5e6*pop[9]),trkmt[9]*trocc/(5e6*pop[9]),wkmt[9]/(5e6*pop[9]),cyckmt[9]/(5e6*pop[9]),microkmt[9]/(5e6*pop[9])]],
    columns=["Year","Car","Bus","Train","Walking","Cycling","E-mobility"])



modevct.plot(x='Year', kind='bar', stacked=True)
plt.ylabel("Average annual personal mobility, km")
plt.title("Average annual personal mobility by mode in 5-year intervals")
mode1=plt.figure(14)

 
output = PdfPages("Output.pdf")
output.savefig(fleet1, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(carfleet, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(vanfleet, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(truckfleet, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(busfleet, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(trainelectrification, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emissioneffs, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emit1, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emit2, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emit3, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emit4, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(emit5, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(energy1, dpi = 300, transparent = True,bbox_inches="tight")
output.savefig(mode1, dpi = 300, transparent = True,bbox_inches="tight")
output.close()

