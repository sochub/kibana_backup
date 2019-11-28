# KIBACKUP

![](https://image.flaticon.com/icons/svg/1983/1983619.svg =250x250)

With this script you can make a backup copy of different instances of KIBANA (just saved object). Basically connects to the API and then saves the data in an S3. You need the following environment variables to function.

###Tables
                    
ENV NAME  | Detail
------------- | -------------
AWS_SESSION_TOKEN  | aws session token
AWS_ACCESS_KEY_ID  | aws access key id
AWS_SECRET_ACCESS_KEY | aws secret access key
AWS_REGION | aws region
BUCKET | s3 bucket name
BUCKET_KEY | s3 bucket path to save the file

###Tables

How to RUN >  make sure that you have the ENV in your machine, then just make: 

```
python3 kibackup.py -k http://localhost:5601
```

The scripts use: 

-k KIBANA URL
-p password for kibana (optional)
-u user for kibana (optional)
