[![DOI](https://zenodo.org/badge/663444806.svg)](https://zenodo.org/badge/latestdoi/663444806)


# Database of Raman and ATR-FTIR spectra of weathered and biofouled polymers
**Brought to you by the JPI Oceans project [MicroplastiX](https://www.microplastix.org/)**

***Authors***: 
- [Robin Lenz¹](https://orcid.org/0000-0003-4156-7380)
- [Franziska Fischer¹](https://orcid.org/0000-0002-2317-6784)
- [Melinda Arnold¹](https://www.ipfdd.de/de/forschung/institut-makromolekulare-chemie/zentrum-makromolekulare-strukturanalyse/spektroskopie-mikroplastik/mitarbeiter/)
- [Verónica Fernández-González²](https://orcid.org/0000-0002-6890-6154)
- [Carmen María Moscoso Pérez²](https://orcid.org/0000-0002-2451-3535)
- [José Manuel Andrade-Garda²](https://orcid.org/0000-0003-1020-5213)
- [Soledad Muniategui-Lorenzo²](https://orcid.org/0000-0001-5946-3366)
- [Dieter Fischer¹](https://orcid.org/0000-0003-4458-2631)
                  

***Affiliations***:
- ¹Leibniz Institute of Polymer Research Dresden, Hohe Straße 6, 01069 Dresden, Germany
- ²University of A Coruña, Campus da Zapateira s/n, 15071, A Coruña, Spain

***Citation***:

To cite the most recent release of the MPX_specDB code please refer to:
> Lenz R, Fischer F, Arnold M, Fernández-González V, Moscoso-Pérez CM, Andrade-Garda JM, Muniategui-Lorenzo S, Fischer D, Database of Raman and ATR-FTIR spectra of weathered and biofouled polymers, 2023, https://doi.org/10.5281/zenodo.8314801.

The raw spectra collection can be found on the chemical research data repository [Radar4Chem](https://doi.org/10.22000/1820) and is citeable as:
> Lenz R, Fischer F, Arnold M, Fernández-González V, Moscoso-Pérez CM, Andrade-Garda JM, Muniategui-Lorenzo S, Fischer D, MicroPlastiX SpecDB, https://doi.org/10.22000/1820.                                                                                                                                                                                                                                                                                                                                

## Contents
This dataset is a spectroscopic library strucutred as a document database. It contains Raman and ATR-FTIR spectra of weathered and biofouled polymers which can be viewed via an interactive app.

> Project MicroPlastiX's Task 4.1 (formerly Task 3.4) examines the biofouling and colonization dynamics of plastic fragments.

In *in situ* experiments, plastic sheets of **10 different polymers** were deployed in the marine environment across **five geographical locations**. Their immersion in stainless steel cages for different intervals, over four seasons, imitates real-world exposure.

## View the app
A live version of the app can be found here: [https://robna.github.io/MPX_specDB/](https://robna.github.io/MPX_specDB/).
> <p align="center"><img src="data/media/qr-code_robna-github-io-mpx_specdb.svg" alt="https://robna.github.io/MPX_specDB/" width="100" height="100"></p>

## Local use
### Using the app
You can use the `Pipfile` to set up a virtual python environment using [pipenv](https://pipenv.pypa.io/en/latest/) or, alternatively the `requirements.txt` with a virtual env and package manager of your choice.
When using pipenv, open a terminal in the project directory and run `pipenv install` to install all dependencies.
Then run `pipenv run streamlit run app.py` to start the app.

### Assessing the data manually
Individual spectra can be found in the `data/spectra` folder, while all available information on the samples is stored in the `data/meta/metadata.json` file. Both will only be populated after the first run of the app or can be obtained from [Radar4Chem](https://doi.org/10.22000/1820).
The spectra filenames follow the pattern `[region]_[polymer]_[biofilm]_[analysis]_[hash].csv` where `hash` holds the first 8 characters of the sha256 hash of the spectrum data, in order to create unique filenames.
You can download or clone the repository to your local machine and use the `metadata.json` file to search for spectra of interest, e.g. by opening it in the Firefox browser which has some basic capabilities for navigating and searching in json files.

# License
Software code in this repository is licensed as specified in the [LICENSE.md](https://github.com/robna/MPX_specDB/blob/main/LICENSE.md) file.
Spectroscopic data and meta data is licensed under [CC BY SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
