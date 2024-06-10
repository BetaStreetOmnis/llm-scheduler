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
                return keys.split(',')
            else:
                return [keys]
        else:
            raise ValueError(f"No keys found for {var_name}")

