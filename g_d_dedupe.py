from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import collections

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

	
def main():
	"""Shows basic usage of the Drive v3 API.
	Prints the names and ids of the first 10 files the user has access to.
	"""
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	drive_service = build('drive', 'v3', http=creds.authorize(Http()))

	
	counter = 0
	page_token = None
	list_of_tuples = []
	#dups_dict = collections.defaultdict(int)
	dups_dict = collections.defaultdict(list) 
	
	while True:
		counter = counter + 1
		#check here for the values spaces can have: https://developers.google.com/drive/api/v3/reference/files/list
		
		
		#from api v2, but could still work. Nothing for file deletions in v3 API
		# try:
			# service.files().delete(fileId=file_id).execute()
		# except errors.HttpError, error:
			# print ('An error occurred: %s') % error
		
		#response = drive_service.files().list(q="mimeType!='audio/au'", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
		response = drive_service.files().list(spaces='drive', pageSize=500, fields='nextPageToken, files(id, name, md5Checksum, parents)', pageToken=page_token).execute()
		
		for f in response.get('files', []):
			# Process change
			
			
			list_of_tuples.append((f.get('md5Checksum'), f.get('name')))
			#dups_dict[f.get('md5Checksum')] += 1
			
			print ('Found file: %s (%s) %s' % (f.get('name'), f.get('id'), f.get('md5Checksum')))
		page_token = response.get('nextPageToken', None)
		
		
		#remove this IF if you want to scan through everything
		if counter >= 10:
			break
		
		
		if page_token is None:
			print("this many:" + str(counter))
			break
			
				
		
	for k,v in list_of_tuples:
		dups_dict[k].append(v)
		
	print("\r\n\r\n")
	print("here are the duplicates")
		
	
	for key in dups_dict:
		if len(dups_dict[key]) > 1 and "-checkpoint" not in str(dups_dict[key]):
			print(dups_dict[key])
	


if __name__ == '__main__':
	main()