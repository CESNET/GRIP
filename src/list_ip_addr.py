
def list_ip(idea):
    result = []
    for ip in idea:
        if '-' in ip:
            parts = ip.split('-')
            if parts[1].isdigit():
                for i in range(int(parts[0].split('.')[3]), int(parts[1])+1):
                    result.append(parts[0].split('.')[0] + '.' + parts[0].split('.')[1] + '.' + parts[0].split('.')[2] + '.' + str(i))
            else:
                for i in range(int(parts[0].split('.')[0]), int(parts[1].split('.')[0])+1):
                    for j in range(int(parts[0].split('.')[1]), int(parts[1].split('.')[1])+1):
                        for k in range(int(parts[0].split('.')[2]), int(parts[1].split('.')[2])+1):
                            for l in range(int(parts[0].split('.')[3]), int(parts[1].split('.')[3])+1):
                                result.append(str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l))
        elif '/' in ip:
            parts = ip.split('/')
            if int(parts[1]) < 8:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [2**(8-(int(parts[1])%8)), 0, 0, 0])]
                for i in range(0, 2**(8-int(parts[1])%8)):
                    for j in range(0, 256):
                        for k in range(0, 256):
                            for l in range(0, 256):
                                result.append(str(int(mask[0])+i) + '.' + str(j) + '.' + str(k) + '.' + str(l))
            elif int(parts[1]) < 16:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 2**(8-(int(parts[1])%8)), 0, 0])]
                for j in range(0, 2**(8-int(parts[1])%8)):
                    for k in range(0, 256):
                        for l in range(0, 256):
                                result.append(str(parts[0].split('.')[0]) + '.' + str(int(mask[1])+j) + '.' + str(k) + '.' + str(l))
            elif int(parts[1]) < 24:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 255, 2**(8-(int(parts[1])%8)), 0])]
                for k in range(0, 2**(8-int(parts[1])%8)):
                    for l in range(0, 256):
                                result.append(str(parts[0].split('.')[0]) + '.' + str(parts[0].split('.')[1]) + '.' + str(int(mask[2])+k) + '.' + str(l))
            elif int(parts[1]) < 32:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 255, 255, 2**(8-(int(parts[1])%8))])]
                for l in range(0, 2**(8-int(parts[1])%8)):
                    result.append(str(parts[0].split('.')[0]) + '.' + str(parts[0].split('.')[1]) + '.' + str(parts[0].split('.')[2]) + '.' + str(int(mask[3])+l))
        else:
            result.append(ip)
    return result
