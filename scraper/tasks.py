#import celery
from __future__ import absolute_import, unicode_literals
from twitter_data_extractor.celery import app

from scraper.models import Result, Job, CustomUser
from datetime import datetime
import twint
from django.core.files import File
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pandas as pd


@app.task
def data_extract(job_id, user_id):
    """ Twint configuration and data extraction"""
    c = twint.Config()
    job = Job.objects.get(pk=job_id)  # get job object

    c.Search = job.keyword
    c.Limit = job.limit
    c.Lang = job.language
    c.Verified = job.verified
    # c.Since = datetime.strftime(job.since, "%Y-%m-%d %H:%M:%S")  # convert to string
    # c.Until = datetime.strftime(job.until, "%Y-%m-%d %H:%M:%S")  # convert to string
    c.Store_csv = True  # Store as csv
    c.Output = f"{job.keyword}_{job.id}.csv"
    twint.run.Search(c)
    data_save.delay(job.id, user_id)  # save the result as result object


@app.task
def data_save(job_id, user_id):
    """ Save data as result object after removing empty columns.
     Upload file to location /media/DataFiles/f"{job.keyword}_{job.id}.csv" """
    result = Result()
    job = Job.objects.get(pk=job_id)
    result.job = job
    file_name = f"{job.keyword}_{job.id}"
    df = pd.read_csv(f"{file_name}.csv")
    df2 = df.dropna(how='all', axis=1)
    df2.to_csv(f"{file_name}.csv")

    # Convert to json
    if job.output_type == "json":
        df2.to_json(f"{file_name}.json", orient="split")
        # df2.to_json  ---> https://www.w3resource.com/pandas/dataframe/dataframe-to_json.php
        f = open(f"{file_name}.json", 'r')
        result.result_file.save(f"{file_name}.json", File(f), save=True)
        os.remove(f"{file_name}.json")
    else:
        f = open(f"{file_name}.csv", 'r')
        result.result_file.save(f"{file_name}.csv", File(f), save=True)

    os.remove(f"{file_name}.csv")
    result.save()
    result = Result.objects.get(job=job_id)
    data_email_send.delay(result.id, user_id)  # send the result via email


@app.task
def data_email_send(result_id, user_id):
    """ Send result as email"""
    user = CustomUser.objects.get(pk=user_id)
    result = Result.objects.get(pk=result_id)
    email = user.email
    subject, from_email, to = 'Twitter data extraction result', 'amithah.nithin@gmail.com', email

    html_content = render_to_string('scraper/email.html', {'user': user})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_file(f"{result.result_file.path}")
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("email sent successfullly")
