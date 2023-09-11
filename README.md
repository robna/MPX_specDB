[![DOI](https://zenodo.org/badge/663444806.svg)](https://zenodo.org/badge/latestdoi/663444806)


# Database of Raman and ATR-FTIR spectra of weathered and biofouled polymers
**Brought to you by the JPI Oceans project [MicroplastiX](https://www.microplastix.org/)**

***Authors***: 
- [Robin Lenz¹](https://orcid.org/0000-0003-4156-7380)
- [Franziska Fischer¹](https://orcid.org/0000-0002-2317-6784)
- [Melinda Arnold¹](https://www.ipfdd.de/de/forschung/institut-makromolekulare-chemie/zentrum-makromolekulare-strukturanalyse/spektroskopie-mikroplastik/mitarbeiter/)
- [José Manuel Andrade-Garda²](https://orcid.org/0000-0003-1020-5213)
- [Soledad Norberta Muniategui-Lorenzo²](https://orcid.org/0000-0001-5946-3366)
- [Dieter Fischer¹](https://www.ipfdd.de/de/organisation/organigramm/personal-homepages/dr-dieter-fischer/)
                  

***Affiliations***:
- ¹Leibniz Institut für Polymerforschung Dresden, Hohe Straße 6, 01069 Dresden, Germany
- ²University of A Coruña, Campus da Zapateira s/n, 15071, A Coruña, Spain

***Citation***:
> Lenz R, Fischer F, Arnold M, Andrade-Garda JM, Muniategui-Lorenzo SN, Fischer D, Database of Raman and ATR-FTIR spectra of weathered and biofouled polymers, 2023, https://doi.org/10.5281/zenodo.8314801.

## Contents
This dataset is a spectroscopic library structured as a document database.
It contains Raman and ATR-FTIR spectra of weathered and biofouled polymers.

> Project MicroPlastiX's Task 4.1 (formerly Task 3.4) examines the biofouling and colonization dynamics of plastic fragments.

In *in situ* experiments, plastic sheets of **10 different polymers** were deployed in the marine environment across **five geographical locations**.
Their immersion in stainless steel cages for different intervals, over four seasons, imitates real-world exposure.
## Local use
### Obtaining the data manually
Individual spectra can be be found in the `spectra` folder, while all available information on the samples is stored in the `metadata,json` file.
The spectra file names follow the pattern `[Region]_[Polymer]_[Biofilm]_[Analysis]_[hash].csv` where `hash` holds the first 8 characters of the sha256 hash of the spectrum data, in order to create unique file names.
You can download or clone the repository to your local machine and use the `metadata.json` file to search for spectra of interest (for convenice, excel users can also take a look at the `metadata.xlsx` file, which contains the same information).

### Using the app
You can use the `Pipfile` to set up a virtual python environment using [pipenv](https://pipenv.pypa.io/en/latest/) or, alternatively the `requirements.txt` with a virtual env and package manager of your choice.
When using pipenv, open a terminal in the project directory and run `pipenv install` to install all dependencies.
Then run `pipenv run streamlit run app.py` to start the app.
