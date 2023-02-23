from flask import Flask, render_template, request
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
from email_analysis_helper import EmailSelectForm, pull_random_docs, store_emails, read_emails, process_document, make_extraction_dictionary
# scrape_all_emails, make_extraction_dictionary, process_document # , process_document, make_extraction_dictionary, scrape_all_emails

app = Flask(__name__)
app.config['SECRET_KEY'] = "trailblazer"

## Home page
@app.route('/')
def home():
    return render_template("index.html")

## Email Analysis Tool
@app.route('/email_analysis', methods=['GET', 'POST'])
def email_analysis():
    analysis_output = ""
    extraction_dictionary = {}
    email_choice_form = EmailSelectForm()
    show_sem_analysis = False
    if email_choice_form.email_buttons.data:
        random_emails = read_emails()["emails_to_pick_from"]
        chosen_email = list(random_emails.keys())[int(email_choice_form.email_buttons.data)]
        chosen_email_text = random_emails[chosen_email]
        analysis_output = process_document(chosen_email_text)
        show_sem_analysis = email_choice_form.sem_analysis_check.data
        if analysis_output != "":
            extraction_dictionary = make_extraction_dictionary(analysis_output)
    else:
        random_emails = pull_random_docs("email_archive", sample_size=3)
        store_emails(emails_to_pick_from=random_emails, email_to_process="")
        chosen_email_text = ""
    return render_template(
        "email_analysis.html",
        random_emails=random_emails,
        email_choice_form=email_choice_form,
        analysis_output=analysis_output,
        extraction_dictionary=extraction_dictionary,
        chosen_email_text=chosen_email_text,
        show_sem_analysis=show_sem_analysis)

## ML Toybox
@app.route('/ml_toybox')
def ml_toybox():
    return render_template("ml_toybox.html")

## Rules Toybox
@app.route('/rules_toybox')
def rules_toybox():
    return render_template("rules_toybox.html")