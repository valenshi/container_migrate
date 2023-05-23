import sys
import xmlrpc.client

ip = "192.168.1.201"
hostname = sys.argv[1]
try:
    # print('collectHost', ip, hostname)
    server_url = "http://" + ip + ":9926/"
    proxy = xmlrpc.client.ServerProxy(server_url, verbose=True)
    result = proxy.hostPower(hostname)
    result = int(result)
    print(result)
except Exception as e:
    print(e)