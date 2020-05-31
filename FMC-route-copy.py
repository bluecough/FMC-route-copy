import sys, argparse, itertools, json
from pathlib import Path

#from crayons import blue, green
from fmc_requests import fmc_authenticate, fmc_get, fmc_delete, fmc_post  # noqa

containerUUID = []
objectid = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dtf', action='store_true', default=False, dest='dumptofile', help='Dump routes to file')
    parser.add_argument('-d', action='store_true', default=False, dest='dumpcoid', help='Dump container and object ids')
    parser.add_argument('-l', action='store', dest='loadroutes', help='Load routes from file')
    results = parser.parse_args()

    try:
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    if results.dumptofile == True:
        f = open('fmc-route-output.txt', 'w')
        dumptofile(f)
        f.close()

    if results.dumpcoid == True:
        dumpcoid()

    if results.loadroutes != None:
        loadroutes(results.loadroutes)

def dumptofile(f):
    # Authenticate with FMC
    access_token, domain_uuid = fmc_authenticate()

    output = fmc_get("devices/devicerecords")
    # So get the number of items in the list. I figure that this will be the number of sensors

    for i in range(len(output['items'])):
        #    print(output['items'][i-1]['id'])
        containerUUID.append(output['items'][i - 1]['id'])
    for i in containerUUID:
        output = fmc_get("devices/devicerecords/" + i + "/routing/ipv4staticroutes")
        #print(output['items'][0]['id'])
        #print(len(output['items']))
        for i in range(len(output['items'])):
            objectid.append(output['items'][i-1]['id'])

    for i in range(len(containerUUID)):
        for j in range(len(objectid)):
            output = "ContainerUUID " + containerUUID[i-1] + " objectID " + objectid[j-1]

    for i in containerUUID:
        for j in objectid:
            getRoutes(i, j, f)

def dumpcoid():
    # Authenticate with FMC
    access_token, domain_uuid = fmc_authenticate()

    output = fmc_get("devices/devicerecords")
    # So get the number of items in the list. I figure that this will be the number of sensors

    for i in range(len(output['items'])):
        #    print(output['items'][i-1]['id'])
        containerUUID.append(output['items'][i - 1]['id'])
    for i in containerUUID:
        output = fmc_get("devices/devicerecords/" + i + "/routing/ipv4staticroutes")
        #print(output['items'][0]['id'])
        #print(len(output['items']))
        for i in range(len(output['items'])):
            objectid.append(output['items'][i-1]['id'])

    for i in range(len(containerUUID)):
        for j in range(len(objectid)):
            output = "ContainerUUID " + containerUUID[i-1] + " objectID " + objectid[j-1]
            print(output)

def getRoutes(containerUUID, objectid, f):
    #access_token, domain_uuid = fmc_authenticate()
    output = fmc_get("devices/devicerecords/" + containerUUID + "/routing/ipv4staticroutes/" + objectid)
    myoutput = dict(itertools.islice(output.items(), 2, None))
    #print(str(myoutput).replace("'", '"').replace('"overridable": False,', ''))
    f.write(str(myoutput).replace("'", '"').replace('"overridable": False,', '').replace('"isTunneled": False,', '') + "\n")
    #f.write(str(myoutput).replace("'overridable': False,", '') + "\n")

def loadroutes(containerUUID):
    f = open('fmc-route-output.txt', 'r')
    access_token, domain_uuid = fmc_authenticate()
    for line in f:
        try:
            output = fmc_post("devices/devicerecords/" + containerUUID + "/routing/ipv4staticroutes", json.loads(line))
        except:
            print("Error: " + line)
            pass

if __name__ == '__main__':
    main()