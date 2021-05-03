#!/usr/bin/env python
# coding: utf-8

# In[10]:


# %run Psn_tr1.ipynb


# In[41]:


def GenresSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            AllGen = ', '.join(di[tb[it]])
            ps1 = [ "This person is singing in the genres "+AllGen
                   , AllGen+" these are the genres in which "+Nm+" sings"
                   , Nm+" has songs in the genres "+AllGen ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                AllGen = ', '.join(di[tb[it]])
                ts.append(Nm + " sings in the genres of " + AllGen)
                ts.append(Nm + " sings in the genre " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " sings in " + str(len(di[tb[it]])) + " genres")
                ts.append(Nm + " sings in more than " + str(random.randint(0,len(di[tb[it]])-1)))
                ts.append(Nm + " sings in less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5)))
                ts.append("The person plays "+random.sample(di[tb[it]],1)[0]+" music")
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,7))
                AllGen = ', '.join(NT)
                ts.append(Nm + " sings in the genres of " + AllGen)
                ts.append(Nm + " sings in the genre " + random.sample(NT,1)[0])
                ts.append(Nm + " sings in " + str(len(NT)) + " genres")
                ts.append(Nm + " sings in less than " + str(random.randint(0,len(NT)-1)))
                ts.append(Nm + " sings in more than " + str(random.randint(len(NT)+1,len(NT)+5)))
                ts.append("The person plays "+random.sample(NT,1)[0]+" music")
            else:
                ts.append(None)

        return ts


# In[42]:


# GenSent(T,N,getG(300),5,False)


# In[43]:


def EducationSent(tb,dn,F,it,tval=True,prem=False):
    A = F[2]
    E = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(E[tb[it]][0] != None):
            ps1 = [ Nm+" studied at "+random.sample(E[tb[it]],1)[0]
                    ,"This person studied in "+random.sample(E[tb[it]],1)[0]
                    ,random.sample(E[tb[it]],1)[0]+" is where "+Nm+" studied" ]
        else:
            ps1 = [None]
        return ps1
        if(A[tb[it]][0] != None):
            ps2 = [ Nm+" earned his degree from "+random.sample(E[tb[it]],1)[0]
                    ,"This person is a graduate of "+random.sample(E[tb[it]],1)[0]
                    ,random.sample(E[tb[it]],1)[0]+" is where "+Nm+" graduated from" ]
        else:
            ps2 = [None]
        
        return ps2
        
    else:
        if(tval):
            if(E[tb[it]][0] != None):
                ts1 = Nm + " studied from " + random.sample(E[tb[it]],1)[0]
            else:
                ts1 = None
            return [ts1]
            if(A[tb[it]][0] != None):
                ts2 = Nm + " graduated from " + random.sample(A[tb[it]],1)[0]
            else:
                ts2 = None
            return [ts2]
        else:
            if(E[tb[it]][0] != None):
                ts1 = Nm + " studied from " + random.sample(list(set(univ)-set(E[tb[it]])),1)[0]
            else:
                ts1 = None
            return [ts1]
            if(A[tb[it]][0] != None):
                ts2 = Nm + " graduated from " + random.sample(list(set(univ)-set(A[tb[it]])),1)[0]
            else:
                ts2 = None
            return [ts2]


# In[44]:


# EdSent(T,N,diA,diE,UE,27,False,True)


# In[45]:


def LabelsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            AllGen = ', '.join(di[tb[it]])
            ps1 = [AllGen+" are the labels in which this person sings"
                  ,"Songs by "+Nm+" are in "+AllGen+" labels"
                  , Nm+" sings in "+AllGen+" labels"]
        else:
            ps1 = [None]
            
        return ps1    
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                AllGen = ', '.join(di[tb[it]])
                ts.append(Nm + " is associated with the labels " + AllGen)
                ts.append(Nm + " is associated with label " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " is associate with " + str(len(di[tb[it]])) + " labels")
                ts.append(Nm + " is associate with more than " + str(random.randint(0,len(di[tb[it]])-1)) + " labels")
                ts.append(Nm + " is associate with less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+ " labels")
                ts.append("The person works with "+random.sample(di[tb[it]],1)[0])
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,7))
                AllGen = ', '.join(NT)
                ts.append(Nm + " is associate with the labels " + AllGen)
                ts.append(Nm + " is associate with label " + random.sample(NT,1)[0])
                ts.append(Nm + " is associate with " + str(len(NT)) + " labels")
                ts.append(Nm + " is associate with less than " + str(random.randint(0,len(NT)-1)) + " labels")
                ts.append(Nm + " is associate with more than " + str(random.randint(len(NT)+1,len(NT)+5))+ " labels")
                ts.append("The person works with "+random.sample(NT,1)[0])
            else:
                ts.append(None)

        return ts


# In[46]:


# LSent(T,N,getL(300),5,True)


# In[47]:


def WebsiteSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    alldom = ['.com', '.co.fr', '.co.in']
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ di[tb[it]][0]+" is this person's website"
                   ,"This person has a website named "+di[tb[it]][0]
                  , di[tb[it]][0]+" is "+Nm+"'s website"]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ts.append(Nm + " has the website " + di[tb[it]][0])
                ts.append("The website has domain name "+dom)
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ndom = random.sample(list(set(alldom)-set(dom)),1)[0]
                ts.append(Nm + " has the website " + random.sample(list(set(univ)-set(di[tb[it]])),1)[0]) 
                ts.append("The website has domain name "+ndom)
            else:
                ts.append(None)
            
        return ts


# In[48]:


# WSent(T,N,getW(T,N,0),1)


# In[49]:


def ConvictionSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ", ".join(di[tb[it]])
            ps1 = [ All+" are the crimes this person is convicted for"
                   , "The crimes that "+Nm+" is convicted for are "+All
                   , "The charges against this person are "+All]
        else:
            ps1 = [None]
            
        return ps1
        
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                All = ", ".join(di[tb[it]])
                ts.append(Nm + " has been convicted for " + All)
                ts.append(Nm + " was convicted for " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " was convicted for " + str(len(di[tb[it]])) + " charges")
                ts.append(Nm + " was convicted for more than " + str(random.randint(0,len(di[tb[it]]))))
                ts.append(Nm + " was convicted for less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+7)))
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,5))
                All = ", ".join(NT)
                ts.append(Nm + " has been convicted for " + All)
                ts.append(Nm + " was convicted for " + random.sample(NT,1)[0])
                ts.append(Nm + " was convicted for " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+6)) + " charges")
                ts.append(Nm + " was convicted for less than " + str(random.randint(0,len(di[tb[it]]))))
                ts.append(Nm + " was convicted for more than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+7)))
            else:
                ts.append(None)      

        return ts


# In[50]:


# CRSent(T,N,getCR(300),2,False)


# # Second part starts here

# In[51]:


def get_Institutions(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Institutions"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[52]:


# get_Institutions(T,N,True)[1]


# In[53]:


def get_Fields(T,N,it,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Fields"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[54]:


# getFl(300)[1]


# In[55]:


def get_Doctoral_students(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Doctoral students"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[56]:


# getStD(300)[1]


# In[57]:


def get_Awards(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Awards"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(not (re.findall(" list",dictionary[k][i]) or re.findall("List ",dictionary[k][i])) ):
                            u.add(dictionary[k][i].replace(",,",",").strip())
                            d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                        else:
                            d[dictionary['Tablename']].append(None)
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        if(not (re.findall(" list",dictionary[k].split(",")[i]) or re.findall(".*List ",dictionary[k].split(",")[i])) ):
                            u.add(dictionary[k].split(",")[i].strip())
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                        else:
                            d[dictionary['Tablename']].append(None)
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[58]:


# getAw(300)[1]


# In[59]:


def get_Relatives(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Relatives"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[60]:


# getRel(300)[1]


# In[61]:


def get_Resting_place(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Resting place"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[62]:


# getRP(300)[1]


# In[63]:


def get_Parents(T,N,fake=False,sel=0):
    u1 = set([])
    u2 = set([])
    d = {}
    k1 = "Parent(s)"
    k2 = "Parents"
    for n in range(700):
        if(int(Ptab[n][1:]) <= 2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u1.add(dictionary[k1][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace(",,",",").strip())
                else:
                    dictionary[k1] = dictionary[k1].replace(",,",",")
                    dictionary[k1] = dictionary[k1].replace(" and ",",")
                    for i in range(len(dictionary[k1].split(","))):
                        u1.add(dictionary[k1].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k1].split(",")[i].strip())
                        
            if(k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u1.add(dictionary[k2][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k2][i].replace(",,",",").strip())
                else:
                    dictionary[k2] = dictionary[k2].replace(",,",",")
                    dictionary[k2] = dictionary[k2].replace(" and ",",")
                    for i in range(len(dictionary[k2].split(","))):
                        u1.add(dictionary[k2].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i].strip())

            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Parents"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u1,d,it,sel,subNone = False)
        
    return list(u1),d


# In[64]:


# getPrnt(300)[1]


# In[65]:


def get_Instruments(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Instruments"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[66]:


# getIns(300)[1]


# In[67]:


def get_Residence(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Residence"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[68]:


# get_Residence(T,N,True)[1]


# In[69]:


def get_Years_active(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Years active"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                r = []
                if(type(dictionary[k]) == list):
                    X = re.findall("[0-9][0-9]+"," ".join(dictionary[k]).replace("\xa0","") )
                    for i in range(len(X)):
                        if(len(X[i])>2):
                            r.append(X[i])
                        else:
                            r.append(X[i-1][:2]+X[i])
                        
                    X = re.findall("present"," ".join(dictionary[k]).replace("\xa0","") )
                    if(X or len(r)%2!=0):
                        store = r[-1]
                        r = []
                        r.append(store)
                        r.append('present')
                else:
                    dictionary[k].replace(",,",",")
                    X = re.findall("[0-9][0-9]+",dictionary[k].replace("\xa0","") )
                    for i in range(len(X)):
                        if(len(X[i])>2):
                            r.append(X[i])
                        else:
                            r.append(X[i-1][:2]+X[i])
                    X = re.findall("present",dictionary[k].replace("\xa0","") )
                    if(X or len(r)%2!=0):
                        store = r[-1]
                        r = []
                        r.append(store)
                        r.append('present')
                        
                for i in range(len(r)):
                    d[dictionary['Tablename']].append(r[i])
                    u.add(r[i])
            if(k not in dictionary.keys() or len(d[dictionary['Tablename']])<1):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel,subNone=False)
            if(len(d[T[it]])>1 and d[T[it]][0] == "present" and d[T[it]][1]=="present"):
                d[T[it]][0] = str(random.randint(1965,1975))
            elif(len(d[T[it]])==1 and d[T[it]][0] == "present"):
                d[T[it]][0] = str(random.randint(1965,1975))
            if(d[T[it]][0]!=None and d[T[it]][0]!="present" and d[T[it]][0]>d[T[it]][-1]):
                temp = d[T[it]][0]
                d[T[it]][0] = d[T[it]][-1]
                d[T[it]][-1] = temp
            elif(d[T[it]][0] == "present"):
                temp = d[T[it]][0]
                d[T[it]][0] = d[T[it]][-1]
                d[T[it]][-1] = temp

    return list(u),d


# In[70]:


# get_Years_active(T,N,True)[1]


# #### Sentences :

# In[71]:


def InstitutionsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" went to "," worked at "," employed at ",]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" are the institutions "+dn[tb[it]][0]+" worked at"
                   , "The person worked at "+All+" institutions" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ', '.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+All )
                ts.append( dn[tb[it]][0]+" was at "+random.sample(di[tb[it]],1)[0]+" at least once" )
                ts.append( dn[tb[it]][0]+" received salary from "+All )
                ts.append( dn[tb[it]][0]+" worked at more than "+str(random.randint(0,length-1))+" places" )
                ts.append( dn[tb[it]][0]+" worked at less than "+str(random.randint(length+1,length+5))+" places" )
                for i in range(len(di[tb[it]])):
                    if(re.findall("[Uu]niversity",di[tb[it]][i]) or re.findall("[Ii]nstitute",di[tb[it]][i]) or re.findall("[Cc]ollege",di[tb[it]][i]) ):
                        syn = [" studied "," taught at "]
                        ts.append(dn[tb[it]][0]+random.sample(syn,1)[0]+di[tb[it]][i])
                        syn = [" literate ", " educated "]
                        ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0])
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+All )
                ts.append( dn[tb[it]][0]+" was at "+random.sample(NT,1)[0]+" at least once" )
                ts.append( dn[tb[it]][0]+" received salary from "+All )
                ts.append( dn[tb[it]][0]+" worked at less than "+str(random.randint(0,length-1))+" places" )
                ts.append( dn[tb[it]][0]+" worked at more than "+str(random.randint(length+1,length+5))+" places" )
                for i in range(len(di[tb[it]])):
                    if(re.findall("[Uu]niversity",di[tb[it]][i]) or re.findall("[Ii]nstitute",di[tb[it]][i]) or re.findall("[Cc]ollege",di[tb[it]][i]) ):
                        syn = [" did not study at "]
                        ts.append(dn[tb[it]][0]+random.sample(syn,1)[0]+di[tb[it]][i])
                        syn = [" illiterate ", " not educated "]
                        ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0])
        else:
            ts.append(None)
        
        return ts


# In[72]:


# InSent(T,N,getIn(300),12,False)


# In[73]:


def FieldsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ dn[tb[it]][0]+" worked in "+All+" fields"
                  , All+" are the fields "+dn[tb[it]][0]+" worked in"
                  , "The person worked in "+All+" fields" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): # not finished
                All = ', '.join(di[tb[it]])
                syn = [" expert at "," educated in "," knowledgeable at "," worked in "," known for "]
                ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0]+All+" area")
                ts.append("At least one person"+random.sample(syn,1)[0]+random.sample(di[tb[it]],1)[0]+" field")
                syn = [" significant "," valuable "]
                ts.append(dn[tb[it]][0]+" made"+random.sample(syn,1)[0]+"contributions in "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                syn = [" engaged "," involved "]
                ts.append("The person"+random.sample(syn,1)[0]+"in "+All+" areas")
                ts.append("The person worked in "+("single area" if length==1 else "multiple areas"))
                ts.append(dn[tb[it]][0]+" worked at more than "+str(random.randint(0,length-1))+" places")
                ts.append(dn[tb[it]][0]+" worked at less than "+str(random.randint(length+1,length+5))+" places")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                syn = [" expert at "," educated in "," knowledgeable at "," worked in "," known for "]
                ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0]+All+" area")
                ts.append("At least one person"+random.sample(syn,1)[0]+random.sample(NT,1)[0]+" field")
                syn = [" significant "," valuable "]
                ts.append(dn[tb[it]][0]+" made"+random.sample(syn,1)[0]+"contributions in "+", ".join(random.sample(NT,random.randint(1,len(NT)))) )
                syn = [" engaged "," involved "]
                ts.append("The person"+random.sample(syn,1)[0]+"in "+All+" areas")
                ts.append("The person worked in "+("single area" if length!=1 else "multiple areas"))
                ts.append(dn[tb[it]][0]+" worked at less than "+str(random.randint(0,length-1))+" places")
                ts.append(dn[tb[it]][0]+" worked at more than "+str(random.randint(length+1,length+5))+" places")
        else:
            ts.append(None)
        
        return ts


# In[141]:


# FlSent(T,N,getFl(T,N,39),39,False)


# In[ ]:


# getFl(300)[1]


# In[ ]:


def Doctoral_studentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" were the doctoral students of "+dn[tb[it]][0]
                  , "The doctoral students of "+dn[tb[it]][0]+" are "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): # not finished
                All = ', '.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" was an advisor to "+", ".join(random.sample(di[tb[it]],random.randint(1,length))))
                syn = [" person "," professor "," faculty "," Ph.D. "]
                ts.append( "The"+random.sample(syn,1)[0]+"supervised "+All )
                ts.append( "The"+random.sample(syn,1)[0]+"mentored "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored at least "+str(random.randint(1,length)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored more than "+str(random.randint(0,length-1)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored less than "+str(random.randint(length+1,length+5)) )
                ts.append( dn[tb[it]][0]+" knows "+random.sample(di[tb[it]],1)[0] )
                ts.append( dn[tb[it]][0]+" met "+random.sample(di[tb[it]],1)[0]+" atleast once" )
                ts.append( dn[tb[it]][0]+" was the advisee of "+random.sample(di[tb[it]],1)[0] )
                ts.append( dn[tb[it]][0]+" awarded a degree to "+random.sample(di[tb[it]],1)[0] )
                ts.append( random.sample(di[tb[it]],1)[0]+" got a degree under "+dn[tb[it]][0] )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,5))
                nl = len(NT)
                All = ', '.join(NT)
                ts.append( dn[tb[it]][0]+" was an advisor to "+", ".join(random.sample(NT,random.randint(1,nl))))
                syn = [" person "," professor "," faculty "," Ph.D. "]
                ts.append( "The"+random.sample(syn,1)[0]+"supervised "+All )
                ts.append( "The"+random.sample(syn,1)[0]+"mentored "+", ".join(random.sample(NT,random.randint(1,nl))) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored at least "+str(random.randint(length+1,length+5)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored less than "+str(random.randint(0,length-1)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored more than "+str(random.randint(length+1,length+5)) )
                ts.append( dn[tb[it]][0]+" knows "+random.sample(NT,1)[0] )
                ts.append( dn[tb[it]][0]+" met "+random.sample(NT,1)[0]+" atleast once" )
                ts.append( dn[tb[it]][0]+" was the advisee of "+random.sample(NT,1)[0] )
                ts.append( dn[tb[it]][0]+" awarded a degree to "+random.sample(NT,1)[0] )
                ts.append( random.sample(NT,1)[0]+" got a degree under "+dn[tb[it]][0] )
        
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# StDSent(T,N,getStD(300),-12)


# In[ ]:


def AwardsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ "The person won "+All
                  , All+" was won by "+dn[tb[it]][0]
                  , All+" were the awards that "+di[tb[it]][0]+" won" ]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" won "+" was winner of "," was rewarded "]
                ts.append( Nm+random.sample(syn,1)[0]+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+random.sample(syn,1)[0]+str(length)+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" more than "+str(random.randint(0,length-1))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" less than "+str(random.randint(length+1,length+5))+" awards" )
                ts.append( ", ".join(random.sample(di[tb[it]],random.randint(1,length)))+" was given to "+Nm )
                ts.append( Nm+" was winner of "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" won "+" was winner of "," was rewarded "]
                ts.append( Nm+random.sample(syn,1)[0]+", ".join(random.sample(NT,random.randint(1,nl))) )
                ts.append( Nm+random.sample(syn,1)[0]+str(random.randint(length+1,length+5))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" less than "+str(random.randint(0,length-1))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" more than "+str(random.randint(length+1,length+5))+" awards" )
                ts.append( ", ".join(random.sample(NT,random.randint(1,nl)))+" was given to "+Nm )
                ts.append( Nm+" was winner of "+", ".join(random.sample(NT,random.randint(1,nl))) )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# AwSent(T,N,getAw(300),-12,True)


# In[ ]:


def RelativesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" are relatives of "+Nm
                  , Nm+" is related to "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ppl = []
                for s in di[tb[it]]:
                    if(re.findall("\(.+\)",s)):
                        relation = re.findall("\(.+\)",s)[0]
                        s = s.strip(relation)
                        ppl.append(s)
                        ts.append(s+" was "+relation.strip("(").strip(")")+" to "+Nm)
                    else:
                        ppl.append(s)
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" know each other" )
                ts.append( random.sample(ppl,1)[0]+" is connected to "+Nm+" by blood" )
                ts.append( random.sample(ppl,1)[0]+" is close to "+Nm )
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" connected by blood" )
                ts.append( Nm+" has more than "+str(random.randint(0,length-1))+" relatives" )
                ts.append( Nm+" has less than "+str(random.randint(length+1,length+5))+" relatives" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ', '.join(NT)
                nl = len(NT)
                ppl = []
                for s in NT:
                    if(re.findall("\(.+\)",s)):
                        relation = re.findall("\(.+\)",s)[0]
                        s = s.strip(relation)
                        ppl.append(s)
                        ts.append(s+" was "+relation.strip("(").strip(")")+" to "+Nm)
                    else:
                        ppl.append(s)
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" know each other" )
                ts.append( random.sample(ppl,1)[0]+" is connected to "+Nm+" by blood" )
                ts.append( random.sample(ppl,1)[0]+" is close to "+Nm )
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" connected by blood" )
                ts.append( Nm+" has less than "+str(random.randint(0,length-1))+" relatives" )
                ts.append( Nm+" has more than "+str(random.randint(length+1,length+5))+" relatives" )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# RelSent(T,N,getRel(300),6,False)


# In[ ]:


def Resting_placeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ "The resting place of "+Nm+" is "+All
                  , All+" is the resting place of the person"]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ts.append( Nm+" was buried at "+All )
                ts.append( "People paid last respect to person at "+All )
                ts.append( "The body of the person was last seen at "+All )
                syn = [" creamted "," buried "]
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"at "+All )
                ts.append("The person's body could be found at "+All )
                ts.append( All+" is a cemetery")
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ', '.join(NT)
                nl = len(NT)
                ts.append( Nm+" was buried at "+All )
                ts.append( "People paid last respect to person at "+All )
                ts.append( "The body of the person was last seen at "+All )
                syn = [" creamted "," buried "]
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"at "+All )
                ts.append("The person's body could be found at "+All )
                ts.append( All+" is a cemetery")
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# RPSent(T,N,getRP(300),20)


# In[74]:


def ParentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" were the parents of "+Nm
                  , "The parents of "+Nm+" are "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ts.append( random.sample(di[tb[it]],1)[0]+" is a guardian of "+Nm )
                if(re.findall("\([FfMm][ao]ther\)",All)):
                    if(re.findall("\([Ff][a]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the father of "+Nm )
                    elif(re.findall("\([Mm][o]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][0].replace(r[0],"") )
                    if(length>1 and re.findall("\([Mm][o]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][1].replace(r[0],"") )
                    elif(length>1 and re.findall("\([Ff][a]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the father of "+Nm )
                ts.append( random.sample(di[tb[it]],1)[0]+" and "+Nm+" met at least once" )
                ts.append( Nm+" used to stay with "+All )
                ts.append( Nm+" was named by "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ', '.join(NT)
                nl = len(NT)
                ts.append( random.sample(NT,1)[0]+" is a guardian of "+Nm )
                if(re.findall("\([FfMm][ao]ther\)",", ".join(di[tb[it]])) and length>1):
                    if(re.findall("\([Ff][a]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][0].replace(r[0],"") )
                    elif(re.findall("\([Mm][o]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the father of "+Nm )
                    if(length>1 and re.findall("\([Mm][o]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the father of "+Nm )
                    elif(length>1 and re.findall("\([Ff][a]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][1].replace(r[0],"") )
                    ts.append( Nm+" was given birth by "+NT[0] )
                ts.append( random.sample(NT,1)[0]+" and "+Nm+" met at least once" )
                ts.append( Nm+" used to stay with "+All )
                ts.append( Nm+" was named by "+All )
                
        else:
            ts.append(None)
        
        return ts


# In[78]:


# ParentsSent(T,N,get_Parents(T,N),427)


# In[ ]:


def InstrumentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" instruments were played by "+Nm 
                  , Nm+" played "+All+" instruments" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" how to play "," can play "," used to play "]
                ts.append( Nm+"knows"+random.sample(syn,1)[0]+All )
                ts.append( "This person"+random.sample(syn,1)[0]+str(length)+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"more than "+str(random.randint(0,length-1))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"less than "+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( Nm+" played "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" did not play "+random.sample(list(set(univ)-set(di[tb[it]])),1)[0] )
                ts.append( Nm+" is an expert at playing "+random.sample(di[tb[it]],1)[0] )
                ts.append( "This person knew"+random.sample(syn,1)[0]+("single" if length==1 else "multiple")+" instrument" )
                ts.append( "This person can make melodious sounds from "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" how to play "," can play "," used to play "]
                ts.append( Nm+" knows"+random.sample(syn,1)[0]+All )
                ts.append( "This person"+random.sample(syn,1)[0]+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"less than "+str(random.randint(0,length-1))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"more than "+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( Nm+" did not play "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" played "+random.sample(list(set(univ)-set(di[tb[it]])),1)[0] )
                ts.append( Nm+" is an expert at playing "+random.sample(NT,1)[0] )
                ts.append( "This person knew"+random.sample(syn,1)[0]+("single" if length!=1 else "multiple")+" instrument" )
                ts.append( "This person can make melodious sounds from "+All )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# IntSent(T,N,getInt(300),5)


# In[ ]:


def ResidenceSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ Nm+" had a residence at "+All
                  , All+" is where "+Nm+" had a residence"
                  , "This person is resided at "+All]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" stayed at "," resided at "," lived at "," was atleast once at "]
                ts.append( Nm+random.sample(syn,1)[0]+ ", ".join(di[tb[it]][:random.randint(1,length)]) )
                syn = [" house "," apartment "]
                ts.append( "The person bought "+random.sample(syn,1)[0]+"at "+All )
                ts.append( "The person is known by someone at "+", ".join(di[tb[it]][:random.randint(1,length)]) )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" stayed at "," resided at "," lived at "," was atleast once at "]
                ts.append( Nm+random.sample(syn,1)[0]+ ", ".join(NT[:random.randint(1,nl)]) )
                syn = [" house "," apartment "]
                ts.append( "The person bought "+random.sample(syn,1)[0]+"at "+All )
                ts.append( "The person is known by someone at "+", ".join(NT[:random.randint(1,nl)]) )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# ResdSent(T,N,getResd(300),-10,False,True)


# In[ ]:


def Years_activeSent(tb,dn,F,it,tval=True,prem=False):
    # Note : Assuming present is 2020
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    y = []
    if(di[tb[it]][0] != None):
        for i in di[tb[it]]:
            x = re.findall("[0-9]+",i)
            if(len(x)>0):
                y.append(x[0])
            else:
                y.append("2020")
    if(prem):
        if(di[tb[it]][0] != None):
    #         All = ', '.join(di[tb[it]])
            ps1 = [ "This person was active from "+"-".join(y)
                  , "-".join(y)+" is when "+Nm+" was active"
                  , "The active years for "+Nm+" were from "+"-".join(y) ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): 
                All = ', '.join(di[tb[it]])
                if(length>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" worked for "+str(span)+" years" )
                    ts.append(Nm+" worked for more than "+str(random.randint(span-6,span-1))+" years")
                    ts.append(Nm+" worked for less than "+str(random.randint(span+2,span+10))+" years")
                    ts.append(Nm+" worked from "+"-".join(y))
                    ts.append(Nm+" started working in "+str(y[0]))
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                if(length>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" worked for "+str(random.randint(span+2,span+10))+" years")
                    ts.append(Nm+" worked for less than "+str(random.randint(span-6,span-1))+" years")
                    ts.append(Nm+" worked for more than "+str(random.randint(span+2,span+10))+" years")
                
                x = re.findall("[0-9]+",NT)
                if(len(x)>0):
                    ny = x[0]
                else:
                    ny = "2020"
                ts.append(Nm+" worked from "+"-".join([ny,str(random.randint(int(ny)+1,2021))]))
                ts.append(Nm+" started working in "+str(random.randint(int(y[0])+1,int(y[0])+10) ))
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# YASent(T,N,getYA(),51)


# In[ ]:


def multi_row3(tb,dn,F,it,tval=True):
    B = F["BDA"][0]
    Ur,R = F["Relatives"]
    Up,P = F["Parents"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(R[tb[it]][0]!=None and P[tb[it]][0]!=None):
            ts["Relatives,Parents"] = []
            Al1 = random.sample(R[tb[it]],1)[0].split("(")[0]
            Al2 = random.sample(P[tb[it]],1)[0].split("(")[0]
            ts["Relatives,Parents"].append(Al1+" is related to "+Al2)
            ts["Relatives,Parents"].append(Al2+" is related to "+Al1)
            
        if(B.isna().Born_Y[it]==False and P[tb[it]][0] != None):
            ts["Born,Parents"] = []
            Al1 = random.sample(P[tb[it]],1)[0].split("(")[0]
            y = int(B.Born_Y[it])
            ts["Born,Parents"].append(Al1+" was born before "+str(random.randint(y+1,y+5)) )
    else:
        if(R[tb[it]][0]!=None and P[tb[it]][0]!=None):
            ts["Relatives,Parents"] = []
            Al1 = random.sample(list(set(Ur)-set(R[tb[it]])),1)[0].split("(")[0]
            Al2 = random.sample(P[tb[it]],1)[0].split("(")[0]
            ts["Relatives,Parents"].append(Al1+" is related to "+Al2)
            ts["Relatives,Parents"].append(Al2+" is related to "+Al1)
            
        if(B.isna().Born_Y[it]==False and P[tb[it]][0] != None):
            ts["Born,Parents"] = []
            Al1 = random.sample(P[tb[it]],1)[0].split("(")[0]
            y = int(B.Born_Y[it])
            ts["Born,Parents"].append(Al1+" was born after "+str(random.randint(y+1,y+5)) )
        
    return ts


# In[53]:


# multi_row3(T,N,6)


# In[ ]:




