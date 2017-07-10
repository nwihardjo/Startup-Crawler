import scrapy
from scrapy_splash import SplashRequest
import csv

def find_text(xpath_value):
	return str(xpath_value).split()[-2]

def find_date(xpath_value):
	str_list = str(xpath_value).split()
	return str_list[-3] + ' ' + str_list[-2]

def clean_string(name):
	"""
	remove non-alphanumeric characters in the 'name' string to give the data to domain name
		args name: string going to be cleaned
	"""
	nameList = list(name)
	while nameList[0].isalnum() == False:
		nameList.remove(nameList[0])
	while nameList[-1].isalnum() == False:
		nameList.remove(nameList[-1])
	for char in nameList:
		if char.isalnum() == False:
			char = '-'

	return ''.join(nameList)

def generate_url(name):
	"""
	generate the url from each startup name based on its database / domain
		args name : startup name
	"""

	for char in name:
		if char.isalnum() == False:
			name = clean_string(name)
			break

	return ('http://e27.co/startup/' + name)

def generate_startup_list():
	"""
	read and list the list of startups which the data needs to be scraped
	"""
	info = 'Input the csv\'s filename and the filetype (ex: excelworkbook.csv) : '
	fileName = input(info)
	startupList = []
	with open(fileName, newline = '') as f:
		reader = csv.reader(f, delimiter = ',')
		skip = True
		for row in reader:
			if skip: 			#to skip the header
				skip = False
				contiue
			startupList.append(generate_url(row[7].lower()))

	return startupList

class cb_spider(scrapy.Spider):
	count_fail = 0
	count_succeed = 0
	succeed_list = []
	fail_list = []
	name = 'cb'
	start_url = ['https://www.crunchbase.com/organization/exim-guru']
	
	def start_requests(self):
		"""
		the function make a request for each url in the start_urls list
		fetch the requested url, and pass it to the callback, which is parse function
		"""
		for url in self.start_url:
			yield SplashRequest(url = url, callback = self.parse, args={'http_method': 'GET',})
		
	def parse(self, response):
		"""
		response: the fetched request received from start_requests
		the function return a dictionary (set of data) that contains the profile of the startup
		"""
		
		filename = 'cb-try.html'
		with open(filename, 'wb') as f:
			f.write(response.body)

		# print("DEBUG: ENTERING PARSE FUNC")
		# final_data = {}
		# final_data['Name'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/h1/text()').extract_first()
		# final_data['Founding'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/p[3]/span/text()').extract_first()
		# final_data['Description'] = response.xpath('//*[@id="page-container"]/div[4]/div/div/div/div/div[1]/div[1]/div[1]/div/p/text()').extract_first()
		# final_data['Website URL'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/span[1]/a/@href').extract_first()
		# final_data['Location'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/span[3]/a/text()').extract_first()

		# final_data['Industry'] = []
		# for element in response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[3]/span/a'):
		# 	final_data['Industry'].append(element.xpath("./text()").extract_first())

		# final_data['Twitter'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/a[1]/@href').extract_first()
		# final_data['Facebook'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/a[2]/@href').extract_first()
		# final_data['Linkedin'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/a[3]/@href').extract_first()
		# final_data['Logo-URL'] = response.xpath('//*[@id="page-container"]/div[3]/div/div/div/div/div/div[1]/img/@src').extract_first()

		# final_data['Investors'], final_data['Funding Amount'], final_data['Funding Date'], final_data['Funding Round'] = ([] for _ in range(4))
		# for funding in response.xpath('//*[@id="funding_table"]/div'):
		# 	try:
		# 		final_data['Investors'].append(funding.xpath('./div[1]/div/div[2]/div/a/text()').extract_first().lstrip().rstrip())
		# 	except:
		# 		final_data['Investors'] = None

		# 	final_data['Funding Round'].append(find_text(funding.xpath('./div[2]').extract_first()))
		# 	final_data['Funding Amount'].append(find_text(funding.xpath('./div[3]').extract_first()))
		# 	final_data['Funding Date'].append(find_date(funding.xpath('./div[4]').extract_first()))

		# if final_data['Name'] == None:
		# 	self.count_fail += 1
		# 	self.fail_list.append((str(self.count_fail) + ': ' + response.url))
		# else: 
		# 	self.count_succeed += 1
		# 	self.succeed_list.append((str(self.count_succeed) + ': ' + final_data['Name']))

		# print('FAIL COUNT : ' , str(self.count_fail))
		# print("FAIL LIST: ", self.fail_list)
		# print('SUCCESS COUNT: ' , str(self.count_succeed))
		# print('SUCCESS LIST: ', self.succeed_list)

		# yield final_data