# AutoTNLI-code

This repository contains the official code for the paper : [Realistic Data Augmentation Framework for Enhancing Tabular Reasoning](https://vgupta123.github.io/docs/autotnli.pdf).

## 0. Prerequisites

Clone this repo - `git clone https://github.com/Dibyakanti/Auto-TNLI-code.git`\
Install requirements with the command `pip intall -r requirements.txt`

## 1. Data generation
To generate AutoTNLI use the command :
```
python3 ./scripts/sentence_generation/generator.py \
--category_list <list_of_categories> \
--counterfactuals <number_of_counterfactuals> \
--store_json False

argument details :
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- counterfactuals: we give the user the ability to control the number of counterfcatuals they wanna generate per table
-- store_json: In case the user wants to store the json files generated for the counterfactual tables

example command:
python3 ./scripts/sentence_generation/generator.py \
--category_list Book City Movie \
--counterfactuals 2 \
--store_json True
```
OR

Go to the folder `scripts/sentence_generation` and run `bash generate.sh`

The data will be generated in the folder `data/autotnli_data/` for each category separately

## 2. Preprocessing

### 2.1. Preprocessing data for standalone setting
To generate splits for checking how does AutoTNLI data perform when used for both training and evaluation
```
python3 ./scripts/preprocessing_data/preprocess_standalone.py \
--split_type "<split_type>" \
--in_dir "./data/autotnli_data/" \
--out_dir "./data/autotnli_splits/<type_of_split>/" \
--category_list <list_of_categories> \
--table_list <list_of_tables>

argument details for each split type :
-- in_dir: Path to folder where the AutoTNLI data is generated and stored
-- out_dir: Path to folder where you want the preprocessed data to be stored
-- category_list: list of categories that you want to generate the data for (i.e. Album, Book, City, Festival, FoodnDrinks, Movie, Organization, Paint, Person, SportsnEvents, University )
-- table_list: list of tables (example: _T0, _F1, _F2)
-- split_type: Type of split you wanna make (i.e. category, key, premise, entity)

if split_type == "category" then:
-- post_cross_category: make the splits done after cross category analysis

if split_type == "key" then:
-- use_metadata: Set to True if you want to make the same key split and you have a metadata file stored in metadata_path
-- metadata_path: Path of the file where the metadata for key splits is stored


if split_type == "premise" then:
-- train_complementary_test: Set to True if you want train to have different paraphrased premises compared to dev/test split

example command:
python3 ./scripts/preprocessing_data/preprocess_standalone.py \
--split_type "premise" \
--in_dir "./data/autotnli_data/" \
--out_dir "./data/autotnli_splits/key/" \
--category_list Book Movie City \
--table_list _T0 _F1 _F2 \
--use_metadata False
```
Note : Make separate folders for each split

### 2.2 Preprocessing data for 2-stage classifier
To generate splits for pre-finetuning with AutoTNLi data
```
python3 ./scripts/preprocessing_data/preprocess_2_stage.py \
--in_dir "./data/autotnli_data/" \
--out_dir "./data/autotnli_splits/<type_of_split>/" \
--category_list <list_of_categories> \
--table_list <list_of_tables> \
--cutoff 30 \
--relevant_rows False

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
python3 ./scripts/preprocessing_data/preprocess_infotabs.py \
--in_dir "./data/infotabs_data/original_data" \
--out_dir "./data/infotabs_data/<type_of_split>/" \
--stage <int> \
--few_shot False

argument details :
-- in_dir: Path to folder where the AutoTNLI data is generated and stored
-- out_dir: Path to folder where you want the preprocessed data to be stored
-- stage: Put 1 for stage-1, 2 for stage-2 and 3 for the test data.
-- few_shot: Set to True of you want to generate 5,10,15,20,25 percent train data splits

example command:
python3 ./scripts/preprocessing_data/preprocess_infotabs.py \
--in_dir "./data/infotabs_data/original_data" \
--out_dir "./data/infotabs_data/first_stage_limited/" \
--stage 1 --few_shot True
```
Note : Make separate folders for each split
## 3. Training and Evaluation

## 3.0 Preprocess (Tokenize) each datasplit that you generated in the previous section
```
python3 ./scripts/model_scripts/preprocess.py \
--max_len 512 \
--data_dir "./data/" \
--in_dir "./autotnli/<split_type>" \
--out_dir "./autotnli/<split_type>/processed" \
--single_sentence 0 \
--splits train dev test_alpha1 \
--model <model_name>

argument details :
-- max_len: Maximum length of the tokenized sentence
-- data_dir: Path to directory that contains all the data
-- in_dir: Path to the directory in 'data_dir' which contains the splits to be tokenized
-- out_dir: Path to the directory in 'data_dir' where we get the tokenized data
-- single_sentences: Set 1 for hypothesis-only cases
-- splits: List of splits that are to be toknized from the 'in_dir'
-- model: This is to be set to RoBERTa or Albert

example command :
python3 ./scripts/model_scripts/preprocess.py \
--max_len 512 \
--data_dir "./data/" \
--in_dir "./autotnli/key" \
--out_dir "./autotnli/key/processed" \
--single_sentence 0 \
--splits train dev test_alpha1 \
--model "RoBERTa"
```

## 3.1 Standalone setting
To train and test the RoBERTa on AutoTNLI datasets
```
python3 ./scripts/model_scripts/classifier.py \
--epochs 10 \
--batch_size 8 \
--nooflabels 2 \
--in_dir "./data/autotnli/<split_type>/processed/" \
--save_dir "./data/models_saved/" \
--save_folder "./autotnli/<split_type>/" \
--model_dir "./data/models_saved/autotnli/<split_type>/" \
--model_name model_<epoch>_<accuracy_on_dev> \
--mode "test" \
--dev_file "dev" \
--train_file "train" \
--embed_size 768 \
--save_enable 1 \
--eval_splits den test_alpha1 \
--seed 17 \
--parallel 0 \
--load False \
--learning_rate 1e-4 \
--store_best False

argument details :
-- epochs:
-- batch_size:
-- nooflabels:
-- in_dir: 
-- save_dir:
-- save_folder:
-- model_dir:
-- model_name:
-- mode:
-- dev_file:
-- train_file:
-- embed_size:
-- save_enable:
-- eval_splits:
-- seed:
-- parallel:
-- load:
-- learning_rate:
-- store_best:

```
## 3.2 AutoTNLI as an Augmentation dataset


## 3.3 Few-shot setting


## TODO: 
