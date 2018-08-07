import ast
import datetime
import json
import operator
import settings


true = True

################################################################################################## 

##################################################################################################

file_write = open(settings.PWD + 'count_of_attach.txt', 'w')
sum_files = 1000000

descArray = []    
for f in range(1, sum_files):
    if f < 10:
        f = '000' + str(f) + '.idea'
    elif f < 100:
        f = '00' + str(f) + '.idea'
    elif f < 1000:
        f = '0' + str(f) + '.idea'
    else:
        f = str(f) + '.idea'
    filik = open(settings.PWD + f, 'r')
    ideafile = (filik.read())
    idea = eval(ideafile) 
    
    if 'Attach' in idea:   
        file_write.write(str(idea['Attach'][0]) + '\n')  


        # 84676
        # {'name': '13012: SIP: SipVicious Brute Force SIP Tool', 'count': 56886}
        # {'name': '32391: UDP: Netcore/Netis Router Backdoor Communication Attempt', 'count': 21773}
        # {'name': 'ET SCAN Potential SSH Scan OUTBOUND', 'count': 2671}
        # {'name': 'Comm. with host known as malware source', 'count': 1537}
        # {'name': '0560: DNS: Version Request (UDP)', 'count': 355}
        # {'name': 'ET DOS Possible NTP DDoS Inbound Frequent Un-Authed MON_LIST Requests IMPL 0x03', 'count': 334}
        # {'name': 'Drop RPF', 'count': 254}
        # {'name': 'Port scanning Security issues', 'count': 215}

        # {'name': '12607: Backdoor: Zero Access Trojan Communication Attempt', 'count': 57}
        # {'name': 'GPL VOIP SIP INVITE message flooding', 'count': 45}
        # {'name': 'ET DOS Possible Memcached DDoS Amplification Query (set)', 'count': 43}
        # {'name': 'Communication w. host having reputation score 80+', 'count': 29}
        # {'name': 'GPL ATTACK_RESPONSE id check returned root', 'count': 28}
        # {'name': 'Resolving name of host having reputation score 80+', 'count': 16}
        # {'name': 'Comm. with host known as botnet member or worm src', 'count': 15}
        # {'name': 'GPL SNMP public access udp', 'count': 14}
        # {'name': '27429: UDP: Ransom_CERBER.ENC Checkin', 'count': 10}
        # {'name': 'ET EXPLOIT ETERNALBLUE Exploit M2 MS17-010', 'count': 9}
        # {'name': '16304: UDP: MIT Kerberos KDC Server TGS-REQ Denial-of-Service Vulnerability', 'count': 6}
        # {'name': '12961: DNS: Large UDP Packet DDoS (ONLY enable when under DoS attack)', 'count': 2}
        # {'name': 'Comm. with server hosting phishing page', 'count': 2}
        # {'name': '30565: DNS: Possible Kelihos .eu CnC Domain Generation Algorithm (DGA) Lookup NXDOMAIN Response', 'count': 2}
        # {'name': 'ET CNC Feodo Tracker Reported CnC Server group 4', 'count': 1}
        # {'name': '5300: DNS: Suspicious Localhost PTR Record Response', 'count': 1}
        # {'name': 'ET DROP Dshield Block Listed Source group 1', 'count': 1}
        # {'name': '0???}?j?x???\x07i\x0c?\x13??????9",2852,"CZ",,"NOVA HOSPODA",0,0,"Information Technology"', 'count': 1}
        # {'name': '29739: SIP: Digium Asterisk app_minivm Caller-ID Command Execution Vulnerability', 'count': 1}


file_write = open(settings.PWD + 'attach_types.txt', 'w')
count = 0

attach_types = []
attach_types_set = set()
result = []
filik = settings.PWD + 'count_of_attach.txt'
with open(filik) as f:
    lines = f.readlines()
    for line in lines:
        print(str(count))
        count += 1
        line = eval(line)
        if 'Content' in line:
            if len(line['Content'].split('|')) > 1:
                try:
                    sign = line['Content'].split('|')[4]
                    attach_types.append(sign)
                    attach_types_set.add(sign)
                except:
                    file_write.write(str(line['Content']) + '\n')
            elif line['Content'].startswith('Drop RPF'):
                try:
                    attach_types.append('Drop RPF')
                    attach_types_set.add('Drop RPF')
                except:
                    file_write.write(str(line['Content']) + '\n')
            elif len(line['Content'].split('\t')) > 1:
                try:
                    sign = line['Content'].split('\t')[4] + ' ' + line['Content'].split('\t')[5]
                    attach_types.append(sign)
                    attach_types_set.add(sign)
                except:
                    file_write.write(str(line['Content']) + '\n')
            else:
                try:
                    sign = json.dumps(line['Content'].replace("u'", '"').replace("'", '"'))
                    sign = json.loads(sign)
                    sign = (ast.literal_eval(sign))
                    attach_types.append(sign['alert']['signature'])
                    attach_types_set.add(sign['alert']['signature'])
                except:
                    file_write.write(str(line['Content']) + '\n')

counter = 0
for item in attach_types_set:
    for i in attach_types:
        if item == i:
            counter += 1
    result.append({'name': item, 'count': counter})
    counter = 0

result.sort(key=operator.itemgetter('count'), reverse=True)

for i in result:
    print(i) 
print(str(count))

