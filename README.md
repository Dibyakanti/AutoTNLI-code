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
python3 ./scripts/preprocessing_data/preprocess_standalone.py --split_type <split_type> --in_dir ./data/autotnli_data/ --out_dir ./data/autotnli_splits/<type_of_split>/ --category_list <list_of_categories> --table_list <list_of_tables>

argument details for each split type :
-- in_dir: Path to folder where the AutoTNLI data is generated and stored
-- out_dir: Path to folder where you want the preprocessed data to be stored
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
To generate splits for pre-finetuning with AutoTNLi data
```
python3 ./scripts/preprocessing_data/preprocess_2_stage.py --in_dir ./data/autotnli_data/ --out_dir ./data/autotnli_splits/<type_of_split>/ --category_list <list_of_categories> --table_list <list_of_tables> --cutoff 30 --relevant_rows False

argument details :
-- in_dir: Path to folder where the AutoTNLI data is generated and stored
-- out_dir: Path to folder where you want the preprocessed data to be stored
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- table_list: list of tables (example: _T0, _F1, _F2)
-- cutoff: how many max tables should be chosen from each category
-- relevant_rows: If you only want to store the relevant premises
```
Note : Make separate folders for each split
### 2.3 Preprocessing Infotabs data
To generate spits from the infotabs data which will be used for fine-tuning
```
python3 ./scripts/preprocessing_data/preprocess_infotabs.py --in_dir ./data/infotabs_data/original_data --out_dir ./data/infotabs_data/<type_of_split>/ --stage <int> --few_shot False

argument details :
-- in_dir: Path to folder where the AutoTNLI data is generated and stored
-- out_dir: Path to folder where you want the preprocessed data to be stored
-- stage: Put 1 for stage-1, 2 for stage-2 and 3 for the test data.
-- few_shot: Set to True of you want to generate 5,10,15,20,25 percent train data splits

example command:
python3 ./scripts/preprocessing_data/preprocess_infotabs.py --in_dir ./data/infotabs_data/original_data --out_dir ./data/infotabs_data/first_stage_limited/ --stage 1 --few_shot True
```
Note : Make separate folders for each split
## 3. Training and Evaluation

## TODO: 
