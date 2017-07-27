import graphitesend
import json
import requests
import sys

def getSolrDataImportStatus(url):
	data = requests.get(url) 
	return data.json()

def convertTimeToSeconds(time):
	(h, m, sms) = time.split(':')
	(s, ms) = sms.split(".")

	return int(h) * 3600 + int(m) * 60 + int(s)

def parseStatus(jsonSolrDataImportStatus):
	result = {}
	result['com_stat'] = 99 # unknown command status

	if jsonSolrDataImportStatus['status'] == "busy":
		result['com_stat'] = 1
	elif jsonSolrDataImportStatus['status'] == "idle":
		result['com_stat'] = 0

	if result['com_stat'] == 1:
		sm = jsonSolrDataImportStatus['statusMessages']
		result['elapsed_seconds'] = convertTimeToSeconds(sm['Time Elapsed'])
		result['total_row_fetched'] = sm['Total Rows Fetched']
		result['total_documents_processed'] = sm['Total Documents Processed']

	return result

def sendToGraphite(graphSrv, graphPrt, pfx, host, solr_col, metrics):
	# clean host data
	ch = host.replace(".", "_")

	pfx = "%s.%s" % (pfx, solr_col,)
	g = graphitesend.init(graphite_server=graphSrv, graphite_port=graphPrt, prefix=pfx, system_name=ch)
	for metric in metrics:
		g.send(metric, metrics[metric])

	return 0

if __name__ == '__main__':
	jsonConfig = None
	if len(sys.argv) == 2:
		conf_name = sys.argv[1]
		try:
			with open(conf_name) as f:
				jsonConfig = json.load(f)
			f.close()
		except:
			print("Could not open file %s!\nPlease provide a valid file name!\n" % (conf_name, ))
			sys.exit(3)
	else:
		print("Please provide the name of the config file as the single first argument!\n")
		sys.exit(2)
	
	jc = jsonConfig
	for item in jc['solr_monitor_list']:
		custom_url = jc['solr_dataimport_url_format'] % (item['solr_webinterface_protocol'], item['solr_host'], item['solr_host_port'], item['solr_collection'], )
	
		json = getSolrDataImportStatus(custom_url)
		res = parseStatus(json)
	
		sendToGraphite(jc['graphite_server'], jc['graphite_port'], jc['graphite_prefix'], item['solr_host'], item['solr_collection'], res)
