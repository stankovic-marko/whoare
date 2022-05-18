import requests
import sys
import json
import time

if __name__ == "__main__":

    whois_server_limits = {
        "http://ip-api.com/json/_ip_": 45,
        "https://ipapi.co/_ip_/json/": 300,
        "http://ipwho.is/_ip_": 45
    }

    whois_servers = list(whois_server_limits.keys())
    ips = []

    file = open(sys.argv[1], "r")
    ip = file.readline()
    while not ip == "":
        ips.append(ip.replace("\n", ""))
        ip = file.readline()
    file.close()

    outfile = open("out.json", "w")
    outfile.write("[")
    current_server = 0
    batch_request = 0
    request = 0

    print("Using server: ", whois_servers[current_server])
    for ip in ips:

        if(batch_request == whois_server_limits[whois_servers[current_server]]):
            print("Number of ips checked: ", request)
            current_server = current_server + 1
            if(current_server == len(whois_servers)):
                current_server = 0
                print("Reached limit on all servers. Continuing in 60 seconds.")
                time.sleep(60.0)
                print("Continuing...")
           
            batch_request = 0
            print("Using server: ", whois_servers[current_server])


        url = whois_servers[current_server].replace("_ip_", ip)
        data = requests.get(url)
        request = request + 1
        batch_request = batch_request + 1

        if(data.status_code == 200):
            json.dump(data.json(), outfile)
            if(request < len(ips)):
                outfile.write(",")
        else:
            print("Error status code. Switching to next server.")
            current_server = current_server + 1
            batch_request = 0
    
    outfile.write("]")
    outfile.close()
    print("Finished. ", request, " ips checked.")
