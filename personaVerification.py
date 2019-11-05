import boto3 as b3

class personaVerification():
	def __init__(self):
		self.name = 0
		self.similarity = 0
		self.confidence = 0
		self.picture = 'img1.jpg'
		self.collectionName = 'collectionTcc'

	def checkFace(self, client):
		face_detected = False
		with open(self.picture, 'rb') as image:
			response = client.detect_faces(Image={'Bytes' : image.read()})
			if(not response['FaceDetails']):
				face_detected = False
			else:
				face_detected = True
		return face_detected, response

	def checkMatches(self, client):
		face_matches = False
		with open(self.picture, 'rb') as image:
			response = client.search_faces_by_image(CollectionId=self.collectionName, Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=95)
			if (not response['FaceMatches']):
				face_matches = False
			else:
				face_matches = True
		return face_matches, response

	def faceMatch(self, client):
		result, resp = self.checkFace(client);
		if(result):
			resu, res = self.checkMatches(client);
			if resu:
				self.name = res['FaceMatches'][0]['Face']['ExternalImageId']
				self.similarity = res['FaceMatches'][0]['Similarity']
				self.confidence = res['FaceMatches'][0]['Face']['Confidence']
			else :
				self.name = 'unknown'
				self.similarity = 0
				self.confidence = 0
			print("[+]Detected Person: " + str(self.name))
			print("[+]Similarity: " + str(self.similarity))
			print("[+]Confidence: " + str(self.confidence))
			print(" ")
		else:
			print("[+]No faces detected")

