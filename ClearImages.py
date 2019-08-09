import pandas as pd 
import numpy as np
import json
import requests
res_list=[]
url1 = 'https://hub.docker.com/v2/repositories/clearlinux/?page=1'
url2 = 'https://hub.docker.com/v2/repositories/clearlinux/?page=2'
url3 = 'https://hub.docker.com/v2/repositories/clearlinux/?page=3'
url4 = 'https://hub.docker.com/v2/repositories/clearlinux/?page=4'
proxies = {'http': 'http://child-prc.intel.com:913', 'https': 'https://child-prc.intel.com:913'}
r1 = requests.get(url1)
r2 = requests.get(url2)
r3 = requests.get(url3)
r4 = requests.get(url4)

js1=json.loads(r1.text)
js2=json.loads(r2.text)
js3=json.loads(r3.text)
js4=json.loads(r4.text)
js=[]
js.extend(js1["results"])
js.extend(js2["results"])
js.extend(js3["results"])
js.extend(js4["results"])
js=pd.DataFrame(js)
features=["name","description","pull_count","star_count","last_updated"]
js=js[features]

name_list=js['name']
#import requests
#res_list=[]
#proxies = {'http': 'http://child-prc.intel.com:913', 'https': 'https://child-prc.intel.com:913'}
#for each in name_list:    
#    url='https://hub.docker.com/v2/repositories/clearlinux/'+each+'/dockerfile/'
#    r = requests.get(url)
#    res_list.append(r.text)
#print(res_list)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',200)


js['from']=js['name'].apply(lambda x:"clearlinux")
#js['from']=js['from'].apply(lambda x:x.split("\\n",1)[0][12:])
#js['from']=js['from'].apply(lambda x:x.split("FROM",1)[1][12:])
#js['from']=js['from'].apply(lambda x:x.split("swupd_args",1)[0] if(x.find("swupd_args")!=-1) else x )
js['last_updated']=js['last_updated'].apply(lambda x:x if x is None else x[:19])
lgpl_dict={'mixer': 'BSD',
 'mariadb': 'Apache License 2.0',
 'clr-installer-ci': 'MIT License',
 'mixer-ci': 'MIT License',
 'clr-sdk': np.nan,
 'os-core': 'Apache License 2.0',
 'machine-learning': np.nan,
 'stacks-dlrs-mkl': 'ISSL',
 'httpd': 'APACHE LICENSE, VERSION 2.0',
 'nginx': 'the 2-clause BSD-like license',
 'golang': 'BSD',
 'python': 'Python PSF LICENSE AGREEMENT',
 'machine-learning-ui': np.nan,
 'redis': 'three clause BSD license.',
 'memcached': 'BSD',
 'node': 'ICU License - ICU 1.8.1 to ICU 57.1',
 'php': 'PHP License v3.01',
 'postgres': 'PostgreSQL License, a liberal Open Source license, similar to the BSD or MIT licenses.',
 'stacks-dlrs-oss': 'BSD',
 'openjdk': 'General Public License Version 2.0',
 'cgit': 'GPLv2',
 'ruby': 'the 2-clause BSDL',
 'elasticsearch': 'ELASTIC LICENSE',
 'stacks-pytorch-mkl': 'BSD&ISSL',
 'tensorflow': 'Apache License 2.0',
 'perl': 'GNU General Public License',
 'haproxy': 'GNU General PublicÿLicenseÿVersion 2',
 'rabbitmq': 'Mozilla Public License Vesion 1.1',
 'iperf': 'BSD',
 'stacks-pytorch-oss': 'BSD',
 'stacks-dars-mkl': 'ISSL',
 'stacks-dlrs-mkl-vnni': 'Apache License 2.0',
 'stacks-dars-openblas': 'BSD',
 'flink': 'Apache License 2.0',
 'stacks-clearlinux': np.nan}
js['license']=js['name'].map(lgpl_dict)
res_list=[]
proxies = {'http': 'http://child-prc.intel.com:913', 'https': 'https://child-prc.intel.com:913'}
for each in name_list:    
    url='https://hub.docker.com/v2/repositories/clearlinux/'+each+'/tags/'
    r = requests.get(url)
    res_list.append(r.text)
res_list_size=[]
for each in res_list:
    each1=json.loads(each)
    each2=each1['results']
    if(len(each2)):
        each3=each2[0]["full_size"]
        res_list_size.append(each3)
    else:
        res_list_size.append(np.nan)
size_dict=dict(zip(name_list,res_list_size))
js['size(MB)']=js['name'].map(size_dict)/1000/1000


js.to_csv("ClearDockerImage.csv",encoding="utf-8",index=None)
print("-----执行成功-------数据已存入当前目录ClearDockerImage.csv")

