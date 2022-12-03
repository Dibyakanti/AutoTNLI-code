# AutoTNLI-data

The data is available at [Drive Link](https://drive.google.com/drive/folders/1xzgkvg6_7US8sJlROe7jaEfIT1QCuT92?usp=sharing).

Below we have shown an example of a table

| table | premises | hypothesis | label | key & premises_used | json_name |
|-------|----------|------------|-------|---------------------|-----------|
| T211 | Kase-san is of romance,yuri genre . The book was written by Hiromi Takashima | Kase-san falls in the genres of romance,yuri | E | {'Genre': ['Kase-san is of romance,yuri genre', 'This book is of romance,yuri genre', 'It falls in romance,yuri category']} | T211 |

Details about each column heading :
table: name of the table from which the sentences are generated
premises: premise\
hypothesis: hypothesis\
label: label for the premise-hypothesis pair\
key & premises_used: the key and the corresponding premises used to infer the hypothesis\
json_name: name of the json from which the sentences were generated\

For each category we have 5 .tsv files ending with _T0, _F1, _F2, _F3, _F4 and _F5. So, here we _T0 represents the ones generated from the original table, and _F<int> represents the ones generated from the counterfactual tables.
