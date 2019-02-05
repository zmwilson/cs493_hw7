import boto3
import os

def recursiveUpload(directory, bucket, client, destination):
	for root, dirs, files in os.walk(directory):
		for filename in files:
			#fix slashes and join paths to create correct S3 structure
		    local_path = os.path.join(root, filename).replace('\\', '/')
		    relative_path = os.path.relpath(local_path, directory).replace('\\', '/')
		    s3_path = os.path.join(destination, relative_path).replace('\\', '/')

		    client.upload_file(local_path, 'zmwilson.cs493bucket', s3_path)

# Session for S3FullAccess clients
# Bucket and Client setup
session = boto3.Session(profile_name='s3-access')
s3 = session.resource('s3')
client = session.client('s3')
bucket = s3.Bucket('zmwilson.cs493bucket')

command = raw_input("Specify a CRUD operation: (C)reate or Update, (R)ead, or (D)elete\n")

#create of update a file in S3
if(command.lower() == "c"):
	upload_type = raw_input("Would you like to upload a song, album, or artist?\n")
	if(upload_type.lower() == "song"):
		input_file = raw_input("Specify a song file to upload to S3.\n")
		file_path = raw_input("Specify a song name for S3.\n")
		s3.Object('zmwilson.cs493bucket', file_path).put(Body=open(input_file, 'rb'))

	if(upload_type.lower() == "album"):
		input_file = raw_input("Specify an album directory to upload to S3.\n")
		file_path = raw_input("Specify an album name for S3.\n")
		recursiveUpload(input_file, bucket, client, file_path)

	if(upload_type.lower() == "artist"):
		input_file = raw_input("Specify an artist directory to upload to S3.\n")
		file_path = raw_input("Specify an artist name for S3.\n")
		recursiveUpload(input_file, bucket, client, file_path)

#list all files or directories in S3
if(command.lower() == "r"):
	print("Contents of bucket:\n")
	for o in bucket.objects.all():
		print(o.key)
#delete specified file from S3
if(command.lower() == "d"):
	input_file = raw_input("Specify a file or directory to delete.\n")
	for k in bucket.objects.filter(Prefix=input_file):
		k.delete()