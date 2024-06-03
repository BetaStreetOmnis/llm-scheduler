import json
import types
from tencentcloud.common import credential #
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models


def hunyuan_llm(content):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        # cred = credential.Credential("SecretId", "SecretKey")
        cred = credential.Credential("AKIDc3Kj9pQuBNNAjBgv33rY8UgiXJdqwrjW", "hp04wnjcPJ9xfGoAORHvgbP1Vt8A0hGj")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = hunyuan_client.HunyuanClient(cred, "ap-beijing", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ChatCompletionsRequest()
        params = {
            "Model": "hunyuan-lite",
            "Messages": [
                {
                    "Role": "user",
                    "Content": content
                }
            ],
            "TopP": 1,
            "Temperature": 0.8,
            "EnableEnhancement": True
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
        resp = client.ChatCompletions(req)
        # 输出json格式的字符串回包
        if isinstance(resp, types.GeneratorType):  # 流式响应
            for event in resp:
                print(event)
        else:  # 非流式响应
            print(resp)
            return resp.Choices[0].Message.Content


    except TencentCloudSDKException as err:
        print(err)
        return err
    

if __name__ == '__main__':
    line = """提取列表['纵览湖南最知名的超市，"步步高"绝对是个不得不提的名字，是时候了解背后推动它的力量"胖东来"团队了 你知道吗？当我们走在步步高的超市中，看到商品琳琅满目，布局井然有序，你有没有想过背后的故事？怎么会有那么多货品，怎么会有那么多品类出自胖东来的手中呢？ 没错，胖东来就是步步高超市的背后金主有了他们精良的商业模式和严格的战略研究，步步高还能失败吗？毫无疑问是不可能的！ 胖东来的团队是真正的商业大脑，他们善于洞察市场、深入消费者心理，抓住每一个消费趋势他们清楚地知道，消费者需要什么，是什么能满足消费者，他们凭借着这样的敏感度和理解能力，使他们在超市业占据了先发优势，始终保持领先地位', '他们将消费者的需求和期待放在了首位，因为他们相信这是企业长久生存的法宝，胖东来通过改善工作环境，提高员工待遇，让员工感受到他们所关心的不仅仅是利益，而是每一位员工的心态和发展 然而，现实中没有完美的东西，胖东来也并非例外也不乏有一些网友表达了对胖东来的不满，主要原因往往集中于其较高的价格毕竟，完美无暇是存在于理想之中的美好想象，稍显遥不可及 胖东来：这些都只是零星的小问题只要您能明确表述您的需求，比如需要对失去的时间或打车费用进行赔偿，并提供相关证明，我都会在我力所能及的范围内尽力解决您的问题 没有错，除非经过亲身经历，否则一切只能视为传闻毕竟，人们常说，不亲自体验，就无法辨识真伪有些事情，眼见未必为实，真正的真相常常蕴藏在亲身体验的过程中', '这已经非单一的求利模式，而是迈向了大众市场的经营逻辑今日的经营者深知，商品的质量要优良，利润则须适宜，服务更应精到向来，这样的经营理念以及店面格局，不是有着一般的吸引力吗？ 不，这可能是一些老板的观点：我为你的八小时工作付了工资，这意味着我买下了你的这八小时即便是上厕所的时间也应计算在内，如果时间过长，他们可能会考虑扣除部分薪资 胖东来的员工可能会这样说：“上班时间实在太短了，我还想继续工作！" 而其他地方的员工可能叫苦会道：“每日的工作时间已足够长，还被要求打加班，薪资却如此微薄，我宁愿偷懒不努力了！” 服务业的首要任务，无疑是服务员的态度对客户的初步影响因此，服务员在工作时的热情，以及他们的积极心态，都是保障业务长期稳定发展的重要条件', '然而，还有人会问，胖东来的商品繁多，会不会影响他们的品牌形象，因为其中有些并非他们直接管理的这里，我只能说，"绝对不会"因为胖东来把握了一个商业原则，那就是尊重消费者的需求和期待因为他们的创新思维和独特眼光，步步高超市成功地从一个传统的零售店升级成为一家深受大众欢迎的现代超市因此，他们的品牌并没有因此削弱，反而在扩大自己影响力的同时，也引领了整个行业的变革和升级 胖东来不仅仅是一个品牌，更是一种精神，一种永不停歇的追求卓越、挑战自我、引领创新的精神他们用行动诠释了"以人为本，服务至上"的经营理念，为自己树立了企业形象他们的成功讲述了一个道理，那就是只要把握住消费者的需要，无论市场如何变化，只要我们服务到位、产品优质，就能赢得市场和消费者的认可', '未来，无论是胖东来还是步步高，只要他们坚持这种以消费者为中心的服务理念，他们一定能在公司发展的道路永不夭折，步步高！ 即便时代在变，行业在变，胖东来始终信奉一条，那就是尊重消费者，热爱消费者，满足消费者的需求这就是他们的信仰，也是他们的承诺未来，他们将始终坚持这一原则，不断创新和开拓，为我们所有的消费者提供更多，更好的服务 总之，胖东来的成功，其背后集合了多种因素，他们准确的市场洞察、注重消费者需求的服务理念，还有无法替代的创新精神他们成功的实践，就是在给我们一个最好的答案，就是他们的企业精神和执行力胖东来，全新的商业时代，我们一同期待！返回搜狐，查看更多 责任编辑：']中的要点信息（30字以内）每个要点之间要空行。"""
    res = hunyuan_llm(line)
    print(1, res)