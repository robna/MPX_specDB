import streamlit as st


def sidebar_filters(df):
    regions = st.sidebar.multiselect('Region', df.Region.unique(), df.Region.unique()[0])
    campaigns = st.sidebar.multiselect('Campaign', df.Campaign.unique(), df.Campaign.unique()[0])
    states = st.sidebar.multiselect('State', df.State.unique(), df.State.unique()[0])
    treatments = st.sidebar.multiselect('Treatment', df.Treatment.unique(), df.Treatment.unique()[0])
    analyses = st.sidebar.radio('Analysis', df.Analysis.unique())
    exposure_days = st.sidebar.multiselect('Exposure_days', df.Exposure_days.unique(), df.Exposure_days.unique()[0])
    polymers = st.sidebar.multiselect('Polymer', df.Polymer.unique(), df.Polymer.unique()[0])
    df = filter_df(df, regions, campaigns, states, treatments, analyses, exposure_days, polymers)
    return df, (regions, campaigns, states, treatments, analyses, exposure_days, polymers)


def filter_df(df, regions, campaigns, states, treatments, analyses, exposure_days, polymers):
    df = df.loc[(df.Region.isin(regions))
                & (df. Campaign.isin(campaigns))
                & (df.State.isin(states))
                & (df.Treatment.isin(treatments))   
                & (df.Analysis == analyses)
                & (df.Exposure_days.isin(exposure_days))
                & (df.Polymer.isin(polymers))
                ]
    return df


def new_chap(title = None):
    st.markdown('___', unsafe_allow_html=True)
    st.text("")  # empty line to make some distance
    if title:
        st.subheader(title)


def df_expander(df, title):
    with st.expander(title):
        st.write(df)
        st.write('Shape: ', df.shape)
        col1, col2 = st.columns([1,3])
        col1.write(df.dtypes.astype(str))
        col2.write(df.describe())
