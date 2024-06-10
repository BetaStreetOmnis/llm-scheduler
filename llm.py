from model.hunyuan import HunyuanLLM
from model.spark import SparkLLM
from model.wenxin import WenxinLLM
import random
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class EnvConfig:
    @staticmethod
    def get_keys(var_name):
        """
        从环境变量中获取单个密钥或多个密钥（逗号分隔），并返回一个列表。
        
        Args:
            var_name (str): 环境变量名称。

        Returns:
            list: 包含一个或多个密钥的列表。
        """
        keys = os.getenv(var_name)
        if keys:
            if ',' in keys:
                return random.choice(keys.split(','))
            else:
                return keys
        else:
            raise ValueError(f"No keys found for {var_name}")


class UniversalLLM:
    """
    通用LLM类，支持多LLM接口混用。
    
    Attributes:
        llm: An instance of a specific LLM class (HunyuanLite, SparkLite, WenxinLite) based on the model_name.
        models: A list of available LLM instances for random selection.
    """
    
    def __init__(self, model_name=None):
        """
        Args:
            model_name (str, optional): 模型名称，可以是"hunyuan_lite"、"spark_lite_llm"或"wenxin_lite"。 
        Raises:
            ValueError: 如果传入的model_name无效。
        """
        self.models = []
        self.model_name = ""
    
    
    
    def _choice_model(self, extracted=[]):
        """
        随机选择一个模型实例。
        
        """
        # 排除已经提取过的模型
        available_models = [model for model in self.models if model[1] not in extracted]
        
        if not available_models:
            return None
        
        # 按优先级排序
        available_models.sort(key=lambda x: x[2])
        
        # 获取最高优先级
        highest_priority = available_models[0][2]
        highest_priority_models = [model for model in available_models if model[2] == highest_priority]
        
        # 随机选择最高优先级模型
        selected_model = random.choice(highest_priority_models)
        
        # 将选中的模型添加到已提取列表中
        extracted.append(selected_model[1])
        print(selected_model)
        
        return selected_model[0], extracted
    

    def generate_text(self, prompt):
        extracted_list = []
        
        llm_model, extracted_list = self._choice_model(extracted=extracted_list)
        for line  in llm_model.generate_response(prompt):
            yield line
        

    def _model(self, model_name):
        if model_name == "hunyuan_lite":
            llm_model = HunyuanLLM(secret_id=EnvConfig.get_keys('hunyuan_SecretId'), secret_key=EnvConfig.get_keys('hunyuan_SecretKey'))
        elif model_name == "spark_lite_llm":
            llm_model = SparkLLM(app_id=EnvConfig.get_keys('SPARKAI_APP_ID'), api_secret=EnvConfig.get_keys('SPARKAI_API_SECRET'), api_key=EnvConfig.get_keys('SPARKAI_API_KEY'))
        elif model_name == "wenxin_lite":
            llm_model = WenxinLLM(api_key=EnvConfig.get_keys('WENXIN_API_KEY'), secret_key=EnvConfig.get_keys('WENXIN_SECRET_KEY'))
        # elif model_name == "gemini_pro":
        #     llm_model = GeminiPro(api_key=EnvConfig.get_keys('GEMINI_API_KEY'))
        else:
            llm_model = None
        return llm_model
    
    def _model_list(self, config_list=None):
        if config_list:
            for config in config_list:
                model_name = config.get("model_name", "hunyuan_lite")
                llm = self._model(model_name)
                if llm:
                    llm.top_p = config.get("top_p", 0.95)
                    llm.temperature = config.get("temperature", 0.7)
                    llm.max_tokens = config.get("max_tokens", 256)
                    llm.stream = config.get("stream", True)
                    self.models.append((llm, model_name, config.get("priority", 0)))

    def set_parameters(self, config_list=None):
        """
        设置LLM模型的参数。

        Args:
            **kwargs: 模型参数的关键字参数。
        """
        # TODO 模型随机性 优先级判断，模型报错的异常处理
        self._model_list(config_list)


    def _chat_completions(self, messages, stream=False):
        """
        进行聊天式对话。

        Args:
            messages (list): 对话消息列表。
            stream (bool): 是否以流模式生成响应。

        Returns:
            str: 生成的对话响应。
        """
        return self.llm.chat_completions(messages, stream)

# 示例用法
if __name__ == "__main__":
    llm = UniversalLLM()
    prompt = "介绍一下人工智能的发展史。"
    # 配置项通过关键字参数传递
    config_list = [
        {"model_name": "hunyuan_lite", "top_p": 0.8, "temperature": 0.6, "max_tokens": 25, "stream": True, "priority":1},
        # {"model_name": "spark_lite_llm", "top_p": 0.85, "temperature": 0.65, "max_tokens": 100, "stream": True, "priority":1}
    ]
    llm.set_parameters(config_list=config_list)
    response = llm.generate_text(prompt)
    for line in response:
        print(line)
