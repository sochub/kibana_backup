#!/usr/bin/env python3

import requests
import argparse
import json
import sys
import gzip
import datetime
import boto3
import logging
import os
import io
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth


def kibackup(kibana_url, user, password):
    # get kibana objects from API
    url = "%s/api/saved_objects/_find" % (args.kibana_url.rstrip("/"),)
    r = requests.get(url, auth=(user, password), verify=False,
                                     params={'per_page': 10000,'type':['config','search','dashboard','visualization','index-pattern']})
    r_objects = r.json()['saved_objects']
    for obj in r_objects:
        get_prefix = json.dumps(obj)
        json_trans = json.loads(get_prefix)
        name_prefix = json_trans["type"]
        data = obj
        print(data)
        logging.info("dump data to s3 processor")
        # send objects to S3 processor
        tos3bucket(data, name_prefix)

def tos3bucket(data, name_prefix):
    # This take the data form the handler and put a bulk of events into a 
    # s3 bucket with gzip file. 
    awsauth = AWS4Auth(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], os.environ['AWS_REGION'],
                       'es',
                       session_token=os.environ['AWS_SESSION_TOKEN'])
    buf = io.BytesIO()
    s3 = boto3.resource('s3', region_name=os.environ['AWS_REGION'])
    year = datetime.datetime.now().strftime("%Y")
    month = datetime.datetime.now().strftime("%m")
    day = datetime.datetime.now().strftime("%d")
    nowD = datetime.datetime.now().strftime("%Y%m%d")
    nowT = datetime.datetime.now().strftime("%H%M%S")
    
    filename = name_prefix + nowD + 'T'+ nowT + ".log.gz"

    with gzip.GzipFile(fileobj=buf, mode='wb') as gfh:
            with io.TextIOWrapper(gfh, encoding='utf-8') as wrapper:
                wrapper.write(json.dumps(data, ensure_ascii=False, default=None))
    buf.seek(0)
    bucketID = os.environ['BUCKET']
    bucketKEY = os.environ['BUCKET_KEY']
    key = bucketKEY + '/' + year + '/' + month + '/' + day + '/' + filename
    s3.Bucket(bucketID).put_object(Key=key, Body=buf)
    logging.info("the file was saved on "+bucketID+"/"+key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Backup Kibana saved objects.')
    parser.add_argument(
        '-k', '--kibana-url'
    )
    parser.add_argument(
        '-u', '--user'
    )
    parser.add_argument(
        '-p', '--password'
    )
    args = parser.parse_args()
    kibackup(args.kibana_url, args.user, args.password)
