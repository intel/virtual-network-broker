import urllib2
import pdb


def function():
    pdb.set_trace()
    secmon_url = 'http://10.42.0.155/32029/'
    data = '{"table_name": "scope",
             "row_id": "d695058e-da4e-4616-bc70-497a176a6842",
             "operation": "PUT"}'
    request_headers = {"Content-Type": "application/json"}
    req = urllib2.Request(secmon_url, data, headers=request_headers)
    req.get_method = lambda: 'POST'
    f = urllib2.urlopen(req)
    json_data1 = json.loads(f.read())
