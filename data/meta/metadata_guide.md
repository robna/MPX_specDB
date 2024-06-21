### Metadata guide
| Column name | Description | Possible values | Explanation |
| ----------- | ----------- | --------------- | ----------- |
| **Region** | Short code for location of the experiment<br />For further specifications: see columns<br />`LocationDescription`, `Country`, `LAT`, `LON` | VLFR<br />NAP<br />LCG | Villefranche-sur-Mer, France<br />Naples, Italy<br />A Coruña / Ares Harbour, Spain |
| **Campaign** | Season of the experiment | Summer<br />Autumn<br />Winter<br />Spring<br />Longterm | start: 2021-06-22<br />start: 2021-09-22<br />start: 2021-12-22<br />start: 2022-03-22<br />start: 2022-01-00 |
| **State** | Transportation and conservation state<br />of the polymer sheet | dry<br />ethanol | sheets were stored and transported dry<br />sheets were stored and transported in ethanol |
| **Treatment** | Condition of the polymer sheet<br />when spectrum was collected | bio<br />nobio | original condition: biofilm was not removed<br />treated condition: biofilm was removed with H~2~O~2~ |
| **Analysis** | Type of spectroscopy | Raman<br />ATR | Raman spectroscopy<br />ATR-FTIR spectroscopy |
| **Exposure_days** | Number of days the polymer sheet was<br />immersed in the sea | 7, 15, 30, 60, 90<br />183 | number of days exposed at sea for seasonal experiments<br /> long term exposure was 6 months |
| **Polymer**<br />**Product_ID**<br />**Supplier**<br />**Specifications** | Details of the polymer used | *str* | see **Polymer guide table** below |
| **Polymer_ID** | Polymer identification number | *int* | integer representation of the polymer code used in this project (also included in `Polymer`)<br />Caution: numbering between sheet polymers and in-situ polymers are not compatible! |
| **file** | name of csv file containing the spectrum | *str* | file names are unique, they follow this structure:<br />[Region]_[Polymer]_[Treatment]_[part-of-file-hash] |
| **file_legacy** | original file names before data set standardisation | *str* | paths kept for reference to the original measurement files |
| **spec_hash** | hash of the spectrum | *str* | hexdigest of the sha256 hash of a spectrum's x, y data as 2-column array in binary representation<br />I.e. using `sha256(spec.to_numpy().tobytes()).hexdigest()`<br />where spec is a 2-column Pandas data frame holding x, and y values |
| **SpecNo** | number of the spectrum | *int* | for ATR measurements of NAP and LCG, spectra of the same sheet were consecutively numbered |
| **ATRcorrection** | Flag if spectrum was ATR corrected<br />(only used for spectra from NAP and LCG) | 0<br />1<br />None | no ATR correction<br />ATR correction was applied<br />not relevant / not recorded |
| **BaselineCorrection** | Flag if spectrum was baseline corrected<br />(only used for spectra from NAP and LCG) | 0<br />1<br />None | no baseline correction<br />baseline correction was applied<br />not relevant / not recorded |
| **x_unit** | unit of the x values | nm<br />cm-1 | wavelength in nanometers<br />wavenumber (Raman shift) in cm⁻¹ |
| **y_unit** | unit of the y values | A<br />Intensity | Absorbance for ATR spectra<br />Arbitrary unit of Raman counts |

---

### Polymer guide
| Polymer        | Product_ID | Supplier | Specifications          |         
| -------------- | ---------- | -------- | ----------------------- |
| (01) LDPE      | CRT102.50  | Carat    | without stabilizers     |
| (02) HDPE      | CRT103.50  | Carat    | without stabilizers     |
| (03) PP        | CRT200.00  | Carat    | homo polymer            |
| (04) PP        | CRT250.00  | Carat    | post consumer recyclate |
| (05) PS        | CRT300.00  | Carat    | GPPS                    |
| (06) PET       | CRT401.00  | Carat    | crystalline             |
| (07) PET       | CRT451.00  | Carat    | flakes ex bottles       |
| (08) PLA       | CRT901.00  | Carat    | biopolymer              |
| (09) PET       | bottle     | Joao     | post consumer           |
| (10) HDPE      | bottle     | n/a      | post consumer           |
| (insitu 01) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 02) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 03) PP | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 04) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 05) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 07) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 08) PP | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 09) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 10) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
| (insitu 12) PE | n/a        | n/a      | plastic piece collected in situ in the marine environment for biofilm and degradation study |
