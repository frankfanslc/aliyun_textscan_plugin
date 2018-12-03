# -*-coding:utf-8-*-
# 同步图片检测服务接口, 会实时返回检测的结果
import datetime
import json
import uuid
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
from apps.core.plug_in.config_process import get_plugin_config, import_plugin_config
from apps.plugins.aliyun_textscan_plugin.config import PLUGIN_NAME, CONFIG

__author__ = "Allen Woo"

import_plugin_config(PLUGIN_NAME, CONFIG)
# 请替换成你自己的accessKeyId、accessKeySecret, 您可以类似的配置在配置文件里面，也可以直接明文替换
clt = client.AcsClient(get_plugin_config(PLUGIN_NAME, "ACCESS_KEY"),
                        get_plugin_config(PLUGIN_NAME, "SECRET_KEY"),
                       get_plugin_config(PLUGIN_NAME, "REGION_ID"))
region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
request = TextScanRequest.TextScanRequest()
request.set_accept_format('JSON')

def main(**kwargs):

    '''
    主函数
    :param kwargs:
        content:需要鉴定的文本内容
    :return:
    '''
    content = kwargs.get("content")
    l = len(content)
    tasks = []
    for s in range(0, l, 3950):
        # 当内容过长的时候避免句子被截断，鉴定失误
        if s:
            s = s-50
        e = s+3950
        if l < e:
            task = {"dataId": str(uuid.uuid1()),
                     "content": content[s:],
                     "time": datetime.datetime.now().microsecond
                     }
        else:
            task = {"dataId": str(uuid.uuid1()),
                     "content": content[s:e],
                     "time": datetime.datetime.now().microsecond
                     }
        tasks.append(task)

    request.set_content(json.dumps({"tasks": tasks, "scenes": ["antispam"]}))
    response = clt.do_action_with_exception(request)
    result = json.loads(response.decode("utf-8"))
    data = {"label":"review", "score":0}
    if 200 == result["code"]:
        taskResults = result["data"]
        for taskResult in taskResults:
            if (200 == taskResult["code"]):
                sceneResults = taskResult["results"]

                for sceneResult in sceneResults:
                    label = sceneResult["label"]
                    suggestion = sceneResult["suggestion"]
                    # suggestion建议用户处理，取值范围：[“pass”, “review”, “block”], pass:文本正常，review：需要人工审核，block：文本违规，可以直接删除或者做限制处理

                    data = {"label":label, "suggestion":suggestion}
                    if suggestion == "pass":
                        # 正常
                        data["score"] = 0
                    elif suggestion == "block":
                        # 违规
                        data["score"] = 100
                        # 直接返回结果
                        return data
                    elif suggestion == "review":
                        # 需要人工鉴定
                        data["score"] = 0
                        # 直接返回结果
                        return data
        return data



'''
label
场景(scene)中文名	场景（scene）	分类（label）	备注
垃圾检测	antispam	normal	正常文本
垃圾检测	antispam	spam	含垃圾信息
垃圾检测	antispam	ad	广告
垃圾检测	antispam	politics	渉政
垃圾检测	antispam	terrorism	暴恐
垃圾检测	antispam	abuse	辱骂
垃圾检测	antispam	porn	色情
垃圾检测	antispam	flood	灌水
垃圾检测	antispam	contraband	违禁
垃圾检测	antispam	meaningless	无意义
'''
