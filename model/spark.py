# pip install --upgrade spark_ai_python  # 安装spark_ai_python库

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import os
from dotenv import load_dotenv

load_dotenv()

class SparkLLM:
    def __init__(self, app_id='', api_secret='', model= 'spark_lite', api_key='', url='wss://spark-api.xf-yun.com/v1.1/chat', domain='general', stream=False, max_tokens=1024, model_kwargs={"search_disable": True}):
        self.app_id = app_id
        self.api_secret = api_secret
        self.api_key = api_key
        self.url = url
        self.domain = domain
        self.stream = stream
        self.max_tokens = max_tokens
        self.model_kwargs = model_kwargs
        self.model_name = model
        self.client = self.create_client()

    def create_client(self):
        return ChatSparkLLM(
            spark_api_url=self.url,
            spark_app_id=self.app_id,
            spark_api_key=self.api_key,
            spark_api_secret=self.api_secret,
            spark_llm_domain=self.domain,
            streaming=self.stream,
            max_tokens=self.max_tokens,
            model_kwargs=self.model_kwargs,
        )
    
    

    def generate_response(self, content):
        messages = [ChatMessage(role="user", content=content)]
        handler = ChunkPrintHandler()
        response = self.client.generate([messages], callbacks=[handler])
        if self.stream:
            lines = self.client.stream(messages)
            for line in lines:
                yield {"content": line.content, "stream": True}
        else:
            yield {'content':response.generations[0][0].text, "stream": False}

if __name__ == '__main__':
    SPARKAI_APP_ID = os.getenv('SPARKAI_APP_ID')
    SPARKAI_API_SECRET = os.getenv('SPARKAI_API_SECRET')
    SPARKAI_API_KEY = os.getenv('SPARKAI_API_KEY')
    
    spark_llm_instance = SparkLLM(
        app_id=SPARKAI_APP_ID,
        api_secret=SPARKAI_API_SECRET,
        api_key=SPARKAI_API_KEY,
        url='wss://spark-api.xf-yun.com/v1.1/chat',
        domain='general',
        stream=True,
        max_tokens=1024,
        model_kwargs={"search_disable": True}
    )
    res= spark_llm_instance.generate_response('搜索重庆胖猫事件')
    for line in res:
        print(line)
