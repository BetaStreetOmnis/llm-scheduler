import json
import types
import os
from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

class HunyuanLLM:
    def __init__(self, secret_id='', secret_key='', region="ap-beijing", model="hunyuan-lite", top_p=1, temperature=0.8,  max_tokens=1024, enable_enhancement=True, stream=True):
        self.cred = credential.Credential(secret_id, secret_key)
        self.region = region
        self.model_name = model
        self.top_p = top_p
        self.temperature = temperature
        self.enable_enhancement = enable_enhancement
        self.stream = stream
        self.max_tokens = max_tokens
        self.client = self.create_client()

    def create_client(self):
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        
        return hunyuan_client.HunyuanClient(self.cred, self.region, clientProfile)

    def generate_response(self, content):
        try:
            req = models.ChatCompletionsRequest()
            params = {
                "Model": self.model_name,
                "Messages": [
                    {
                        "Role": "user",
                        "Content": content
                    }
                ],
                "MaxTokens": self.max_tokens,
                "Stream":   self.stream,
                "TopP": self.top_p,
                "Temperature": self.temperature,
                "EnableEnhancement": self.enable_enhancement
            }
            print(params)
            req.from_json_string(json.dumps(params))
            resp = self.client.ChatCompletions(req)
            if self.stream:  # 流式响应
                # pass
                for event in resp:
                    yield {"content": json.loads(event['data'])["Choices"][0]['Delta']['Content'], "stream": True}
            else:  # 非流式响应
                # resp:
                print(5)
                for choice in resp.Choices:
                    # 确保 choice 是一个对象，并正确访问其属性
                    content = getattr(choice.Message, 'Content', None)
                    if content:
                        yield {"content": content, "stream":False}
        except TencentCloudSDKException as err:
            print(err)
            return err

# 加载环境变量
load_dotenv()

# # 使用示例
# if __name__ == "__main__":
#     secret_id = os.getenv("hunyuan_SecretId")
#     secret_key = os.getenv("hunyuan_SecretKey")
    
#     hunyuan_llm_instance = HunyuanLLM(secret_id, secret_key, model="hunyuan-lite", top_p=1, temperature=0.8, enable_enhancement=True, streaming=False)
#     response = hunyuan_llm_instance.generate_response("写一篇100字的作文")
#     for line in response:
#         print(line)
    
