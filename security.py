import smtplib

class security():
	def __init__(self):
		self.receiver = 'gui.cabral201@gmail.com'
		self.topic = 'MUSK Security Service'
		self.text = 'Motion Detected'
		self.sender = 'projetosd373@gmail.com'
		self.password = 'projetosel373'
		self.message = '\r\n'.join([ 'From: %s' % self.sender, 'To: %s' % self.receiver, 'Subject: %s' % self.topic, '', '%s' % self.text ])
		self.server = smtplib.SMTP()

	def sendEmail(self):
		self.server.connect('smtp.gmail.com', '587')
		self.server.starttls()
		self.server.login(self.sender, self.password)
		self.server.sendmail(self.sender, self.receiver, self.message)
		self.server.quit()
		return print("[+]The email was send")

	def sendAlert(self):
		print("[+]Send an alert message to user's phone")
