# 文心一言免费模型
# encoding=utf-8
import requests
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class WenxinLLM:
    def __init__(self, api_key='', secret_key='', model='wenxin', top_p=0.7, temperature=0.9,  max_tokens=1024, stream=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.model_name = model
        self.top_p = top_p
        self.temperature = temperature
        self.stream = stream
        self.max_tokens = max_tokens
        
        
    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        return str(requests.post(url, params=params).json().get("access_token"))

    def generate_response(self, content):
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + self.get_access_token()
   
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "penalty_score": 1,
            "system": "你是一个专业的问答机器人。",
            "max_output_tokens": self.max_tokens,
            "stream": self.stream
        })
        headers = {
            'Content-Type': 'application/json'
        }
        if self.stream:
            response = requests.request("POST", url, headers=headers, data=payload, stream=True)
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    json_data = line[6:]
                    result = json.loads(json_data)
                    yield {"content": result['result']}
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
            yield {"content": response.json()['result']}



if __name__ == '__main__':
    API_KEY = os.getenv('WENXIN_API_KEY')
    SECRET_KEY = os.getenv('WENXIN_SECRET_KEY')
    print(API_KEY, SECRET_KEY)
    
    wenxin_llm_instance = WenxinLLM(api_key=API_KEY, secret_key=SECRET_KEY,streaming=False)
    response = wenxin_llm_instance.generate_response('搜索重庆胖猫事件')
    for line in response:
        print(line)
