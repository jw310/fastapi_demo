import os

from google.cloud import storage


key_path = os.path.join(os.getcwd(), 'llm/key')
# print(key_path)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{key_path}/xxx.json'


client = storage.Client()
# blobs = client. list_blobs("xxxx", prefix="product_info/")
# for blob in blobs:
#   print (blob. name)

# bucket = client. bucket("xxx")
# blob = bucket.blob("xxx.csv")
# with open ("./xxx.csv", "wb") as f:
#     blob.download_to_file(f)