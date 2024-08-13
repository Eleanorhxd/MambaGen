# MambaGen
**This is the data and code for our paper** `MambaGen: Efficient Visual Representation Learning for Automatic Radiology Report Generation`.

For reproduction of medication prediction results in our paper, see instructions below.

## Overview
We have modularized and encapsulated the code into a more readable form. In brief, MambaGen consists of three parts: encoder and decoder, encoder mainly gengerates the representation of patients and decoder calculates the usage probability for each drug labels.
## Prerequisites

Make sure your local environment has the following installed:

* `pytorch>=1.12.1 & <=1.9`
* `numpy == 1.15.1`
* `python >= 3.8`
* `scikit-learn>=0.24.2`
* `Torchvision`
* `Pycocoevalcap`
#### Datastes

We use two publicly available radiology report generation datasets (IU X-Ray and MIMIC-CXR) in our paper.

For `IU X-Ray`, you can download the dataset from [here](https://openi.nlm.nih.gov/faq).

For `MIMIC-CXR`, you can download the dataset from [here](https://physionet.org/content/mimic-cxr/2.0.0/).

| Dataset |Type| TRAIN | VAL | TEST |
| :------ | --------: | --------: | -----: |
| IMAGE# | 5,226 | 748 | 1,496 |
|IU X-ray| REPORT# | 2,770 | 395 | 790 |
| PATIENT# | 2,770 | 395 | 790 |
| AVG.LEN | 37.56 | 36.78 | 33.62 |

After downloading the datasets, put them in the directory `data`.

## Documentation

```
--src
  │--README.md
  │--data_loader.py
  │--train.py
  │--model_net.py
  │--outer_models.py
  │--util.py
  
--datas
  │--ddi_A_final.pkl
  │--combo_label_convert_matrix.pkl
  │--records_final_iii.pkl
  │--records_final_iv.pkl
  │--voc_final_iii.pkl
  │--voc_final_iv.pkl

--combo
  │--iii
    │--pattern_records_final.pkl
  │--iv
    │--pattern_records_final.pkl
```

## How to MambaGen

### 1 Install IDE 

Our project is built on PyCharm Community Edition ([click here to get](https://www.jetbrains.com/products/compare/?product=pycharm-ce&product=pycharm)).

### 2 Environment setting
#### 2.1 Inpterpreter 
We recommend using `Python 3.11` or higher as the script interpreter. [Click here to get](https://www.python.org/downloads/release/python-3110/) `Python 3.11`. 
#### 2.2 Packages
Please follow the packages in [Prerequisites](#prerequisites), utilize `pip install <package_name>` to construct the environment.
### 3 Start training
Please follow the steps below:
3.1 prepare data and process
  In ./data, you can find the well-preprocessed data in pickle form. Also, it's easy to re-generate the data as follows:

  - download MIMIC data and put DIAGNOSES_ICD.csv, PRESCRIPTIONS.csv, PROCEDURES_ICD.csv in ./data/
  - download DDI data and put it in ./data/
  - run code ./data/processing.py
    
  Data information in ./data:

  - records_final.pkl is the input data with four dimension (patient_idx, visit_idx, medical modal, medical id)           where medical model equals 3 made of diagnosis, procedure and drug.
  - voc_final.pkl is the vocabulary list to transform medical word to corresponding idx.
  - ddi_A_final.pkl and are drug-drug adjacency matrix constructed from EHR and DDI dataset.
  - combo_label_convert_matrix.pkl is mapping files for FP Tree algorithm script.
    
  3.2 run main.py


## Performance of LDENet
Compared with existing methods, LDENet shows a significant advantage on several common metrics:


| Methods  | Jaccard             | PRAUC               | F1                  | DDI             | AVG_MED           |
|----------|---------------------|---------------------|---------------------|-----------------|-------------------|
| ECC      | 0.4996 / 0.4233     | 0.6844 / 0.7284     | 0.6569 / 0.5680     | 0.0846 / 0.0771 | 18.0722 / 8.1070  |
| LEAP     | 0.4521 / 0.4287     | 0.6549 / 0.5506     | 0.6138 / 0.5820     | 0.0731 / 0.0592 | 18.7138 / 11.5198 |
| GAMENet  | 0.5237 / 0.4963     | 0.7775 / 0.7508     | 0.6783 / 0.6514     | 0.0861 / 0.0890 | 27.2145 / 18.4426 |
| SafeDrug | 0.5233 / 0.5000     | 0.7742 / 0.7485     | 0.6764 / 0.6557     | 0.0615 / 0.0575 | 19.9178 / 14.4705 |
| COGNet   | 0.5336 / 0.4884     | 0.7739 / 0.7087     | 0.6869 / 0.6367     | 0.0852 / 0.0894 | 28.0900 / 19.7235 |
| DGCL     | 0.5255 / 0.4993     | 0.7738 / 0.7535     | 0.6801 / 0.6542     | 0.0836 / 0.0735 | 28.6253 / 16.6284 |
| Carmen   | 0.5323 / 0.5049     | 0.7736 / 0.7513     | 0.6865 / 0.6615     | - / -           | - / -             |
| MoleRec  | 0.5271 / 0.4930     | 0.7717 / 0.7426     | 0.6816 / 0.6503     | 0.0726 / 0.0961 | 21.6489 / 18.7085 |
| LDENet   | **0.5497 / 0.5251** | **0.7960 / 0.7761** | **0.7014 / 0.6788** | 0.0629 / 0.0657 | 19.2441 / 17.1884 |


## Acknowledgement
We sincerely thank - [R2GenCMN](https://github.com/cuhksz-nlp/R2GenCMN).

## TODO

To make the experiments more efficient, we developed some experimental scripts, which will be released along with the paper later.
