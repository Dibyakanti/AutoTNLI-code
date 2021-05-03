# All lists important for creating data

Dict = {"Psn1" : ["BDA","BDA","BDA","Spouse","Occupation","Education","Children","Genres","Labels","Website","Conviction","Institutions"
        ,"Fields","Doctoral_students","Awards","Relatives","Resting_place","Parents","Instruments","Residence","Years_active"]
      ,"Psn2" : ["Born","Died","Age","Spouse","Occupation","Education","Children","Genres","Labels","Website","Conviction","Institutions"
        ,"Fields","Doctoral_students","Awards","Relatives","Resting_place","Parents","Instruments","Residence","Years_active"] 
      ,"Psn":["Spouse","Occupation","Education","Genres","Labels","Website","Conviction","Institutions","Fields","Doctoral_students"
      	,"Awards","Relatives","Resting_place","Parents","Instruments","Residence","Years_active"]
      ,"Movie_tr1":["Directed_by","Produced_by","Screenplay_by","Starring","Music_by","Cinematography"
      	,"Edited_by","Productioncompany","Distributed_by","Release_date","Running_time","Country","Language","Budget","Box_office"]
      ,"Book_tr1":["Publisher","Schedule","Format","Genre","Publication_date","No_of_issues","Main_character","Written_by"]
      ,"FnD_tr1":["Manufacturer","Country_of_origin","Variants","Introduced","Related_products"
      	,"Alcohol_by_volume","Website","Color","Main_ingredients","Type"]
      ,"Organiz_tr1":["Website","Headquarters","Founded","Industry","Key_people","Products","Number_of_employees"
      	,"Traded_as","Founder","Area_served","Type","Subsidiaries","Parent","Owner","Predecessor"]
      ,"Paint_tr1":["Artist","Year","Medium","Dimensions","Location"]
      ,"Fest_tr1":["Type","Observed_by","Frequency","Celebrations","Significance","Observances","Date","Related_to","Also_called"
      	,"Official_name","Begins","Ends","2021_date","2020_date","2019_date","2018_date"]
      ,"SpEv_tr1":["Venue","Date","Competitors","Teams","No_of_events","Established","Official_site"]
      ,"Univ_tr1":["Website","Type","Established","Undergraduates","Postgraduates","Motto","Location"
      	,"Nickname","Campus","Colors","Students","Academic_staff","Administrative_staff","President","Endowment","Mascot"
      	,"Provost","Sporting_affiliations","Academic_affiliations","Former_names"] }

Cnt = { "Psn" : 626
      ,"Movie_tr1":200
      ,"Book_tr1":51
      ,"FnD_tr1":80
      ,"Organiz_tr1":79
      ,"Paint_tr1":132
      ,"Fest_tr1":35
      ,"SpEv_tr1":80
      ,"Univ_tr1":37 }

getfa = {
"Psn":{"Spouse":[1],"Occupation":[0,1,2],"Education":[1],"Children":[1],"Genres":[0,1,2],"Labels":[0,1,2],"Website":[1]
  ,"Conviction":[0,1,2],"Institutions":[1],"Fields":[0,1,2],"Doctoral_students":[0,1,2],"Awards":[0,1,2],"Relatives":[0,1]
  ,"Resting_place":[0,1,2],"Parents":[1],"Instruments":[0,1,2],"Residence":[1],"Years_active":[1]},
"Movie_tr1":{"Directed_by":[0,1,2],"Produced_by":[0,1,2],"Screenplay_by":[1],"Starring":[0,1,2],"Music_by":[0,1,2],"Cinematography":[1]
  ,"Edited_by":[0,1,2],"Productioncompany":[1],"Distributed_by":[0,1,2],"Release_date":[0,1,2],"Running_time":[1]
  ,"Country":[0,1,2],"Language":[0,1,2],"Budget":[1],"Box_office":[1]},
"Book_tr1":{"Publisher":[1],"Schedule":[1],"Format":[0,1,2],"Genre":[0,1,2],"Publication_date":[1],
        "No_of_issues":[1],"Main_character":[0,1,2],"Written_by":[0,1,2]},
"FnD_tr1":{"Manufacturer":[1],"Country_of_origin":[0,1,2],"Variants":[0,1,2],"Introduced":[1],"Related_products":[0,1,2],
    "Alcohol_by_volume":[1],"Website":[1],"Color":[0,1,2],"Main_ingredients":[0,1,2],"Type":[0,1,2]},
"Organiz_tr1":{"Wesbsite":[1],"Headquarters":[1],"Founded":[1],"Industry":[0,1,2],"Key_people":[0,1,2],"Products":[0,1,2]
	,"Number_of_employees":[1],"Traded_as":[0,1,2],"Founder":[0,1,2],"Area_served":[0,1,2],"Type":[1],"Subsidiaries":[0,1,2]
	,"Parent":[1],"Owner":[1],"Predecessor":[1]},
"Paint_tr1":{"Artist":[1],"Year":[1],"Medium":[1],"Dimensions":[1],"Location":[1]},
"Fest_tr1":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],
    "Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],
    "2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"SpEv_tr1":{"Venue":[0,1,2],"Date":[1],"Competitors":[0,1,2],"Teams":[1],
	"No_of_events":[1],"Established":[1],"Official_site":[1]},
"Univ_tr1":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],
    "Motto":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],
    "Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],
    "Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]}
}

multi_row_Cnt = { "Psn" : 3
      ,"Movie_tr1":3
      ,"Book_tr1":4
      ,"FnD_tr1":3
      ,"Organiz_tr1":3
      ,"Paint_tr1":2
      ,"Fest_tr1":3
      ,"SpEv_tr1":2
      ,"Univ_tr1":3 }