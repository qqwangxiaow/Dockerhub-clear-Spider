import pandas as pd 
import numpy as np
import json
import requests
res_list=[]
proxies = {'http': 'http://child-prc.intel.com:913', 'https': 'https://child-prc.intel.com:913'}
js=[]
for i in range(1,18):  
    url1 = 'https://hub.docker.com/v2/repositories/bitnami?page='+str(i)
    r1 = requests.get(url1,proxies=proxies)
    js1=json.loads(r1.text)
    js.extend(js1["results"])
js_df=pd.DataFrame(js)
features=['name','namespace','pull_count','star_count','last_updated','is_automated','is_migrated','description']
js_df2=js_df[features]
js_df2.to_csv("bitnami_docker.csv",encoding='utf-8',index=None)