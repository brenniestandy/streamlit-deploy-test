import requests
import json
import pandas as pd

async def fetch(fetchWhat):
    # url = "http://localhost:3000/all"
    url = "https://ymfpmafvdp6lyzcd3dw3lhht3i0nvvgd.lambda-url.us-east-1.on.aws/"
    
    response = requests.get(url, params={"fetchWhat": fetchWhat})
    
    if response.status_code == 200:
        data = json.loads(response.text)
        # data_compilation = []
        # for item in data[0]:
        #     data_compilation.append(pd.DataFrame(item))
        
        # return pd.concat(data_compilation)
        return pd.DataFrame(data["body"][0])
