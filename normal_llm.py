from llm.hunyuan_lite import HunyuanLite
from llm.spark_lite_llm import SparkLite
from llm.wenxin_lite import WenxinLite




# 通用llm
class NormalLLM:
    def __init__(self, model_name):
        if model_name == "hunyuan_lite":
            self.llm = HunyuanLite()
        elif model_name == "spark_lite_llm":
            self.llm = SparkLite()
        elif model_name == "wenxin_lite":
            self.llm = WenxinLite()
