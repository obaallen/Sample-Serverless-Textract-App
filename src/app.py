import os
import json, decimal
import boto3
import urllib.parse
from boto3.dynamodb.conditions import Key, Attr

client = boto3.resource('dynamodb')
textract = boto3.client('textract')

tableName = os.environ.get('TABLE_NAME')

def handler(event, context):

  table = client.Table(tableName)

  print(table.table_status)
 
  key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
  bucket = event['Records'][0]['s3']['bucket']['name']
  
  response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': bucket,
            'Name': key
        }
    })
    
  fullText = ""
  
  for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        fullText = fullText + item["Text"] + '\n'
  
  print(fullText)

  table.put_item(Item= {
    'id': key,
    'text': fullText
    })

  
  return 
