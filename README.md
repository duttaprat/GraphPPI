# GraphPPI

## This is the readme file that contains the guidelines and information about the compilation the code of the following paper

**Paper Name:-** Graph-based Hub Gene Selection Technique using Protein Interaction Information: Application to  Sample Classification
>This paper explores the information of protein-protein interaction (PPI) with a graph mining technique for finding a proper subset of features (genes), which further takes part in sample classification. Here, our contribution for feature selection is three-fold: firstly, all the genes are grouped into different clusters based on the integrated information of the gene expression values and their protein interactions using a multi-objective optimization (MOO) based clustering approach. Secondly, the confidence scores of the protein interactions are incorporated in a popular graph mining algorithm namely Goldberg algorithm to find out the relevant features. These features are the topologically and functionally significant genes, named as hub genes. Finally, these hub genes are identified varying the degrees of the nodes, and those are utilized for the sample classification task.


* **Authors:** Pratik Dutta, Sriparna Saha and Saurabh Gulati
* **Affiliation:** Indian Institute of Technology Patna, India
* **Corresponding Author:** [Pratik Dutta](http://www.iitp.ac.in/~pratik.pcs16/) (pratik.pcs16@iitp.ac.in ) 
* **Accepted(12th January, 2019):**  [IEEE Journal of Biomedical and Health Informatics(IEEE JBHI)](https://jbhi.embs.org/)
	

## Prerequisities
* **[Python 2.7+](https://www.python.org/downloads/release/python-2713/)**
* **[sklearn](https://scikit-learn.org/stable/install.html)**
* **[matplotlib 2.0+](https://matplotlib.org/users/installing.html)**
* **[mpl_toolkits](https://matplotlib.org/2.0.2/mpl_toolkits/index.html)**
* **[numpy 1.10+](https://pypi.org/project/numpy/)**
* **[Cytoscape](https://cytoscape.org/download.html)**


# Description

## 1. MOO-based clustering

This folder contains the python code of the proposed MOO-based clustering. Use `terminal`(for linux users) and goto the '1. MOO-based clustering' folder. Then complie the code by following commands

```bash
cd examples
```
Write the **_PATH DESCRIPTION_** of the `dataset` in line number **28** of the **`main.py`**


```bash
python main.py <initial_population_size> <number_of_generation>
```

**Output:** Generate a file named **`non_dominated_solutions.txt`** that contains all the cluster information.


## 2. Modified Goldberg Algorithm
This folder contains the modified Goldberg Algorithm.

**`3. Significant_genes_expression_values.py`** Obtain the gene expression values of the selected genes.

**`4. all_classifiers.py`** Implementation of four classifiers (SVM, Random Forest, kNN, and ANN) with 10-fold cross validation


# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 



