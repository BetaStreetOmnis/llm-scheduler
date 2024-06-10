## 概述
本项目提供了一个基于 Streamlit 的网页界面，用于与多个大型语言模型 (LLM) 进行交互，包括 HunyuanLite、SparkLite 和 WenxinLite等各平台免费llm接口。应用允许用户配置和管理多个 LLM，为每个模型设置参数，并生成对用户提示的响应。最大的特点是支持多个模型同时使用并轮流调度，从而实现更灵活和高效的响应生成，避免超过限定QPS值。

## 功能
多模型支持和轮流调度：配置和使用多个 LLM，例如 HunyuanLite、SparkLite 和 WenxinLite，并在多个模型之间进行轮流调度以生成响应。
动态配置：通过 Streamlit 侧边栏动态添加、查看和管理模型配置。
流式响应：选择以流模式接收响应。
优先级设定：为模型设置优先级以控制其选择。

## 试用地址
http://47.108.118.232:8501/

## 安装

### 先决条件
Python 3.8+

### 安装依赖
pip install streamlit 
pip install python-dotenv
pip install spark-ai-python
pip install tencentcloud-sdk-python

### 复制代码
git clone https://github.com/BetaStreetOmnis/free_llm_api.git
cd free_llm_api

### 设置
在项目根目录下.env.example重命名为.env文件，并添加您的 API 密钥。例如：

hunyuan_SecretId=your_hunyuan_secret_id
hunyuan_SecretKey=your_hunyuan_secret_key
SPARKAI_APP_ID=your_sparkai_app_id
SPARKAI_API_SECRET=your_sparkai_api_secret
SPARKAI_API_KEY=your_sparkai_api_key
WENXIN_API_KEY=your_wenxin_api_key
WENXIN_SECRET_KEY=your_wenxin_secret_key

## 运行 Streamlit 应用：

streamlit run streamlit_app.py

## 使用
### 主界面

模型配置：使用侧边栏选择一个模型，设置参数（Top P、Temperature、Max Tokens、Priority、Stream），点击“Add Model Configuration”按钮添加配置。
当前模型配置：在侧边栏查看已添加的模型配置列表。
提示输入：在主输入框中输入您的提示，点击“Generate Response”按钮生成模型响应。


示例代码
UniversalLLM 类
UniversalLLM 类管理与不同 LLM 的交互。它允许设置参数、生成文本，并根据优先级选择模型。

## 许可证
本项目使用Apache License 2.0许可证。

## 致谢
特别感谢 HunyuanLite、SparkLite 和 WenxinLite 的开发者和贡献者提供的模型和 API，用于本项目。






