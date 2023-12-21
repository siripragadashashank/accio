
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import time
from datetime import datetime
import pickle
import itertools
import plotly.express as px
from apps.legal.plot_setup import finastra_theme
from apps.legal.download_data import Data
import sys

import metadata_parser

from pathlib import Path
import os



####### CACHED FUNCTIONS ######
@st.cache(show_spinner=False, suppress_st_warning=True)
def filter_company_data(df_company, esg_categories, start, end):
    #Filter E,S,G Categories
    comps = []
    for i in esg_categories:
        X = df_company[df_company[i] == True]
        comps.append(X)
    df_company = pd.concat(comps)
    # df_company = df_company[(df_company.DATE >= start) &
    #                         (df_company.DATE <= end)]
    df_company = df_company[df_company.DATE.between(start, end)]
    return df_company


@st.cache(show_spinner=False, suppress_st_warning=True,
          allow_output_mutation=True)
def load_data(start_data, end_data):
    data = Data().read(start_data, end_data)
    companies = data["data"].Organization.sort_values().unique().tolist()
    companies.insert(0,"Select a Company")
    return data, companies


@st.cache(show_spinner=False,suppress_st_warning=True)
def filter_publisher(df_company,publisher):
    if publisher != 'all':
        df_company = df_company[df_company['SourceCommonName'] == publisher]
    return df_company


def get_melted_frame(data_dict, frame_names, keepcol=None, dropcol=None):
    if keepcol:
        reduced = {k: df[keepcol].rename(k) for k, df in data_dict.items()
                   if k in frame_names}
    else:
        reduced = {k: df.drop(columns=dropcol).mean(axis=1).rename(k)
                   for k, df in data_dict.items() if k in frame_names}
    df = (pd.concat(list(reduced.values()), axis=1).reset_index().melt("date")
            .sort_values("date").ffill())
    df.columns = ["DATE", "ESG", "Score"]
    return df.reset_index(drop=True)


def filter_on_date(df, start, end, date_col="DATE"):
    
    '''
    df = df[pd.to_datetime((df[date_col]) >= pd.to_datetime(start)) &
            pd.to_datetime((df[date_col]) <= pd.to_datetime(end))]'''
    return df


def get_clickable_name(url):
    try:
        T = metadata_parser.MetadataParser(url=url, search_head_only=True)
        title = T.metadata["og"]["title"].replace("|", " - ")
        return f"[{title}]({url})"
    except:
        return f"[{url}]({url})"


def main(start_data, end_data):
    ###### CUSTOMIZE COLOR THEME ######
    alt.themes.register("finastra", finastra_theme)
    alt.themes.enable("finastra")
    violet, fuchsia = ["#694ED6", "#C137A2"]




    # Streamlit app title and introduction
    st.title('ESG Investing Insights 🌱💼')
    st.write(
        "Environmental, Social, & Governance (ESG) investing has rapidly gained popularity in the world of finance. "
        "The idea is to invest in companies that are sustainable, particularly in the 3 ESG categories:"
    )
    st.write(
        "- **Environmental:** Issues such as climate change and pollution 🌍\n"
        "- **Social:** Issues around workplace practices and human capital 👥\n"
        "- **Governance:** Issues such as executive pay, accounting, and ethics 🏛️"
    )

    # Information about ESG research
    st.write(
        "There has been a tremendous amount of research around ESG investing. Harvard Law School Forum on Corporate Governance "
        "published a paper titled 'ESG Matters' in which they studied companies with particularly high ESG scores compared to "
        "those with low scores with the following conclusions:"
    )

    # ESG research conclusions
    st.write(
        "- Higher ESG is associated with higher profitability and lower volatility 💹\n"
        "- High ESG scoring companies tend to be good allocators of capital 💰\n"
        "- Good ESG companies generally have higher valuations, EVA growth, size, and returns 📈"
    )

    # Role of the Legal Team
    st.write(
        "The organization's legal team plays a crucial role in ESG investing. They are responsible for ensuring that the "
        "investment decisions align with legal and regulatory standards related to environmental practices, social responsibility, "
        "and governance. This includes assessing and mitigating legal risks associated with ESG factors."
    )

    # Add a link to the Harvard Law School Forum on Corporate Governance
    st.markdown("[Read the full paper: ESG Matters](https://corpgov.law.harvard.edu/2021/09/02/esg-matters/) 📄")




    ###### SET UP PAGE ######
    '''
    icon_path = os.path.join(".", "raw", "esg_ai_logo.png")
    st.set_page_config(page_title="ESG AI", page_icon=icon_path,
                    layout='centered', initial_sidebar_state="collapsed")
    _, logo, _ = st.columns(3)
    logo.image(icon_path, width=200)
    style = ("text-align:center; padding: 0px; font-family: arial black;, "
             "font-size: 400%")
    title = f"<h1 style='{style}'>ESG<sup>AI</sup></h1><br><br>"
    st.write(title, unsafe_allow_html=True)'''


    ###### LOAD DATA ######
    with st.spinner(text="Fetching Data..."):
        data, companies = load_data(start_data, end_data)
    df_conn = data["conn"]
    df_data = data["data"]
    embeddings = data["embed"]


    ####### CREATE SIDEBAR CATEGORY FILTER######
    st.sidebar.title("Filter Options")
    date_place = st.sidebar.empty()
    esg_categories = st.sidebar.multiselect("Select News Categories",
                                            ["E", "S", "G"], ["E", "S", "G"])
    pub = st.sidebar.empty()
    num_neighbors = st.sidebar.slider("Number of Connections", 1, 20, value=8)





    ###### RUN COMPUTATIONS WHEN A COMPANY IS SELECTED ######
    company = st.selectbox("Select a Company to Analyze", companies)
    if company and company != "Select a Company":
        ###### FILTER ######
        df_company = df_data[df_data.Organization == company]
        diff_col = f"{company.replace(' ', '_')}_diff"
        esg_keys = ["E_score", "S_score", "G_score"]
        esg_df = get_melted_frame(data, esg_keys, keepcol=diff_col)
        ind_esg_df = get_melted_frame(data, esg_keys, dropcol="industry_tone")
        tone_df = get_melted_frame(data, ["overall_score"], keepcol=diff_col)
        ind_tone_df = get_melted_frame(data, ["overall_score"],
                                       dropcol="industry_tone")


        ###### DATE WIDGET ######
        start = df_company.DATE.min()
        end = df_company.DATE.max()
        selected_dates = date_place.date_input("Select a Date Range",
            value=[start, end], min_value=start, max_value=end, key=None)
        time.sleep(0.8)  #Allow user some time to select the two dates -- hacky :D
        start, end = selected_dates


        ###### FILTER DATA ######
        df_company = filter_company_data(df_company, esg_categories,
                                         start, end)
        esg_df = filter_on_date(esg_df, start, end)
        ind_esg_df = filter_on_date(ind_esg_df, start, end)
        tone_df = filter_on_date(tone_df, start, end)
        ind_tone_df = filter_on_date(ind_tone_df, start, end)
        date_filtered = filter_on_date(df_data, start, end)


        ###### PUBLISHER SELECT BOX ######
        publishers = df_company.SourceCommonName.sort_values().unique().tolist()
        publishers.insert(0, "all")
        publisher = pub.selectbox("Select Publisher", publishers)
        df_company = filter_publisher(df_company, publisher)


        ###### DISPLAY DATA ######
        URL_Expander = st.expander(f"View {company.title()} Data:", True)
        URL_Expander.write(f"### {len(df_company):,d} Matching Articles for " +
                           company.title())
        display_cols = ["DATE", "SourceCommonName", "Tone", "Polarity",
                        "NegativeTone", "PositiveTone"]  #  "WordCount"
        URL_Expander.write(df_company[display_cols])

        ####
        URL_Expander.write(f"#### Sample Articles")
        link_df = df_company[["DATE", "URL"]].head(3).copy()
        # link_df["URL"] = link_df["URL"].apply(lambda R: f"[{R}]({R})")
        link_df["ARTICLE"] = link_df.URL.apply(get_clickable_name)
        link_df = link_df[["DATE", "ARTICLE"]].to_markdown(index=False)
        URL_Expander.markdown(link_df)
        ####


        ###### CHART: METRIC OVER TIME ######
        st.markdown("---")
        col1, col2 = st.columns((1, 3))

        metric_options = ["Tone", "NegativeTone", "PositiveTone", "Polarity",
                          "ActivityDensity", "WordCount", "Overall Score",
                          "ESG Scores"]
        line_metric = col1.radio("Choose Metric", options=metric_options)

        if line_metric == "ESG Scores":
            # Get ESG scores
            esg_df["WHO"] = company.title()
            ind_esg_df["WHO"] = "Industry Average"
            esg_plot_df = pd.concat([esg_df, ind_esg_df]
                                    ).reset_index(drop=True)
            esg_plot_df.replace({"E_score": "Environment", "S_score": "Social",
                                 "G_score": "Governance"}, inplace=True)

            metric_chart = alt.Chart(esg_plot_df, title="Trends Over Time"
                                       ).mark_line().encode(
                x=alt.X("yearmonthdate(DATE):O", title="DATE"),
                y=alt.Y("Score:Q"),
                color=alt.Color("ESG", sort=None, legend=alt.Legend(
                    title=None, orient="top")),
                strokeDash=alt.StrokeDash("WHO", sort=None, legend=alt.Legend(
                    title=None, symbolType="stroke", symbolFillColor="gray",
                    symbolStrokeWidth=4, orient="top")),
                tooltip=["DATE", "ESG", alt.Tooltip("Score", format=".5f")]
                )

        else:
            if line_metric == "Overall Score":
                line_metric = "Score"
                tone_df["WHO"] = company.title()
                ind_tone_df["WHO"] = "Industry Average"
                plot_df = pd.concat([tone_df, ind_tone_df]).reset_index(drop=True)
            else:
                df1 = df_company.groupby("DATE")[line_metric].mean(
                    ).reset_index()
                df2 = filter_on_date(df_data.groupby("DATE")[line_metric].mean(
                    ).reset_index(), start, end)
                df1["WHO"] = company.title()
                df2["WHO"] = "Industry Average"
                plot_df = pd.concat([df1, df2]).reset_index(drop=True)
            metric_chart = alt.Chart(plot_df, title="Trends Over Time"
                                     ).mark_line().encode(
                x=alt.X("yearmonthdate(DATE):O", title="DATE"),
                y=alt.Y(f"{line_metric}:Q", scale=alt.Scale(type="linear")),
                color=alt.Color("WHO", legend=None),
                strokeDash=alt.StrokeDash("WHO", sort=None,
                    legend=alt.Legend(
                        title=None, symbolType="stroke", symbolFillColor="gray",
                        symbolStrokeWidth=4, orient="top",
                        ),
                    ),
                tooltip=["DATE", alt.Tooltip(line_metric, format=".3f")]
                )
        metric_chart = metric_chart.properties(
            height=340,
            width=200
        ).interactive()
        col2.altair_chart(metric_chart, use_container_width=True)

    
        ###### CHART: ESG RADAR ######
        


def app():
#if __name__ == "__main__":
    root = Path(__file__).parent.parent.parent
    data_path = os.path.join(root, 'apps', 'legal', 'Data')

    args = sys.argv
    if len(args) != 3:
        start_data = "dec30"
        end_data = "jan12"
    else:
        start_data = args[1]
        end_data = args[2]

    

    if f"{start_data}_to_{end_data}" not in os.listdir(data_path):
        print(f"There isn't data for {dir_name}")
        raise NameError(f"Please pick from {os.listdir('Data')}")
        sys.exit()
        st.stop()
    else:
        main(start_data, end_data)
    alt.themes.enable("default")


# one_month, ten_days
