# AutoTNLI-code

This repository contains the code for the paper : [Realistic Data Augmentation Framework for Enhancing Tabular Reasoning](https://vgupta123.github.io/docs/autotnli.pdf).

## 0. Prerequisites

Clone this repo - `git clone https://github.com/Dibyakanti/Auto-TNLI-code.git`\
Install requirements with the command `pip intall -r requirements.txt`

## 1. Data generation
To generate AutoTNLI use the command :
```
python3 generator.py --category_list <list_of_categories> --counterfactuals <number_of_counterfactuals> --store_json False

argument details :
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- counterfactuals: we give the user the ability to control the number of counterfcatuals they wanna generate per table
-- store_json: In case the user wants to store the json files generated for the counterfactual tables
```
OR

Go to the folder `scripts/sentence_generation` and run `bash generate.sh`

The data will be generated in the folder `data\autotnli_data\` for each category separately

## 2. Preprocessing


## 3. Training and Evaluation
