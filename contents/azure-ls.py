import argparse
import os
import json

from azure.storage.blob import BlockBlobService

parser = argparse.ArgumentParser(description='Azure storage LS.')
parser.add_argument('container', help='Azure Container Name')
parser.add_argument('prefix', help='Prefix')
args = parser.parse_args()

# endpoint_suffix = "core.chinacloudapi.cn"
endpoint_suffix = None
account_name = None
access_key = None
prefix = None

if "RD_CONFIG_ACCOUNT_NAME" in os.environ:
    account_name = os.environ["RD_CONFIG_ACCOUNT_NAME"]
if "RD_CONFIG_ACCESS_KEY" in os.environ:
    access_key = os.environ["RD_CONFIG_ACCESS_KEY"]
if "RD_CONFIG_PREFIX" in os.environ:
    prefix = os.environ["RD_CONFIG_PREFIX"]
if "RD_CONFIG_ENDPOINT_SUFFIX" in os.environ:
    endpoint_suffix = os.environ["RD_CONFIG_ENDPOINT_SUFFIX"]

# account = CloudStorageAccount(account_name, access_key)
# blockblob_service = account.create_block_blob_service()
blockblob_service = BlockBlobService(account_name, access_key, endpoint_suffix=endpoint_suffix)

if not prefix:
    generator = blockblob_service.list_blobs(args.container)
else:
    generator = blockblob_service.list_blobs(args.container, prefix=prefix)

result = list()


for blob in generator:

    result.append({'name': blob.name,
                   'last_modified':blob.properties.last_modified.strftime("%Y-%m-%d %H:%M:%S") ,
                   'content_length':blob.properties.content_length,
                   'blob_type':blob.properties.blob_type,
                   'content_type':blob.properties.content_settings.content_type,
                   'content_md5':blob.properties.content_settings.content_md5,
                   'etag':blob.properties.etag})

json_response = json.dumps(result) 
print(json_response)

