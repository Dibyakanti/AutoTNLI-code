import numpy as np
import pandas as pd
import re
import random
import sys
import json

# Address
category_map_address = "../wiki_data/table_categories modified.tsv"
tablesFolder = "../wiki_data/tables"
tablesFolderJson = "../wiki_data/json/"

# Needed across categories
category_map = pd.read_csv(category_map_address,sep="\t")

day_of_week = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

reverse_month_of_year = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}

month_of_year = {1: 'January',2: 'February',3: 'March',4: 'April',5: 'May',6: 'June',7: 'July',8: 'August',9: 'September',10: 'October',11: 'November',12: 'December'}

FakeDICT_helper = {
"Book":{"Publisher":[1],"Schedule":[1],"Format":[0,1,2],"Genre":[0,1,2],"Publication_date":[1],"No_of_issues":[1],"Main_character":[0,1,2],"Written_by":[0,1,2]},
"City":{"Elevation":[1],"Metro":[1],"Urban":[1],"City":[1],"Location":[1],"Government":[1],"Highest_elevation":[1],"Lowest_elevation":[1],"Land":[1],"Water":[1],"Demonym":[1],"Province":[1],"Mayor":[1],"Time_zone":[1],"Named_for":[1],"Area_code":[1],"Postal_code":[1],"Coordinates":[1],"Incorporated":[1],"Density":[1],"Urban_density":[1],"Metro_density":[1]},
"Festival":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],"Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],"2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"FoodnDrinks":{"Manufacturer":[1],"Country_of_origin":[0,1,2],"Variants_Flavour":[0,1,2],"Introduced":[1],"Related_products":[0,1,2],"Alcohol_by_volume":[1],"Website":[1],"Color":[0,1,2],"Main_ingredients":[0,1,2],"Type":[0,1,2]},
"Movie":{"Directed_by":[0,1,2],"Produced_by":[0,1,2],"Screenplay_by":[1],"Starring":[0,1,2],"Music_by":[0,1,2],"Cinematography":[1],"Edited_by":[0,1,2],"Productioncompany":[1],"Distributed_by":[0,1,2],"Release_date":[0,1,2],"Running_time":[1],"Country":[0,1,2],"Language":[0,1,2],"Budget":[1],"Box_office":[1]},
"Organization":{"Website":[1],"Headquarters":[1],"Founded":[1],"Industry":[0,1,2],"Key_people":[0,1,2],"Products":[0,1,2],"Number_of_employees":[1],"Traded_as":[0,1,2],"Founder":[0,1,2],"Area_served":[0,1,2],"Type":[1],"Subsidiaries":[0,1,2],"Parent":[1],"Owner":[1],"Predecessor":[1]},
"Paint":{"Artist":[1],"Year":[1],"Medium":[1],"Dimensions":[1],"Location":[1]},
"Person":{"Spouse":[1],"Occupation":[0,1,2],"Education":[1],"Children":[1],"Genres":[0,1,2],"Labels":[0,1,2],"Website":[1],"Conviction":[0,1,2],"Institutions":[1],"Fields":[0,1,2],"Doctoral_students":[0,1,2],"Awards":[0,1,2],"Relatives":[0,1],"Resting_place":[1],"Parents":[1],"Instruments":[0,1,2],"Residence":[1],"Years_active":[1]},
"SportsnEvents":{"Venue":[0,1,2],"Date":[1],"Competitors":[0,1,2],"Teams":[1],"No_of_events":[1],"Established":[1],"Official_site":[1]},
"University":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],"Motto":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],"Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],"Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]}
}


# Necessary functions
def FakeDICT(tb,dn,univ,di,it,sel=0,subNone = False):
    '''
    d1 : dict for that table
    univ : list of a set
    df : dataframe of Born/Death to get the table name
    sel: selection bit to select whether to 0 : add / 1 : substitute / 2 : delete
    it : choose table name from the dataframe
    '''
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
    elif(sel==1): # substitute 
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

