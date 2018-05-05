# -*-coding:utf-8-*-

__author__ = "Allen Woo"
PLUGIN_NAME = "aliyun_textscan_plugin"

CONFIG = {
    "ACCESS_KEY":{
        "info":"ACCESS KEY ID",
        "value_type":"string",
        "value":"<Your AK ID>",
        "reactivate":True
    },
    "SECRET_KEY":{
        "info":"SECRET KEY",
        "value_type":"password",
        "value":"<Your SK>",
        "reactivate":True
    },
    "REGION_ID":{
        "info":"region_id:cn-shanghai, cn-hangzhou等",
        "value_type":"string",
        "value":"cn-shanghai",
        "reactivate":True
    }

}

