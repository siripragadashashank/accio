import streamlit as st
import boto3
import pdfplumber
from io import BytesIO


def get_s3():
    s3 = boto3.resource('s3', aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])
    return s3


def save_file(fl):
    file_name = fl.name
    s3 = get_s3()
    s3.Bucket(st.secrets['AWS_BUCKET_NAME']).put_object(Key=file_name, Body=fl)
    st.write('Success! File Saved!')


def get_files_list():
    s3= get_s3()
    file_names = []
    bucket = s3.Bucket(st.secrets['AWS_BUCKET_NAME'])
    for s3_obj in bucket.objects.all():
        file_names.append(s3_obj.key)
    s3_filename = st.sidebar.radio('Select a file', file_names, index=0)
    return s3_filename


def get_file(s3_filename):
    s3 = get_s3()
    obj = s3.Object(st.secrets['AWS_BUCKET_NAME'], s3_filename)
    fl = obj.get()['Body'].read()
    with pdfplumber.open(BytesIO(fl)) as pdf:
        pages = pdf.pages
        page = pages[0]
        text = page.extract_text().split('\n')
        for txt in text:
            st.write(txt)


def app():
    st.title('Upload ')

    fl = st.sidebar.file_uploader('Upload new file:', type=['pdf', 'docx', 'txt'],
                                  accept_multiple_files=False)

    if fl is not None:
        save_file(fl)
