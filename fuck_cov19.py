import logging
import time
import warnings

import requests

# 初始化日志以及警告配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S')
warnings.filterwarnings('ignore')

# 是否选择消息提醒
notice_enable = True

# 叮咚订购接口地址以及配置参数
url = "https://maicai.api.ddxq.mobi/order/getMultiReserveTime?products=%5B%5B%7B%22type%22%3A1%2C%22id%22%3A%225e9448aabdb365338d68b14c%22%2C%22price%22%3A%223.80%22%2C%22count%22%3A1%2C%22description%22%3A%22%22%2C%22sizes%22%3A%5B%5D%2C%22cart_id%22%3A%225e9448aabdb365338d68b14c%22%2C%22parent_id%22%3A%22%22%2C%22parent_batch_type%22%3A-1%2C%22category_path%22%3A%2258f9d213936edfe4568b569a%2C58fbf4fb936edf42508b4654%22%2C%22manage_category_path%22%3A%2221%2C25%2C28%22%2C%22activity_id%22%3A%22%22%2C%22sku_activity_id%22%3A%22%22%2C%22conditions_num%22%3A%22%22%2C%22product_name%22%3A%22%E7%B4%AB%E7%9A%AE%E5%A4%A7%E8%92%9C%20%E7%BA%A6250g%22%2C%22product_type%22%3A0%2C%22small_image%22%3A%22https%3A%2F%2Fimgnew.ddimg.mobi%2Fproduct%2F0031372aeb4041118e7be6687a6a6b9b.jpg%3Fwidth%3D800%26height%3D800%22%2C%22total_price%22%3A%223.80%22%2C%22origin_price%22%3A%223.80%22%2C%22total_origin_price%22%3A%223.80%22%2C%22no_supplementary_price%22%3A%223.80%22%2C%22no_supplementary_total_price%22%3A%223.80%22%2C%22size_price%22%3A%220.00%22%2C%22buy_limit%22%3A0%2C%22price_type%22%3A0%2C%22promotion_num%22%3A0%2C%22instant_rebate_money%22%3A%220.00%22%2C%22is_invoice%22%3A1%2C%22sub_list%22%3A%5B%5D%2C%22is_booking%22%3A0%2C%22is_bulk%22%3A0%2C%22view_total_weight%22%3A%22%E4%BB%BD%22%2C%22net_weight%22%3A%22250%22%2C%22net_weight_unit%22%3A%22g%22%2C%22storage_value_id%22%3A0%2C%22temperature_layer%22%3A%22%22%2C%22sale_batches%22%3A%7B%22batch_type%22%3A-1%7D%2C%22is_shared_station_product%22%3A0%2C%22is_gift%22%3A0%2C%22supplementary_list%22%3A%5B%5D%2C%22order_sort%22%3A15%2C%22is_presale%22%3A0%7D%5D%5D"
header = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123c) NetType/WIFI Language/zh_CN',
    'cookie': '',
    'ddmc-city-number': '0101',
    'ddmc-build-version': '2.81.4',
    'ddmc-device-id': '',
    'ddmc-station-id': '',
    'ddmc-channel': 'applet',
    'ddmc-longitude': '',
    'ddmc-latitude': '',
    'ddmc-uid': ''
}
params = {
    "uid": "624a4252ee8ec400017f2c8a",
    "longitude": "",
    "latitude": "",
    "station_id": "",
    "city_number": "0101",
    "api_version": "9.49.1",
    "app_version": "2.81.4",
    "applet_source": "",
    "channel": "applet",
    "app_client_id": "4",
    "sharer_uid": "",
    "s_id": "",
    "openid": "",
    "h5_source": "",
    "device_token": "",
    "address_id": "",
    "group_config_id": "",
    "isBridge": "false",
    "nars": "",
    "sesi": ""
}

# pushdeer 的配置参数 pushkey自己去拿
push_param = {
    "pushkey": "",
    "text": "叮咚可以抢菜拉！！！！！！！"
}
push_url = "https://api2.pushdeer.com/message/push"

# 检查今日是否有可以订购的时段
while True:
    response = requests.post(url=url, params=params, timeout=10000, headers=header, verify=False)

    if response.status_code != requests.codes.ok:
        logging.error("------------------- 获取订购时段失败 ------------------- ")
        continue

    json = response.json()

    day_times = json['data'][0]['time'][0]['times']

    can_order = False

    for t in day_times:
        if t['disableType'] == 0 and t['select_msg'] != '自动尝试可用时段':
            can_order = True
            break
    if can_order:
        logging.info("------------------- 今天可以选择付款时间段！！请火速抢购 --------------" + str(json['data'][0]['time'][0]['times']))
        if notice_enable:
            r = requests.post(push_url, params=push_param)
            if r.status_code == requests.codes.ok:
                logging.info("------------------- pushdeer通知发送成功 ------------------- ")
            else:
                logging.error("------------------- pushdeer通知发送失败 ------------------- ")
    else:
        logging.info("------------------- 今天暂无可以订购的时段 --------------" + str(json['data'][0]['time'][0]['times']))

    time.sleep(8)
