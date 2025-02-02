from dataclasses import dataclass
from datetime import datetime

from bgutils import dtUtil
from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderCar(BaseSpider):
    title: str #小车名称
    style: str #小车类型
    desc: str #书描述
    price: str #车价
    pic: str #车图片
    regdate: str #注册日期
    distance: str #行驶路程


    def __init__(self, username, collector, rawurl, rawdata):
        super().__init__(username, collector, "car_data", rawurl, rawdata)
        return
