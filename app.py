from pathlib import Path
import pandas as pd

from app_utils import sidebar_filters, new_chap, df_expander
from plots import spectra_plot, metadata_viewer

import streamlit as st
st.set_page_config(layout="wide")

data_root = 'spectra/'

@st.cache_data()
def load_specs(df, convert_wavelength=True):
    spectra = pd.DataFrame()
    for _, row in df.drop(columns=['Polymer_ID', 'file_legacy', 'LocationDescription', 'Country', 'LAT',
       'LON', 'spec_hash', 'x_unit', 'y_unit']).iterrows():
        spectrum = pd.read_csv(data_root+row.file, skiprows=0, header=0)
        if convert_wavelength & ('nm' in spectrum.columns):
            spectrum.nm = wavelength_to_wavenumber(spectrum.nm)
            spectrum = spectrum.rename(columns={'nm': 'cm-1'})

        spectrum = pd.concat([spectrum, pd.DataFrame([row.values]*spectrum.shape[0], columns=row.index)], axis=1)
        spectra = pd.concat([spectra, spectrum], axis=0, ignore_index=True)
    return spectra


@st.cache_data()
def count_measurements_per_sample(df):
    gd = df.groupby(['Region', 'Campaign', 'State', 'Treatment', 'Exposure_days', 'Polymer_ID', 'Polymer', 'Analysis', 'Supplier', 'Product_ID', 'Specifications']).size()
    gf = gd.unstack(['Analysis', 'Treatment']).reset_index()
    gf.columns = [' '.join(col) for col in gf.columns.values]
    gf.columns = gf.columns.str.rstrip() # type: ignore
    return gf


def wavelength_to_wavenumber(w, excitation=532.0):
    '''
    Convert x-values of Raman spectra measured in
    wavelength [nm] to Ramanshift wavenumber [cm-1].
    :param w: x-values of wavelength [nm], array-like
    :param excitation: laser excitation wavelength [nm], float
    :return: x-values of wavenumber [cm-1], array-like
    '''
    return 1e7 / excitation - 1e7 / w

def main():
    col1, col2 = st.columns([3,1])
    col2.image('media/MPX_logo.png', width=300)
    col1.title('MicroPlastiX - Weathered polymer and biofilm spectra')
    col1.markdown('''
                  *Authors:*
                  - [Robin Lenz](https://orcid.org/0000-0003-4156-7380)
                  - [Franziska Fischer](https://orcid.org/0000-0002-2317-6784)
                  - [Melinda Arnold](https://www.ipfdd.de/de/forschung/institut-makromolekulare-chemie/zentrum-makromolekulare-strukturanalyse/spektroskopie-mikroplastik/mitarbeiter/)
                  - [José Manuel Andrade-Garda](https://orcid.org/0000-0003-1020-5213)
                  - [Soledad Norberta Muniategui Lorenzo](https://orcid.org/0000-0001-5946-3366)
                  - [Dieter Fischer](https://www.ipfdd.de/de/organisation/organigramm/personal-homepages/dr-dieter-fischer/)
                  ''')
    new_chap('Introduction')
    col1, _, col2 = st.columns([3,1,2])
    col1.markdown('''
                This app allows you to explore the **weathered polymer and biofilm spectra** measured in the MicroPlastiX project.
                
                > Project MicroPlastiX's Task 4.1 (formerly Task 3.4) examines the biofouling and colonization dynamics of plastic fragments.

                In *in situ* experiments, plastic sheets of **10 different polymers** were deployed in the marine environment across **five geographical locations**.
                Their immersion in stainless steel cages for different intervals, over four seasons, imitates real-world exposure.
                            ''')
    col1.image('media/MPX_locations.png', caption='Locations of the experiments (note: coordinates are not exact, but you find the exact locations in the metadata)', use_column_width=True)
    col1.markdown('''
                Sheets, retrieved after their deployment period, were spectroscopically analysed using **microATR-FTIR** and **micro-Raman** techniques.
                Spectra were obtained from the weathered surface of the sheets, and from the biofilm layer that had developed on the surface.
                The raw data is available in the [spectra](spectra/) folder. Additionally, the [metadata](metadata.json) is available as a JSON file.
                This app reads the metadata JSON file and loads spectra from the folder. By using the filters on the left, you can select which spectra to load.
                The loaded spectra are displayed in the plot below. You can pan, zoom and hover over the plot to see the exact values of the spectra and all relevant metadata.
                Use the download button below the plot to download the selected spectra as a CSV file.
                ''')
    col2.video('media/in-situ/Cage deployment (video: Joao Frias).mp4', start_time=2)
    pics = [p.as_posix() for p in Path('media/in-situ').glob('*.*') if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    caps = [Path(p).stem for p in pics]
    with col2.expander('Pictures from the in situ experiments'):
        st.image(pics, caption=caps, width=400, use_column_width=True)  # type: ignore

    new_chap('Data availability and description')
    col1, col2, col3, col4 = st.columns(4)
    raw_data_checkbox = col4.checkbox('Show raw data')
    metadata_df = pd.read_json('metadata.json', orient='table')
    summary_df = count_measurements_per_sample(metadata_df)
    metadata_df_filtered, filters = sidebar_filters(metadata_df)

    if raw_data_checkbox:
        data_root = st.text_input('Load spec data from here:', 'spectra/')
        df_expander(summary_df, "Summary of number of spectra available in the dataset (DataFrame name: summary_df)")
        df_expander(metadata_df, "All measurements (DataFrame name: metadata_df)")
        df_expander(metadata_df_filtered, "Loaded measurements (DataFrame name: metadata_df_filtered)")
    convert = st.sidebar.checkbox('Convert wavelength [nm] to wavenumber [cm-1]')
    spectra = load_specs(metadata_df_filtered, convert)
    if raw_data_checkbox:
        df_expander(spectra, "Loaded spectra (DataFrame name: spectra)")
    
    col1.metric(f'Total samples available: ', f"{metadata_df.groupby(['Region', 'Campaign', 'State', 'Exposure_days', 'Polymer_ID']).ngroups}",
                f"{metadata_df.fillna({'Replicate': 'A'}).groupby(['Region', 'Campaign', 'State', 'Exposure_days', 'Polymer_ID', 'Replicate']).ngroups} (incl. replicates)")
    col2.metric(f'Measured Raman Spectra: ', f'{(metadata_df.Analysis == "Raman").sum()}')
    col3.metric(f'Measured ATR Spectra: ', f'{(metadata_df.Analysis == "ATR").sum()}')

    if col4.checkbox('Show detailed summary of measurements'):
        region = col4.radio('Region:', metadata_df.Region.unique())
        treatment = col4.radio('Before or after biofilm removal?', metadata_df.Treatment.unique()[::-1])
        analysis = col4.radio('Show counts of:', metadata_df.Analysis.unique()[::-1])
        col4.markdown(f':arrow_left: At the moment, the table lists the number of **{analysis} spectra** available from the **{region} region**, where **{"biofilm was removed" if treatment == "nobio" else "biofilm was not removed"}**.')
        col4.markdown('Use the controls above to change this.')
        col1.write(metadata_viewer(summary_df, analysis, treatment, region)) # type: ignore

    st.markdown('---')
    with st.expander('Show metadata guide'):
        st.markdown('''
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
                    ''', unsafe_allow_html=True)
    with st.expander('Show spectra acquisition parameters'):
        st.markdown('''
                    [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8313017.svg)](https://doi.org/10.5281/zenodo.8313017)
                    ### Raman spectra
                    Raman spectra have been measured with a **Witec Alpha 300R** confocal Raman microscope.
                    - Laser: 532 nm
                    - Laser power: 5 mW
                    - Objectiv: 20x
                    - Integration time: 0.5 s
                    - Accumulation number: 50
                    ''')
        st.markdown('''
                    ### ATR-FTIR spectra
                    ATR spectra have been measured with a **Perkin Elmer Spotlight 400** FTIR microscope with a Germanium ATR appendage or a **Bruker Hyperion 2000** with Vertex 70.
                    - Range: 4000-600 cm-1
                    - Resolution: 4 cm^-1^
                    - scans: 100
                    ''')

    new_chap('Data viewer')
    st.markdown('''
                The plot below shows the spectra that have been loaded.
                - use the filters on the left to select which spectra to load
                - pan and zoom to explore the spectra
                - activate the ruler to better compare peaks across spectra (this might be slower to load: hover over a position and wait for the ruler to appear)
                - use the legend to highlight individual spectra (hold shift while clicking to select multiple)
                ''')
    if spectra.shape[0] == 0:
        st.warning('No spectra found. Please adjust filters.')
    else:
        if convert & ('nm' in metadata_df_filtered.x_unit.values):
            st.info('Spectra have been converted from wavelength [nm] to wavenumber [cm-1].')
        ruler = st.checkbox('Show ruler (possibly slow)', value=False)
        spec_viewer = spectra_plot(spectra, x=spectra.columns[0], y=spectra.columns[1], color='file', ruler=ruler)
        st.altair_chart(spec_viewer, use_container_width=True) # type: ignore
        
        # ## get selected spectra using streamlit-vega-lite  # Can't get this to work with current version of streamlit and altair
        # from streamlit_vega_lite import altair_component
        # event_dict = altair_component(spec_viewer)
        # st.write(event_dict)
        # selected_specs = event_dict.get('file')
        # if selected_specs:
        #     spectra = spectra.loc[spectra.file.isin(selected_specs)]
            
    st.download_button(
        label="Download displayed spectra as CSV",
        data=spectra.to_csv().encode('utf-8'),
        file_name='spectra.csv',
        mime='text/csv',
        disabled=spectra.shape[0] == 0,
    )


if __name__ == '__main__':
    main()
    