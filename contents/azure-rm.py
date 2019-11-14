import azure.common
import argparse
import os
import json
import sys

from azure.storage.blob import BlockBlobService

parser = argparse.ArgumentParser(description='Azure storage LS.')
parser.add_argument('container', help='Azure Container Name')
parser.add_argument('prefix', help='Prefix')
parser.add_argument('blob_path', help='Blob Path')
args = parser.parse_args()

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

blockblob_service = BlockBlobService(account_name, access_key, endpoint_suffix=endpoint_suffix)

logs = list()

if not args.blob_path:
    # removing a list
    if not prefix:
        generator = blockblob_service.list_blobs(args.container)
    else:
        generator = blockblob_service.list_blobs(args.container,prefix=prefix)

    for blob in generator:

        logs.append("Removing " + blob.name + " from container " + args.container) 
        blockblob_service.delete_blob(args.container,blob.name)
else:
    # removing a file
    if blockblob_service.exists(args.container,args.blob_path):
        logs.append("Removing " + args.blob_path + " from container " + args.container)
        blockblob_service.delete_blob(args.container,args.blob_path)
    else:
        print("Blob doesn't exists")
        sys.exit(1) 
    

logs.append('Finish sucessfully')

json_response = json.dumps(logs) 
print(json_response)