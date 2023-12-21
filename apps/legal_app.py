import streamlit as st
from apps import news
from apps.legal import esg, landing, upload_and_chat  # , #chat

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


def app():
    tab1, tab2, tab3 = st.tabs(["About", "Legal Genie", "EcoWealth Watch"])  # , "Document Writer"])

    with tab1:
        landing.app()

    with tab2:
        upload_and_chat.app()

    with tab3:
        esg.app()


