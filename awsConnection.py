import boto3 as b3

class awsConnection():
	def __init__(self):
		self.awsRekognitionClient = 0
		self.key_id = "*******************"
		self.secret_key = "*******************"
		self.aws_region = "us-west-2"
		#Complete ******** with your credentials
		
	def getRekognitionClient(self):
		self.awsRekognitionClient = b3.client('rekognition', aws_access_key_id = self.key_id, aws_secret_access_key = self.secret_key, region_name = self.aws_region)
		print("[+]Connected to AWS Rekognition")

	
