from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys

if './' not in sys.path:
    sys.path.append('./')





getfa = {
"Movie_tr1":{"Dir":[0,1,2],"Prod":[0,1,2],"SP":[1],"SR":[0,1,2],"M":[0,1,2],"Cin":[1],"EdiB":[0,1,2],"PC":[1],
    "Dby":[0,1,2],"Rdate":[0,1,2],"Rtime":[1],"Cty":[0,1,2],"Lang":[0,1,2],"Budg":[1],"BO":[1]},
"Book_tr1":{"P":[1],"Sch":[1],"Fmt":[0,1,2],"Gen":[0,1,2],"PubDate":[1],
        "NI":[1],"MChar":[0,1,2],"Wby":[0,1,2]},
"FnD_tr1":{"Mf":[1],"COP":[0,1,2],"VF":[0,1,2],"In":[1],"RPd":[0,1,2],
    "Abv":[1],"W":[1],"C":[0,1,2],"MIn":[0,1,2],"T":[0,1,2]},
"Organiz_tr1":{"W":[1],"Hq":[1],"Fd":[1],"In":[0,1,2],"Kp":[0,1,2],"Pdt":[0,1,2],"Ne":[1],"Ta":[0,1,2],"F":[0,1,2],
    "As":[0,1,2],"T":[1],"S":[0,1,2],"P":[1],"O":[1],"Pred":[1]},
"Fest_tr1":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],
    "Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],
    "2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"SpEv_tr1":{"Venue_Location":[0,1,2],"Date_Dates":[1],"Competitors":[0,1,2],"Teams":[1],
	"No_of_events":[1],"Established_Founded":[1],"Official_site":[1]},
"Univ_tr1":{"W":[1],"T":[0,1,2],"E":[1],"Ug":[1],"Pg":[1],
    "M":[0,1,2],"L":[1],"N":[1],"C":[1],"Col":[0,1,2],
    "St":[1],"Ac":[1],"Ad":[1],"Pr":[1],"Edw":[1],"Ma":[1],
    "Prov":[1],"SAf":[0,1,2],"AAf":[0,1,2],"Fn":[1]}
}





Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories.tsv",sep="\t") 
# Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t")





Ptab = np.array(Catg[Catg.category.isin(['Festival'])].table_id)
tablesFolder = "/content/drive/My Drive/Auto-TNLI/data/tables"
# tablesFolder = "../../autotnlidatasetandcode/tables"





def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
#     keys =[i.text for i in soup.find('tr').find_all('th')]
    keys = []
#     keys.append(soup.find('caption').text)
    keys =[i.text.replace("\xa0"," ") for i in soup.find('tr').find_all('th')]
    if(soup.find('caption')):
        keys.insert(0,soup.find('caption').text)
    vals = []
    for i in soup.find('tr').find_all('td'):
        if(i.parent.find('th')):
            result = [val.text.strip().replace("\n", "").replace("\t", "") for val in i.find_all('li')]
            if not result:
                if(i.find('br')):
                    for x in i.findAll('br'):
                        x.replace_with(',')
#                 print(i.text)
                    result = i.text.split(',')
                if "â€“" in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("â€“")]
                elif " to " in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("to")]
                else:
                    result = i.text.strip().replace("\n", "").replace("\t", "")
            vals.append(result)
    title = keys[0]
    dictionary = dict(zip(keys[1:], vals))
    dictionary["Title"] = title
    dictionary["Tablename"] = filename.split(".")[0]
    return dictionary





def get_Table_Title():
    d = {}
    tb = []
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            tb.append(dictionary['Tablename'])
            if("Title" in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Title'])
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(dictionary['Title'])
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return d,tb





N,T = get_Table_Title()
# T





'''
d1 : dict for that table
univ : list of a set
df : dataframe of Born/Death to get the table name
sel: selection bit
it : choose table name from the dataframe
'''
def FakeDICT(tb,dn,univ,di,it,sel=0,subNone = False): # selection bit selects whethet to substitute/delete/add
    d1 = di
    univ = list(univ)
    if(sel==0): # add
        if(d1[tb[it]][0]==None):
            d1[tb[it]]=[]
        ulimit = min(2,len(di[tb[it]])+1) # choose an upper limit of how many to add
        n_add = ulimit
        if(ulimit>1):
            n_add = random.randint(1,ulimit)
        add = random.sample(list(set(univ)-set(d1[tb[it]])),n_add)
        d1[tb[it]] =  list(set(d1[tb[it]]).union(set(add)))
        return d1
    elif(sel==1): 
        if(len(di[tb[it]])>0 and di[tb[it]][0] != None):
            if(len(di[tb[it]])>1):
                keep = random.sample(d1[tb[it]],1)
                ulimit = min(len(list(set(univ)-set(d1[tb[it]]))),len(d1[tb[it]])-1)
                substitute = random.sample(list(set(univ)-set(d1[tb[it]])),ulimit)
            else:
                keep=[]
                substitute = random.sample(list(set(univ)-set(d1[tb[it]])),len(d1[tb[it]]))
            d1[tb[it]] =  list(set(substitute).union(set(keep)))
        elif(len(di[tb[it]])>0):
            possible_sub = random.sample(list(set(univ)-set(d1[tb[it]])),1)
            for i in range(6): # Probability that none is chose = 1/7
                possible_sub.append(random.sample(list(set(univ)-set(d1[tb[it]])),1)[0])
            possible_sub.append(None)
            sub = random.sample(possible_sub,1)
            d1[tb[it]][random.randint(0,len(d1[tb[it]])-1)] = sub[0]
        return d1
    elif(sel==2): # delete nd : for size = 1
        if(len(di[tb[it]])>1 and di[tb[it]][0] != None):
            llimit = max(1,len(d1[tb[it]])-1)
            keep = random.sample(d1[tb[it]], random.randint(1,llimit) ) 
            d1[tb[it]] = keep
        return d1
    
    return None





def get_Type(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Type"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get_Type(T,N,True)[0]





def get_Observed_by(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Observed by"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get_Observed_by(T,N,True)[0]





def get_Frequency(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Frequency"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get_Frequency(T,N,True)[1]





def get_Celebrations(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Celebrations"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get_Celebrations(T,N,True)[1]





def get_Significance(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Significance"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            if(len(dictionary[k][i])>0):
                                u.add(dictionary[k][i])
                                d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get_Significance(T,N,True)[1]





def get_Observances(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Observances"
    for n in range(35):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getObv()[1]





def get_Date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Date"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip(".").replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip(".").replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getD()[1]





def get_Related_to(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Related to"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip("."))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip("."))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getRt()[1]





def get_Also_called(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Also called"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip(".").replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip(".").replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getAs()[1]





def get_Official_name(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Official name"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\u200e",""))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\u200e",""))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if(len(dictionary[k].split(",")[i])>0):
                            u.add(dictionary[k].split(",")[i].strip().strip(".").replace("\u200e",""))
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip().strip(".").replace("\u200e",""))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getOn()[1]





def get_Begins(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Begins"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip())
                    d[dictionary['Tablename']].append(dictionary[k].strip())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getBg()[1]





def get_Ends(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Ends"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip())
                    d[dictionary['Tablename']].append(dictionary[k].strip())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# getEn()[1]





def get_2021_date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "2021 date"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip().replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].strip().replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get21()[1]





def get_2020_date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "2020 date"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip().replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].strip().replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get20()[1]





def get_2019_date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "2019 date"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip().replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].strip().replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d





# get19()[1]





def get_2018_date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "2018 date"
    for n in range(35):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(len(dictionary[k][i])>0):
                            u.add(dictionary[k][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k].split(","))):
                    u.add(dictionary[k].strip().replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].strip().replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(35): # for getting all the fakes in one go
            sel = random.sample(getfa["Fest_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d





# get18()[1]


# #### Dictionary of all extracted data from html/json :




def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Type","Observed_by","Frequency","Celebrations","Significance","Observances"
                      ,"Date","Related_to","Also_called","Official_name","Begins","Ends"
                     ,"2021_date","2020_date","2019_date","2018_date"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data
# F is the Extracted_data[key]


# #### Sentences and premises generator :




def TypeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    length = len(di[tb[it]])
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" is of "+All+" type"
                  , All+(" are" if length>1 else " is")+" the type(s) "+Nm+" festival"]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is a "+All+" festival" )
                ts.append( "This festival is of more than "+str(random.randint(0,length-1))+" characteristics" )
                ts.append( "This festival is of less than "+str(random.randint(length+1,length+5))+" characteristics" )
                ts.append( Nm+" is a "+random.sample(di[tb[it]],1)[0]+" festival" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" is a "+All+" festival" )
                ts.append( "This festival is of less than "+str(random.randint(0,length-1))+" characteristics" )
                ts.append( "This festival is of more than "+str(random.randint(length+1,length+5))+" characteristics" )
                ts.append( Nm+" is a "+random.sample(NT,1)[0]+" festival" )
        else:
            ts.append(None)
        
        return ts





# TypeSent(T,N,get_Data()["Type"],2,False,True)





def Observed_bySent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The festival is observed by "+All
                  , All+" observe "+Nm+" festival"]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is celebrated by "+All )
                ts.append( Nm+" is celebrated by more than "+str(random.randint(0,length-1))+" groups" )
                ts.append( Nm+" is celebrated by less than "+str(random.randint(length+1,length+5))+" groups" )
                ts.append( Nm+" is celebrated by "+("single" if length==1 else "multiple")+" groups" )
                ts.append( Nm+" celebrate "+random.sample(di[tb[it]],1)[0]+" festival" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" is celebrated by "+All )
                ts.append( Nm+" is celebrated by more than "+str(random.randint(0,length-1))+" groups" )
                ts.append( Nm+" is celebrated by less than "+str(random.randint(length+1,length+5))+" groups" )
                ts.append( Nm+" is celebrated by "+("single" if length==1 else "multiple")+" groups" )
                ts.append( Nm+" celebrate "+random.sample(NT,1)[0]+" festival" )
                
        else:
            ts.append(None)
        
        return ts





# ObySent(T,N,getOby()[1],getOby()[0],0)





def FrequencySent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The frequency of this festival is "+All
                  , All+" is the frequency of this festival"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is a "+All+" festival" )
                if(re.findall("annual",All)):
                    ts.append( Nm+" is celebrated "+All+"ly" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append( Nm+" is a "+All+" festival" )
                if(re.findall("annual",All)):
                    syn = [" every day"," every month"," weekly"," every Sunday"," bimonthly"]
                    ts.append( Nm+" is celebrated"+random.sample(syn,1)[0] )
                
        else:
            ts.append(None)
        
        return ts





# FSent(T,N,getF()[1],getF()[0],0,False)





def CelebrationsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The festival involves celebrating "+All
                  , All+" are the celebrations of this festival" ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The festival involves "+random.sample(di[tb[it]],1)[0] )
                ts.append( "The festival involves more than "+str(random.randint(0,length-1))+" rituals" )
                ts.append( "The festival involves less than "+str(random.randint(length+1,length+5))+" rituals" )
                ts.append( "There are "+str(length)+" rituals in this festival" )
                ts.append( Nm+" is celebrated by "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "The festival involves "+random.sample(NT,1)[0] )
                ts.append( "The festival involves less than "+str(random.randint(0,length))+" rituals" )
                ts.append( "The festival involves more than "+str(random.randint(length+1,length+5))+" rituals" )
                ts.append( "There are "+str(random.randint(length+1,length+5))+" rituals in this festival" )
                ts.append( Nm+" is celebrated by "+All )
                
        else:
            ts.append(None)
        
        return ts





# CSent(T,N,getC()[1],getC()[0],1)





def SignificanceSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The significance of "+Nm+" festival are "+All
                  , All+" are the significance of the "+Nm+" festival" 
                  , "Because of "+All+" the festival "+Nm+" is observed" ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The festival is celebrated because "+All )
                ts.append( "The festival "+Nm+" is celebrated to acknowledge "+random.sample(di[tb[it]],1)[0] )
                ts.append( "The festival is celebrated to mark "+All )
                ts.append( "The festival is observed because of "+random.sample(di[tb[it]],1)[0] )
                ts.append( "The festival "+Nm+" is celebrated due to "+str(length)+" reasons" )
                ts.append( "The festival is celebrated because of more than "+str(random.randint(0,length-1))+" reasons" )
                ts.append( "The festival is celebrated because of less than "+str(random.randint(length+1,length+5))+" reasons" )
                ts.append( "The festival is celebrated because of "+("single reason" if length==1 else "multiple reasons") )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "The festival is celebrated because "+All )
                ts.append( "The festival "+Nm+" is celebrated to acknowledge "+random.sample(NT,1)[0] )
                ts.append( "The festival is celebrated to mark "+All )
                ts.append( "The festival is observed because of "+random.sample(NT,1)[0] )
                ts.append( "The festival "+Nm+" is celebrated due to "+str(random.randint(length+1,length+6))+" reasons" )
                ts.append( "The festival is celebrated because of less than "+str(random.randint(0,length))+" reasons" )
                ts.append( "The festival is celebrated because of more than "+str(random.randint(length,length+5))+" reasons" )
                ts.append( "The festival is celebrated because of "+("single reason" if length!=1 else "multiple reasons") )
                
        else:
            ts.append(None)
        
        return ts





# SSent(T,N,getS()[1],getS()[0],1,False)





def ObservancesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" rituals are observed in this festival"
                  , All+" are the observances in "+Nm ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is celebrated by "+random.sample(di[tb[it]],1)[0] )
                ts.append( All+" are observed in "+Nm )
                ts.append( Nm+" is celebrated by more than "+str(random.randint(0,length-1))+" rituals" )
                ts.append( Nm+" is celebrated by less than "+str(random.randint(length+1,length+5))+" rituals" )
                ts.append( Nm+" is observed by celebrating "+("single ritual" if length==1 else "multiple rituals") )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" is celebrated by "+random.sample(NT,1)[0] )
                ts.append( All+" are observed in "+Nm )
                ts.append( Nm+" is celebrated by less than "+str(random.randint(0,length))+" rituals" )
                ts.append( Nm+" is celebrated by more than "+str(random.randint(length,length+5))+" rituals" )
                ts.append( Nm+" is observed by celebrating "+("single ritual" if length!=1 else "multiple rituals") )
                
        else:
            ts.append(None)
        
        return ts





# ObvSent(T,N,getObv()[1],getObv()[0],0,False)





def DateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is when "+Nm+" is celebrated" 
                  , "On "+All+", "+Nm+" is celebrated" ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The festival is celebrated on "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "The festival is celebrated on "+",".join(random.sample(NT,random.randint(1,len(NT)))) )
                
        else:
            ts.append(None)
            
        return ts





# DSent(T,N,getD()[1],getD()[0],0,False)





def Related_toSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" is related to "+All
                  , All+" is related to "+Nm ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is similar to "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( random.sample(di[tb[it]],1)[0]+" is similar to "+Nm )
                ts.append( "The festival is similar to "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+" is celebrated in line with "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+" is similar to more than "+str(random.randint(0,length-1))+" festivals" )
                ts.append( Nm+" is similar to less than "+str(random.randint(length+1,length+5))+" festivals" )
                ts.append( Nm+" is similar to "+("single festival" if length==1 else "multiple festivals") )
                ts.append( Nm+" and "+random.sample(di[tb[it]],1)[0]+" are similar" )
                ts.append( "Following festivals "+All+" are similar to each other" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ','.join(NT)
                ts.append( Nm+" is similar to "+",".join(random.sample(NT,random.randint(1,len(NT)))) )
                ts.append( random.sample(NT,1)[0]+" is similar to "+Nm )
                ts.append( "The festival is similar to "+",".join(random.sample(NT,random.randint(1,len(NT)))) )
                ts.append( Nm+" is celebrated in line with "+",".join(random.sample(NT,random.randint(1,len(NT)))) )
                ts.append( Nm+" is similar to less than "+str(random.randint(0,length))+" festivals" )
                ts.append( Nm+" is similar to more than "+str(random.randint(length,length+5))+" festivals" )
                ts.append( Nm+" is similar to "+("single festival" if length!=1 else "multiple festivals") )
                ts.append( Nm+" and "+random.sample(NT,1)[0]+" are similar" )
                ts.append( "Following festivals "+All+" are similar to each other" )
                
        else:
            ts.append(None)
        
        return ts





# RtSent(T,N,getRt()[1],getRt()[0],0,False)





def Also_calledSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" is also called "+All
                  , All+" is also called "+Nm ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The festival is also called as "+All )
                ts.append( "There is at least one more name of "+Nm+" festival" )
                ts.append( Nm+" is also known as "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                syn = [ " alternate "," other name " ]
                ts.append( Nm+" is the"+random.sample(syn,1)[0]+"of "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+" is known by more than "+str(random.randint(0,length-1))+" names" )
                ts.append( Nm+" is known by less than "+str(random.randint(length+1,length+5))+" names" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ','.join(NT)
                ts.append( "The festival is also called as "+All )
                ts.append( "There is at least one more name of "+Nm+" festival" )
                ts.append( Nm+" is also known as "+",".join(random.sample(NT,random.randint(1,len(NT)))) )
                syn = [ " alternate "," other name " ]
                ts.append( Nm+" is the"+random.sample(syn,1)[0]+"of "+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+" is known by less than "+str(random.randint(0,length))+" names" )
                ts.append( Nm+" is known by more than "+str(random.randint(length,length+5))+" names" )
        else:
            ts.append(None)
        
        return ts





# AsSent(T,N,getAs()[1],getAs()[0],0,False)





def Official_nameSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The official name of the festival "+Nm+" is "+All
                  , "The common name of the festival "+All+" is "+Nm ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" is the primary name of the festival" )
                ts.append( Nm+" is also known by "+All )
                ts.append( All+" is also known by "+Nm )
                syn = [ " alternate "," other name " ]
                ts.append( Nm+" is the"+random.sample(syn,1)[0]+"of "+All )
                ts.append( "The festival "+Nm+" is also called as "+All )
                ts.append( "There is at least one more name of "+random.sample([Nm,All],1)[0]+" festival" )
                ts.append( "The common name of "+All+" is "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append( All+" is the primary name of the festival" )
                ts.append( Nm+" is also known by "+All )
                ts.append( All+" is also known by "+Nm )
                syn = [ " alternate "," other name " ]
                ts.append( Nm+" is the"+random.sample(syn,1)[0]+"of "+All )
                ts.append( "The festival "+Nm+" is also called as "+All )
                ts.append( "There is at least one more name of "+random.sample([All],1)[0]+" festival" )
                ts.append( "The common name of "+All+" is "+Nm )
                
        else:
            ts.append(None)
            
        return ts





# OnSent(T,N,getOn()[1],getOn()[0],0,False)





def BeginsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" start"," initiate"]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" begins on "+All
                  , All+" is when the festival begins"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is"+random.sample(syn,1)[0]+"ed on "+All )
                ts.append( Nm+random.sample(syn,1)[0]+"s at "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" is"+random.sample(syn,1)[0]+"ed on "+All )
                ts.append( Nm+random.sample(syn,1)[0]+"s at "+All )
                
        else:
            ts.append(None)
            
        return ts





# BgSent(T,N,getBg()[1],getBg()[0],3)





def EndsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [ " goes on "," runs " ]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" ends on "+All
                  , All+" is when this festival ends " ]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+random.sample(syn,1)[0]+"till "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+random.sample(syn,1)[0]+"till "+All )
                
        else:
            ts.append(None)
            
        return ts





# EnSent(T,N,getEn()[1],getEn()[0],3,False)





# give the year to use it for example 21,20,19,18
def _2021_dateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The 2021 date of the festival was "+All
                  , Nm+" 2021 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" was celebrated on "+All+" in "+str(2021) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" was celebrated on "+All+" in "+str(2021) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
        else:
            ts.append(None)
            
        return ts





# Y2021Sent(2021,T,N,get2021()[1],get2021()[0],6)





def _2020_dateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The 2020 date of the festival was "+All
                  , Nm+" 2020 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" was celebrated on "+All+" in "+str(2020) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" was celebrated on "+All+" in "+str(2020) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
        else:
            ts.append(None)
            
        return ts





def _2019_dateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The 2019 date of the festival was "+All
                  , Nm+" 2019 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" was celebrated on "+All+" in "+str(2019) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" was celebrated on "+All+" in "+str(2019) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
        else:
            ts.append(None)
            
        return ts





def _2018_dateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
#     syn = [" creators "," founding fathers "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The 2018 date of the festival was "+All
                  , Nm+" 2018 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" was celebrated on "+All+" in "+str(2018) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( Nm+" was celebrated on "+All+" in "+str(2018) )
                ts.append( Nm+" was celebrated on different date in different year" )
                
        else:
            ts.append(None)
            
        return ts





def multi_row1(tb,dn,F,it,tval=True):
    
    Nm = dn[tb[it]][0]
    
    def Y1_2(t1,t2,tval):
        
        f1 = F[str(t1)+"_date"]
        f2 = F[str(t2)+"_date"]
        u1,y1 = f1
        u2,y2 = f2
        if(y1[tb[it]][0]!=None and y2[tb[it]][0]!=None):
            if(tval):
                Al1 = ",".join(y1[tb[it]])
                Al2 = ",".join(y2[tb[it]])
            else:
                n1 = random.sample(list(set(u1)-set(y1[tb[it]])),1)
                n2 = random.sample(list(set(u2)-set(y2[tb[it]])),1)
                Al1 = ",".join(n1)
                Al2 = ",".join(n2)
                
            return (Nm+" was celebrated on "+Al1+" in "+str(t1)+" and on "+Al2+" in "+str(t2))
        else:
            
            return None
    
    ts = {}
    if(tval):
        for i in [2018,2019,2020]:
            for j in [2019,2020,2021]:
                if(Y1_2(i,j,tval)!=None and i!=j):
                    ts[str(i)+"_date"+","+str(j)+"_date"]=[]
                    ts[str(i)+"_date"+","+str(j)+"_date"].append(Y1_2(i,j,tval))
                    
    else:
        for i in [2018,2019,2020]:
            for j in [2019,2020,2021]:
                if(Y1_2(i,j,tval)!=None and i!=j):
                    ts[str(i)+"_date"+","+str(j)+"_date"]=[]
                    ts[str(i)+"_date"+","+str(j)+"_date"].append(Y1_2(i,j,tval))
        
    return ts





# multi_row1(T,N,get_Data(),0,False)





def multi_row2(tb,dn,F,it,tval=True):
    Uo,O = F["Official_name"]
    Ua,A = F["Also_called"]
    
    
    ts = {}
    if(tval):
        if(O[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Official_name,Also_called"] = []
            Al1 = ",".join(random.sample(O[tb[it]],1))
            Al2 = ",".join(random.sample(A[tb[it]],1))
            ts["Official_name,Also_called"].append( Al1+" is also called "+Al2 )
            ts["Official_name,Also_called"].append( Al2+" is a common name of "+Al1 )
        
        
    else:
        if(O[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Official_name,Also_called"] = []
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Ua)-set(O[tb[it]])),1))
            ts["Official_name,Also_called"].append( Al1+" is also called "+Al2 )
            ts["Official_name,Also_called"].append( Al2+" is a common name of "+Al1 )
        
    return ts





# multi_row2(T,N,get_Data(),0,False)





def multi_row3(tb,dn,F,it,tval=True):
    Uo,O = F["Observances"]
    Us,S = F["Significance"]
    Uc,C = F["Celebrations"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(O[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Observances,Significance"] = []
            Al1 = ",".join(random.sample(O[tb[it]],1))
            Al2 = ",".join(random.sample(S[tb[it]],1))
            ts["Observances,Significance"].append( Al1+" is observed to signify "+Al2 )
            ts["Observances,Significance"].append( Al2+" is signified by "+Al1 )
            
        if(C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Celebrations,Significance"]=[]
            Al1 = ",".join(random.sample(C[tb[it]],1))
            Al2 = ",".join(random.sample(S[tb[it]],1))
            ts["Celebrations,Significance"].append( Al1+" is celebrated to signify "+Al2 )
            ts["Celebrations,Significance"].append( Al2+" is signified by "+Al1 )
        
        
    else:
        if(O[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Observances,Significance"] = []
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Us)-set(S[tb[it]])),1))
            ts["Observances,Significance"].append( Al1+" is observed to signify "+Al2 )
            ts["Observances,Significance"].append( Al2+" is signified by "+Al1 )
            
        if(C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Celebrations,Significance"]=[]
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Us)-set(S[tb[it]])),1))
            ts["Celebrations,Significance"].append( Al1+" is celebrated to signify "+Al2 )
            ts["Celebrations,Significance"].append( Al2+" is signified by "+Al1 )
        
    return ts





# multi_row3(T,N,get_Data(),5,False)













