<p align="center"><img width="80%" src="logo.png" /></p>

This repository contains the official code for the paper : [Realistic Data Augmentation Framework for Enhancing Tabular Reasoning](https://vgupta123.github.io/docs/autotnli.pdf).
```
@inproceedings{kumar-etal-2022-autotnli,
			title = "Realistic Data Augmentation Framework for Enhancing Tabular Reasoning",
			author = "Kumar, Dibyakanti  and
			  Gupta, Vivek  and
			  Sharma, Soumya  and
			  Zhang, Shuo",
			booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
			month = dec,
			year = "2022",
			address = "Online and Abu Dhabi",
			publisher = "Association for Computational Linguistics",
			url = "https://vgupta123.github.io/docs/autotnli.pdf",
			pages = "",
			abstract = "Existing approaches to constructing training data for Natural Language Inference (NLI) tasks, such as for semi-structured table reasoning, are either via crowdsourcing or fully automatic methods. However, the former is expensive and time-consuming and thus limits scale, and the latter often produces naive examples that may lack complex reasoning. This paper develops a realistic semi-automated framework for data augmentation for tabular inference. Instead of manually generating a hypothesis for each table, our methodology generates hypothesis templates transferable to similar tables. In addition, our framework entails the creation of rational counterfactual tables based on human written logical constraints and premise paraphrasing. For our case study, we use the InfoTabS (Gupta et al., 2020), which is an entity-centric tabular inference dataset. We observed that our framework could generate human-like tabular inference examples, which could benefit training data augmentation, especially in the scenario with limited supervision.",
		}
```
## 0. Prerequisites

Clone this repo - `git clone https://github.com/Dibyakanti/Auto-TNLI-code.git`\
Install requirements with the command `pip intall -r requirements.txt`

```
├── data
│   ├── autotnli_data
│   │   └── README.md
│   ├── autotnli_splits
│   │   ├── category
│   │   ├── category_cross
│   │   ├── entity
│   │   ├── key
│   │   └── parapharsing
│   ├── infotabs_data
│   │   ├── first_stage
│   │   ├── first_stage_limited
│   │   ├── original_data
│   │   │   ├── dev.tsv
│   │   │   ├── test_alpha1.tsv
│   │   │   ├── test_alpha2.tsv
│   │   │   ├── test_alpha3.tsv
│   │   │   └── train.tsv
│   │   ├── second_stage
│   │   ├── second_stage_limited
│   │   └── test
│   ├── models_saved
│   │   ├── first_stage
│   │   └── second_stage
│   ├── results
│   │   ├── first_stage
│   │   └── second_stage
│   └── wiki_data
│       ├── all_jsons.json
│       ├── json
│       │   ├── T0.json
│       │   ├── T1000.json
│       │   ├── T1001.json
│       ├── table_categories modified.tsv
│       ├── table_categories.tsv
│       ├── tables
│       │   ├── T0.html
│       │   ├── T1000.html
│       │   ├── T1001.html
│       └── wikipediaTableCategories.tsv
│
└── scripts
│   ├── model_scripts
│   │   ├── aggregate_both_stages_albert.py
│   │   ├── aggregate_both_stages_roberta.py
│   │   ├── classifier_albert.py
│   │   ├── classifier.py
│   │   ├── feedforward.py
│   │   ├── preprocess.py
│   │   └── utils.py
│   ├── preprocessing_data
│   │   ├── preprocess_2_stage.py
│   │   ├── preprocess_infotabs.py
│   │   └── preprocess_standalone.py
│   └── sentence_generation
│       ├── Album.py
│       ├── Book.py
│       ├── City.py
│       ├── Festival.py
│       ├── FoodnDrinks.py
│       ├── generate.sh
│       ├── generator.py
│       ├── __init__.py
│       ├── Movie.py
│       ├── Organization.py
│       ├── Paint.py
│       ├── Person.py
│       ├── SportsnEvents.py
│       ├── University.py
│       └── util.py
├── LICENSE
├── logo.png
├── README.md
├── requirements.txt
```

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
-- epochs: set training epochs number (only used while training, i.e., model is "train")
-- batch_size: set batch size for training (only used while training)
-- nooflabels: 
-- in_dir: set as preprocessed directory name.
-- save_dir: path to the directory where the trained models and the predictions are stored
-- nooflabels: set as 3 as three labels entailment, neutral and contradiction)
-- save_folder: name of the folder where the trained models and the predictions are stored
-- model_dir: Path to directory containing the trained model (used while mode=="test" or when load=="True")
-- model_name: model filename usually is in format 'model_<epoch>_<accuracy>' (used while mode=="test" or when load=="True")
-- mode: set "train" for training, set "test" for prediction
-- dev_file: name of the development set file
-- train_file: name of the training set file
-- embed_size: set this to 768 for base model and 1024 for large model
-- save_enable: set as 1 to save prediction files as predict_<datasetname>.json in save_dir.
-- eval_splits:  ' ' separated datasplits names [dev, test_alpha1, test_alpha2, test_alpha3] (only used while prediction, i.e., model is "test")
-- seed: set a particular seed
-- parallel: for a single GPU, 1 for multiple GPUs (used when training large data, use the same flag at both predictions and train time)
-- load: to start training from a previously saved checkpoint
-- learning_rate: set the learning rate
-- store_best: to store the model with the best dev accuracy
```
Note : While training make sure the save_folder is set differently for each split to avoid overwriting and confusion

## 3.2 AutoTNLI as an Augmentation dataset
Similar to `Section 3.1` when training.

While testing for RoBERTa make sure the first stage model is stored in model_dir + "first_stage" and model_dir + "second_stage" for second stage
```
python3 ./scripts/model_scripts/aggregrate_both_stages_roberta.py \
--in_dir "./data/infotabs_data/test/processed/"
--nooflabels 2
--save_dir "./data/results/"
--save_folder "./first_stage/"
--model_dir "./models_saved/first_stage/"
--model_name_first_stage "model_<epoch>_<accuracy>"
--model_name_second_stage "model_<epoch>_<accuracy>"
--embed_size 768
--save_enable 1
--eval_splits den test_alpha1 test_alpha2 test_alpha3

argument details :
-- in_dir: set as preprocessed directory name.
-- nooflabels: set as 2 as three labels
-- save_dir: path to the directory where the predictions are stored
-- save_folder: name of the folder where the predictions are stored
-- model_dir: Path to directory containing the trained model (used while mode=="test" or when load=="True")
-- model_name_first_stage: model filename for the stage-1 usually is in format 'model_<epoch>_<accuracy>' 
-- model_name_second_stage: model filename for the stage-2 usually is in format 'model_<epoch>_<accuracy>'
-- embed_size: set this to 768 for base model and 1024 for large model
-- save_enable: set as 1 to save prediction files as predict_<datasetname>.json in save_dir.
-- eval_splits: ' ' separated datasplits names [dev, test_alpha1, test_alpha2, test_alpha3] (only used while prediction, i.e., model is "test")
```

## 3.3 Few-shot setting
Similar to `Section 3.1` while training and `Section 3.2` while testing.
