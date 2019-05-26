
# coding: utf-8

# In[96]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic(u'matplotlib inline')


# In[3]:

df = pd.read_csv('911.csv')


# In[4]:

df.info()


# In[5]:

df.head()


# In[6]:

df['zip'].value_counts().head(5)#i 5 cap più frequenti nelle chiamate 911


# In[7]:

df['twp'].value_counts().head(5)#top 5 città 


# In[8]:

df['title'].nunique()#quanti titoli descrittivi unici abbiamo 


# In[17]:

x = df['title'].iloc[0]
x


# In[10]:

x.split(':')[0]#Creo nuovi elementi nel datframe


# In[11]:

df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])


# In[12]:

df ['Reason']#Ragioni


# In[13]:

df['Reason'].value_counts()#Conteggio delle ragioni di chiamata


# In[1]:

#Adesso uso seaborn per fare un plot 


# In[21]:

sns.countplot(x='Reason', data=df)#mi mette sulle X la nuova colonna e incorcia i dati automaticamente con il dataframe principale passandolo sulla y


# In[30]:

type(df['timeStamp'].iloc[0])#mi soffermo sul tipo di dato della colonna timestamp


# In[31]:

#Adesso devo convertire il tipo di data in Data


# In[39]:

df['timeStamp']=pd.to_datetime(df['timeStamp'])#riconfiguro la colonna come tipo data


# In[42]:

type(df['timeStamp'].iloc[0])#verifico il corretto cambio, ho un oggetto data poso fare delle operazioni


# In[45]:

time = df['timeStamp'].iloc[0]#quando ho un tipo di dato data in pandas ho dei metodi che leggono ore,mesi,anni
time


# In[46]:

time.hour


# In[48]:

time.year


# In[49]:

time.month


# In[50]:

#POSSO CREARE NUOVE COLONNE PER CREARE NUOVI DATI 


# In[53]:

df['Hour']=df['timeStamp'].apply(lambda time: time.hour)#Uso lambda per esplodere la funzione .hour su tutta la colonna time stamp


# In[55]:

df['Hour'].head()#Creo la colonna ore


# In[56]:

df['Month']=df['timeStamp'].apply(lambda time: time.month)


# In[57]:

df['Month'].head()#creo una nuova colonna mese


# In[60]:

df['Day Of Week']=df ['timeStamp'].apply(lambda time: time.dayofweek)


# In[61]:

df['Day Of Week'].head()#creo una nuova colonna giorno della settimana


# In[63]:

#Adesso che ho i giorni della settimana numerici devo convertirli in Nomi 
#Devo creare un dizionario e usare La funzione map()


# In[64]:

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[65]:

df['Day Of Week']=df['Day Of Week'].map(dmap)


# In[66]:

df['Day Of Week'].head()#Sostituzione Effettuata


# In[67]:

#Adesso Effettuo un conteggio dei giorni della settimana in base alle ragioni di chiamata


# In[68]:

sns.countplot(x='Day Of Week',data=df)#conteggio su tutti i dati 


# In[71]:

sns.countplot(x='Day Of Week', data=df, hue='Reason')#Adesso con seaborn posso filtrare le maggiorni ragioni di chiamata per giorno!
#strumento potentissimo


# In[73]:

#Adesso voglio raggruppare per mese,creo un oggetto di questo tipo


# In[74]:

sns.countplot(x='Month', data=df, hue='Reason')#Stesso grafico per mese


# In[75]:

#adesso faccio un analisi sul Mese 


# In[76]:

byMonth = df.groupby('Month').count()#Faccio una groupby 


# In[77]:

byMonth.head()


# In[78]:

#Adesso posso creare dei plot semplici per colonna del dataframe byMont


# In[79]:

byMonth['lat'].plot()


# In[80]:

#Adesso con la funzione lmplot() che crea un fit lineare del numero di telefonate per mese
#NB per usare tale funzione bisogna resettare l'index


# In[81]:

sns.lmplot(x='Month',y='twp', data= byMonth.reset_index())


# In[82]:

#Adesso creo una nuova Colonna Data a partire dalla colonna timeStamo


# In[83]:

t = df['timeStamp'].iloc[0]#estraggo la prima riga


# In[84]:

t


# In[86]:

t.date()


# In[89]:

df['Date']=df['timeStamp'].apply(lambda t:t.date())#Creo una nuova Colonna per Data 


# In[91]:

df.groupby('Date').count().head()#Posso fare un analisi per data del mio DataSet


# In[92]:

df.groupby('Date').count()['lat']#estraggo la colonna delle chiamate ricevute con informazione di latitudine


# In[97]:

df.groupby('Date').count()['lat'].plot()#faccio un plot di questo dato
plt.tight_layout()#cosi sistemo l'overlapping sull'asse x


# In[98]:

#Adesso ricreo i plot per Ragione, Ems, Fire, Traffic


# In[101]:

df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[102]:

df[df['Reason']=='Fire'].groupby('Date').count()['lat'].plot()
plt.title('Fire')
plt.tight_layout()


# In[103]:

df[df['Reason']=='EMS'].groupby('Date').count()['lat'].plot()
plt.title('EMS')
plt.tight_layout()


# In[104]:

#Adesso creiamo una Mappa Di Calore con il nostro dataframe modificato usando il metodo unstack()


# In[107]:

#faccio una group by multipla per giorno della settimana e ore, e le filtro per Raione, poi forzo il data frame su una matrice con il metodo unstack()
df.groupby(by=['Day Of Week','Hour']).count()['Reason'].unstack()


# In[108]:

#Definisco il nuovo DataFrame
dayHour = df.groupby(by=['Day Of Week','Hour']).count()['Reason'].unstack()


# In[111]:

#Adesso col nuovo data frame posso creare la mappa di calore
sns.heatmap(dayHour, cmap='viridis')#con cmap aggiungo il Colore Verde


# In[113]:

plt.figure(figsize=(12,6))#Rendo più leggibile cambiando dimensione alla figura
sns.heatmap(dayHour, cmap='viridis')



# In[121]:

#Adesso posso  creare un Clustermap
sns.clustermap(dayHour, cmap='coolwarm')


# In[116]:

#Ricostruisco per Mese
dayMonth = df.groupby(by=['Day Of Week','Month']).count()['Reason'].unstack()


# In[118]:

plt.figure(figsize=(12,6))#Rendo più leggibile cambiando dimensione alla figura
sns.heatmap(dayMonth, cmap='viridis')


# In[120]:

sns.clustermap(dayMonth, cmap='coolwarm')


# Abbiamo effettuato un analisi completa delle telefonate ricevute al 911 a NewYork Dal 2015 al 2018 
# Si nota dai grafici estratti che la maggiorparte delle chiamate per le tre MacroAeree di ragioni si concentrano tra le 8 e le 18 tutti i giorni della settimana in particolare dal giovedi alla domenica.
# Da qui si potrebbe Creare un modello predittivo delle chiamate che potrebbere arrivare e per quale motivo!!!
# 
# 
