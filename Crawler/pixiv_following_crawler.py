import requests
import json
import queue
import os
import time

saveDir = './responses'

visited = {}
visitingQueque = queue.Queue()

def makeRequest(id):
    url='https://www.pixiv.net/ajax/user/{}/following?offset=0&limit=24&rest=show&tag=&lang=zh'.format(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'cookie': 'first_visit_datetime_pc=2021-08-28+23%3A51%3A32; p_ab_id=0; p_ab_id_2=4; p_ab_d_id=757421878; yuid_b=N4g4d2M; c_type=19; privacy_policy_agreement=3; privacy_policy_notification=0; a_type=0; b_type=1; tag_view_ranking=Lt-oEicbBr~RTJMXD26Ak~Ngz9KxUrJt~GX5cZxE2GY~b_G3UDfpN0~yZf1XmIy-U~nriWjM9urd~zyKU3Q5L4C~pSy0aCI-bY~q303ip6Ui5~RcahSSzeRf~fIMPtFR8GH~X_1kwTzaXt~y3NlVImyly~f7vBIMyqt6~K8esoIs2eW~jfcC9KzP1p~w8ffkPoJ_S~-sp-9oh8uv~Itu6dbmwxu~ahHegnNVxX~EhyAxo-Aql~HLWLeyYOUF~kGYw4gQ11Z~4ZEPYJhfGu~d2oWv_4U1L~LJo91uBPz4~38QHnJb19N~kP7msdIeEU~OT4SuGenFI~3mLXnunyNA~R-EFi7fMtD~h9r9YX0n2U~ZXFMxANDG_~BbGzECviUP~qtVr8SCFs5~EUwzYuPRbU~1SfcsyJqhK~JevMHrchAG~jH0uD88V6F~Tcn3gevBtQ~AdlIj3j7DB; PHPSESSID=55008219_Oo1gSEwfyMDn8mGNxFE0ursAPklIt0Yu; __cf_bm=AViL9lMPUqpYIe4bfTy.baDuQbA60ivZRvFLuhEYCRE-1636377545-0-ARTRnY5vL79wgn9095NBuGSpQXejJRiSb6+kii6PmhunRxY1W80JGzEPft3OmhmHGL3WbzkGye3KK3jQM2dYnvg9e4nDIWtkJb8IV7/+Op6v; device_token=64dece80d8b66963ff2a7b64692d8750',
        'referer': 'https://www.pixiv.net/users/{}/following'.format(id),
    }
    proxy = '127.0.0.1:7890'
    proxies = {
        'http': 'http//' + proxy,
        'https': 'https://' + proxy,
    }
    response = requests.get(url, headers=headers, proxies=proxies).json()
    total = response['body']['total']
    for i in range(24, total, 24):
        url='https://www.pixiv.net/ajax/user/{}/following?offset={}&limit=24&rest=show&tag=&lang=zh'.format(id, i)
        partialResponse = requests.get(url, headers=headers, proxies=proxies).json()
        for user in partialResponse['body']['users']:
            response['body']['users'].append(user)

    visited[id] = 1
    for user in response['body']['users']:
        visitingQueque.put(user['userId'])
    return response

def writeJSON(id, content):
    try:
        with open(os.path.join(saveDir, id+'.json'), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print('Saved to {}.json'.format(id))
    except:
        print('Saving {}.json error!'.format(id))
        print(json.dumps(content, indent=2))
    

def loadVisited():
    visitedList = os.listdir(saveDir)
    for file in visitedList:
        id = file.split('.')[0]
        visited[id] = 1
    print('Loaded total {} visited records'.format(len(visitedList)))

if __name__ == '__main__':
    startId = '6662895'
    visitingQueque.put(startId)
    loadVisited()
    
    startTime = time.time()
    epoch = 0
    while(len(visited) < 10000):
        visitingId = visitingQueque.get()
        if (visitingId in visited) : continue
        response = makeRequest(visitingId)
        writeJSON(visitingId, response)

        epoch += 1
        if (epoch % 10 == 0):
            timeSpent = int(time.time() - startTime)
            print('Epoch{}: total time {}m {}s'.format(epoch, timeSpent//60, timeSpent%60))