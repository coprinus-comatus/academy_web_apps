import json
import requests
import random
import os
import base64
# from bs4 import BeautifulSoup
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
# from nl_api_anonymize_email import anonymize_email

class EmailSelectForm(FlaskForm):
    email_choices = [("0", "Email #1"), ("1", "Email #2"), ("2", "Email #3")]
    email_buttons = RadioField("Email to Process", choices=email_choices)
    sem_analysis_check = BooleanField("Show semantic analysis")
    submit = SubmitField("Process email")


# # Data to send API request
# def read_api_data(api_data_name = "api_data.json"):
#     load_dotenv()
#     api_key = str(os.environ["API_KEY"])
#     api_endpoint = str(os.environ["API_WORKFLOW_ENDPOINT"])
#     return api_key, api_endpoint

# Data to send API request
def read_api_data(api_data_name = "api_data.json"):
    with open(api_data_name, "r") as api_json:
        api_data = json.load(api_json)
    api_key = api_data["api_key"]
    api_endpoint = api_data["api_endpoint"]
    return api_key, api_endpoint

## Convert to Base64
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        string = file.read()
    base64_bytes = base64.b64encode(string)
    base64_string = str(base64_bytes, "utf-8")
    return base64_string

## Sending the document to the API
def process_document(document_to_process):
    api_key, api_endpoint = read_api_data()
    # print(document_to_process)
    # print(encode_file_to_base64(document_to_process))
    response = requests.post(
        url=api_endpoint,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "X-API-KEY": api_key
        },
        json={
            "text": document_to_process
            # "path": f"{document_to_process}",
            # "base64": encode_file_to_base64(document_to_process)
        })
    print(response)
    if str(response) == "<Response [200]>":
        analysis_output = response.json()
        print(analysis_output)
    else:
        analysis_output = ""
    return analysis_output

## Organizing the extractions into a single dictionary
# def make_extraction_dictionary(analysis_output):
#     extraction_dictionary =  {}
#     for extraction in analysis_output["extraction_model"]["extractions"]:
#         template_name = extraction["template"]
#         if template_name not in extraction_dictionary:
#             extraction_dictionary[template_name] = set()
#         for field in extraction["fields"]:
#             if field["name"] == template_name:
#                 extraction_value = field["value"]
#             else:
#                 extraction_value = f"{field['name'].upper()}: {field['value']}"
#             extraction_dictionary[template_name].add(extraction_value)
#     return extraction_dictionary

def make_extraction_dictionary(analysis_output):
    extraction_dictionary =  {}
    for extraction in analysis_output["extraction_model"]["extractions"]:
        template_name = extraction["template"]
        if template_name not in extraction_dictionary:
            extraction_dictionary[template_name] = set()
        for field in extraction["fields"]:
#             extraction = tuple()
            if field["name"] == template_name:
                extraction = ("", field["value"])
#                 extraction_value = field["value"]
            else:
                extraction = (field["name"], field["value"])
#                 extraction_value = f"{field['name'].upper()}: {field['value']}"
#             extraction_dictionary[template_name].add(extraction_value)
            extraction_dictionary[template_name].add(extraction)
    return extraction_dictionary

## Pull random emails
def pull_random_docs(doc_folder, sample_size=3):
    random_docs_dict = {}
    for _, _, files in os.walk(doc_folder):
        try:
            random_file_names = random.sample(files, sample_size)
            for file_name in random_file_names:
                file_path = os.path.join(doc_folder, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    random_docs_dict[file_path] = str(file.read())
                    # random_texts_list.append(str(file.read()))
            return random_docs_dict
        except ValueError:
            print("Not enough files for sample size.")
    return random_docs_dict

## Store emails
def store_emails(emails_to_pick_from, email_to_process, json_file_name="emails_in_page.json"):
    emails_dictionary = {
        "emails_to_pick_from": emails_to_pick_from,
        "email_to_process": email_to_process
    }
    with open(json_file_name, "w", encoding="utf-8") as json_output:
        json.dump(emails_dictionary, json_output)

## Read emails
def read_emails(json_file_name="emails_in_page.json"):
    with open(json_file_name, "r", encoding="utf-8") as json_input:
        emails_dictionary = json.load(json_input)
    return emails_dictionary