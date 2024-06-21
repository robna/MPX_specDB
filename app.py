from pathlib import Path
import shutil
import pandas as pd
import requests
import tarfile
import zipfile
from io import BytesIO

from app_utils import sidebar_filters, new_chap, df_expander
from plots import spectra_plot, metadata_viewer

import streamlit as st
st.set_page_config(layout="wide")

data_root = Path('data')

media_path = data_root/'media'

md = data_root/'meta'  # metadata directory
mdf = md/'metadata.json'  # metadata file

sp = data_root/'spectra'  # spectra directory
sp.mkdir(parents=True, exist_ok=True) # ensure the directory exists
spf = sp.glob('*.csv')  # spectra files


def radar_tar(doi):
    repo_url = requests.get(f'https://doi.org/{doi}').url
    tar_url = requests.get(repo_url).links['item']['url']
    response = requests.get(tar_url)
    tar = tarfile.open(fileobj=BytesIO(response.content))
    return tar
    

def get_data(doi, mdf=mdf, spf=spf):
    if not mdf.exists() or not any(spf):
        tar = radar_tar(doi)
        dataset_path = f"{doi.replace('/','-')}/data/dataset/"  #  tar file inner path to the dataset uses "-" instead of "/"
        for member in tar.getmembers():
            if member.name.startswith(dataset_path):
                if member.name.endswith('metadata.json'):
                    # Extract metadata.json directly to the md directory
                    member_file = tar.extractfile(member)
                    with open(mdf, 'wb') as f:
                        f.write(member_file.read())
                elif member.name.endswith('spectra.zip'):
                    # Extract spectra.zip content to memory
                    member_file = tar.extractfile(member)
                    spectra_zip_in_memory = BytesIO(member_file.read())
                    with zipfile.ZipFile(spectra_zip_in_memory) as spectra_zip:
                        spectra_zip.extractall(sp)


def refresh_files():
    shutil.rmtree(sp)
    mdf.unlink()
    st.rerun()


@st.cache_data()
def load_specs(df, convert_wavelength=True):
    spectra = pd.DataFrame()
    for _, row in df.drop(columns=['Polymer_ID', 'file_legacy', 'LocationDescription', 'Country', 'LAT',
       'LON', 'spec_hash', 'x_unit', 'y_unit']).iterrows():
        spectrum = pd.read_csv(sp/row.file, skiprows=0, header=0)
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

    doi = st.sidebar.text_input('Dataset DOI:', '10.22000/1820')
    st.sidebar.markdown(f'[>> Go to dataset <<](https://dx.doi.org/{doi})')
    with st.sidebar.status("Downloading data...", expanded=True) as status:
        get_data(doi)
        status.update(label="Download complete!", state="complete", expanded=False)
    
    st.sidebar.button('Reload data', on_click=refresh_files)

    st.sidebar.markdown('---')
    st.sidebar.markdown('[<p align="center"><img src="https://radar4chem.radar-service.eu/radar/image/DmaGuUIxEhpEYXIF/institution-logo.png" alt="https://dx.doi.org/10.22000/1820" height="60"></p>](https://dx.doi.org/10.22000/1820)', unsafe_allow_html=True)
    st.sidebar.markdown('---')
    
    col1, col2 = st.columns([3,1])
    col2.image(str(media_path/'MPX_logo.png'), width=300)
    col1.title('MicroPlastiX - Weathered polymer and biofilm spectra')
    
    with open(md/'authors.md', 'r') as file:
        authors = file.read()
    col1.markdown(authors, unsafe_allow_html=True)
    
    new_chap('Introduction')
    col1, _, col2 = st.columns([3,1,2])
    col1.markdown('''
                This app allows you to explore the **weathered polymer and biofilm spectra** measured in the MicroPlastiX project.
                
                > Project MicroPlastiX's Task 4.1 (formerly Task 3.4) examines the biofouling and colonization dynamics of plastic fragments.

                In *in situ* experiments, plastic sheets of **10 different polymers** were deployed in the marine environment across **five geographical locations**.
                Their immersion in stainless steel cages for different intervals, over four seasons, imitates real-world exposure.
                            ''')
    col1.image(str(media_path/'MPX_locations.png'), caption='Locations of the experiments (note: coordinates are not exact, but you find the exact locations in the metadata)', use_column_width=True)
    col1.markdown('''
                Sheets, retrieved after their deployment period, were spectroscopically analysed using **microATR-FTIR** and **micro-Raman** techniques.
                Spectra were obtained from the weathered surface of the sheets, and from the biofilm layer that had developed on the surface.
                The raw data is available in the [spectra](data/spectra/) folder. Additionally, the [metadata](data/metadata/metadata.json) is available as a JSON file.
                This app reads the metadata JSON file and loads spectra from the folder. By using the filters on the left, you can select which spectra to load.
                The loaded spectra are displayed in the plot below. You can pan, zoom and hover over the plot to see the exact values of the spectra and all relevant metadata.
                Use the download button below the plot to download the selected spectra as a CSV file.
                ''')
    col2.video(str(media_path/'in-situ'/'Cage deployment (video: Joao Frias).mp4'), start_time=2)
    pics = [p.as_posix() for p in (media_path/'in-situ').glob('*.*') if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    caps = [Path(p).stem for p in pics]
    with col2.expander('Pictures from the in situ experiments'):
        st.image(pics, caption=caps, width=400, use_column_width=True)  # type: ignore

    new_chap('Data availability and description')
    col1, col2, col3, col4 = st.columns(4)
    raw_data_checkbox = col4.checkbox('Show raw data')
    metadata_df = pd.read_json(mdf, orient='table')
    summary_df = count_measurements_per_sample(metadata_df)
    metadata_df_filtered, filters = sidebar_filters(metadata_df)

    if raw_data_checkbox:
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
        with open(md/'metadata_guide.md', 'r') as file:
            metadata_guide = file.read()
        st.markdown(metadata_guide, unsafe_allow_html=True)
    with st.expander('Show spectra acquisition parameters'):
        with open(md/'sops.md', 'r') as file:
            sops = file.read()
        st.markdown(sops)

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
    