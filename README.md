# AutoTNLI-code

This repository contains the code for the paper : [Realistic Data Augmentation Framework for Enhancing Tabular Reasoning](https://vgupta123.github.io/docs/autotnli.pdf).

## 0. Prerequisites

Clone this repo - `git clone https://github.com/Dibyakanti/Auto-TNLI-code.git`\
Install requirements with the command `pip intall -r requirements.txt`

## 1. Data generation
To generate AutoTNLI use the command :
```
python3 ./scripts/sentence_generation/generator.py --category_list <list_of_categories> --counterfactuals <number_of_counterfactuals> --store_json False

argument details :
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- counterfactuals: we give the user the ability to control the number of counterfcatuals they wanna generate per table
-- store_json: In case the user wants to store the json files generated for the counterfactual tables

example command:
python3 ./scripts/sentence_generation/generator.py --category_list Book City Movie --counterfactuals 2 --store_json True
```
OR

Go to the folder `scripts/sentence_generation` and run `bash generate.sh`

The data will be generated in the folder `data/autotnli_data/` for each category separately

## 2. Preprocessing

### 2.1. Preprocessing data for standalone setting
To generate splits for checking how does AutoTNLI data perform when used for both training and evaluation
```
python3 ./scripts/preprocessing_data/preprocess_standalone.py --split_type <type_of_split> --in_dir ./data/autotnli_data/ --out_dir ./data/autotnli_splits/<type_of_split>/ --category_list <list_of_categories> --table_list <list_of_tables>

argument details for each split type :
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- table_list: list of tables (example: _T0, _F1, _F2)
-- split_type: Type of split you wanna make (i.e. category, key, premise, entity)

if split_type == category then:
-- post_cross_category: make the splits done after cross category analysis

if split_type == key then:
-- use_metadata: Set to True if you want to make the same key split and you have a metadata file stored in metadata_path
-- metadata_path: Path of the file where the metadata for key splits is stored


if split_type == premise then:
-- train_complementary_test: Set to True if you want train to have different paraphrased premises compared to dev/test split

example command:
python3 ./scripts/preprocessing_data/preprocess_standalone.py --split_type premise --in_dir ./data/autotnli_data/ --out_dir ./data/autotnli_splits/key --category_list Book Movie City --table_list _T0 _F1 _F2 --use_metadata False
```
Note : Make separate folders for each split

### 2.2 Preprocessing data for 2-stage classifier

### 2.3 Preprocessing Infotabs data

## 3. Training and Evaluation
