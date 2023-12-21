import streamlit as st
import pandas as pd
import json
from snowflake.snowpark import Session, FileOperation

# # connect to Snowflake
# with open('creds.json') as f:
#     connection_parameters = json.load(f)
# session = Session.builder.configs(connection_parameters).create()
#
# file = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv"})
# file_df = pd.read_csv(file)
# snowparkDf = session.write_pandas(file_df,
#                                   file.name,
#                                   auto_create_table=True,
#                                   overwrite=True)


stage_nm = 'demo'

conn_param = {
    'user': st.secrets["user"],
    'account': st.secrets["account"],
    'password': st.secrets["password"],
    'database': st.secrets["database"],
    'warehouse': st.secrets["warehouse"],
    'schema': st.secrets["schema"]
}

session = Session.builder.configs(conn_param).create()

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    FileOperation(session).put_stream(input_stream=uploaded_file,
                                      stage_location='@'+stage_nm+'/'+uploaded_file.name,
                                      auto_compress=False)


