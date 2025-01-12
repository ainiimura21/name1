# Monitoring Progression of Scleroderma

---
## Project Description
This is a website for visualising datasets to study protein expression in Scleroderma patients. The website is able to 
generate the following plots:
- Correlation Plot
- Boxplot
- UMAP plot
- Volcano plot

---
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact/Support](#contact)
  
---
## Introduction
Scleroderma is an autoimmune disease that can cause thickened areas of skin and connective tissues. To gain a deeper
understanding of this condition, analysing the expression of different proteins observed in Scleroderma patients is 
highly beneficial.
This website utilizes a dataset to generate 4 graphs, enabling researchers to analyse results while requiring
minimal bioinformatics expertise.


---
## Features
### Selecting Protein
Users can search for proteins using multiple naming conventions including:
- Protein Name
- Full Protein Name
- Entrez Gene ID
- Entrez Gene Symbol

Alternatively, users can utilize the volcano plot on the main page to select a protein by hovering over and clicking 
on the plot.
### Volcano Plot

### Correlation Plot

### Box Plot

### UMAP Plot

---
## Installation
1. Clone the repository:
```bash
 git clone https://github.com/ainiimura21/name1.git
```

2. Install dependencies:
```bash
pip install numpy pandas matplotlib seaborn streamlit
 ```

## Usage
To run the project, use the following command:
```bash
streamlit run app/main.py
```

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.


