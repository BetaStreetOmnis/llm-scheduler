# pip install --upgrade spark_ai_python  # 安装spark_ai_python库

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = ''
SPARKAI_API_SECRET = ''
SPARKAI_API_KEY = ''
#星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'general'

def spark_llm(content):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=content
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    # generations=[[ChatGeneration(text='你好！很高兴和你交流，有什么我可以帮助你的吗？', message=AIMessage(content='你好！很高兴和你交流，有什么我可以帮助你的吗？'))]] llm_output={'token_usage': {'question_tokens': 11, 'prompt_tokens': 11, 'completion_tokens': 13, 'total_tokens': 24}} run=[RunInfo(run_id=UUID('c0b70f87-6099-4a81-b5e7-cb3e4398e3c3'))]
    return a.generations[0][0].text

if __name__ == '__main__':
    a = spark_llm()
    print(a)