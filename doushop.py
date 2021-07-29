#coding:utf8
"""
发布日期：2021.07.29
主要针对抖店第三方开发者文档的第二个版本，也就是发布日期最新接口。
"""
import requests
import traceback
import time
import hashlib
import json
import asyncio

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.ioloop import IOLoop

from conf import ConfDoushop

import uuid
import whatwg_url

debug = 0


# await order_dao.add_order(data)
# await product_dao.add_product(data)

class DouShopProxy(ConfDoushop):
    """docstring for DouShopProxy"""

    def __init__(self):
        super(DouShopProxy, self).__init__()
        self.base_url = "https://openapi-fxg.jinritemai.com/{}?app_key=" + self.APP_KEY + "&"
        self.async_client = AsyncHTTPClient()

        """
        the get_access_token recv is: {'data': {'access_token': '54aab0dc-9b7a-4320-952f-57187498dd80', 'expires_in': 242893, 'refresh_token': '9890778e-6269-47d0-9da5-36c6c965360e', 'scope': 'SCOPE', 'shop_id': 7743045, 'shop_name': 'H的礼物清单'}, 'err_no': 0, 'log_id': '2021072522484501013113214408A67B55', 'message': 'success'}
        """
#         IOLoop.current().spawn_callback(self.auto_update_token)
#         IOLoop.current().spawn_callback(self.sync_orders)
#         IOLoop.current().spawn_callback(self.sync_products)

    async def auto_update_token(self):
        while True:
            print(" start auto_update_token" )
            now_time = time.time()
            # 提前1个小时更新
            delta_time = self.expires_in-now_time + self.get_token_time -60*60
            print("the sleep time is:",delta_time)
            await asyncio.sleep(delta_time)
            await self.get_refresh_token()

    def create_sign(self, method, param_json, timestamp):
        """
        创建签名
        """
        myStr = self.APP_SECRET + "app_key" + self.APP_KEY + "method" + method + "param_json" + param_json + "timestamp" + timestamp + "v2" + self.APP_SECRET
        md5 = hashlib.md5(myStr.encode()).hexdigest()
        return md5

    @staticmethod
    def get_date():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    async def get_access_token(self):
        """
        首次获取token
        the jdata is: {'data': {'access_token': '54aab0dc-9b7a-4320-952f-57187498dd80', 'expires_in': 604800, 'refresh_token': '9890778e-6269-47d0-9da5-36c6c965360e', 'scope': 'SCOPE', 'shop_id': 7743045, 'shop_name': 'H的礼物清单'}, 'err_no': 0, 
        """
        if debug:
            self.access_token = "fc04a1f7-d341-49fd-9112-492830508e68"
            self.expires_in = 604800
            self.refresh_token = 'c4e3e3f2-4938-4779-9191-5d6ed8429486'
            return None
        try:
            timestamp = self.get_date()
            method = "token.create"
            param_json = json.dumps({"code": "", "grant_type": "authorization_self", "shop_id": self.shop_id}).replace(
                ' ', '')
            sign = self.create_sign(method, param_json, timestamp)
            token_url = self.base_url.format(
                "token/create") + "method=token.create&param_json=" + param_json + "&timestamp=" + timestamp + "&v=2&sign=" + sign

            token_url = whatwg_url.urlparse(token_url)
            token_url = token_url.geturl()

            # res = requests.get(token_url)
            print(token_url)
            req = HTTPRequest(token_url)
            resp = await self.async_client.fetch(req)
            # jdata = res.json()
            jdata = json.loads(resp.body)
            print("the get_access_token recv is:", jdata)
            message = jdata.get("message", "")
            if message == "success":
                self.access_token = jdata.get("data", {}).get("access_token", None)
                self.expires_in = int(jdata.get("data", {}).get("expires_in", None))
                self.refresh_token = jdata.get("data", {}).get("refresh_token", None)
        except:
            traceback.print_exc()

    async def get_refresh_token(self):
        '''
        刷新token
        '''

        try:
            print("the self.refresh_token", self.refresh_token)
            method = "token.refresh"
            uri = "token/refresh"
            param_json = json.dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token}).replace(' ',
                                                                                                                  '')

            jdata = await self.base_request_data_doushop(method, uri, param_json)
            print("the get_refresh_token recv is:", jdata)

            if jdata:
                self.access_token = jdata.get("data", {}).get("access_token", None)
                self.expires_in = jdata.get("data", {}).get("expires_in", None)
                self.refresh_token = jdata.get("data", {}).get("refresh_token", None)
                self.get_token_time = time.time()
        except:
            traceback.print_exc()

    # product/list
    async def get_products_list(self):
        '''
        获取产品列表
        '''

        try:
            # print ("the self.refresh_token",self.refresh_token)
            method = "product.listV2"
            uri = "product/listV2"
            # 已上架
            start_page = 1
            size = 10
            while 1:
                param_json = json.dumps({"page": start_page, "size": size,"status":0}).replace(' ', '')
                # https://openapi-fxg.jinritemai.com/shop/getShopCategory?app_key=your_app_key_here&method=shop.getShopCategory&access_token=your_accesstoken_here&param_json={"cid":"0"}&timestamp=2018-06-19 16:06:59&v=2&sign=your_sign_here
                jdata =await self.base_request_data_doushop(method, uri, param_json)
                recv_data = jdata.get("data")
                if not recv_data:
                    break
                product_list = recv_data.get("data",None)
                if not product_list:
                    break
                for product in product_list:
                    pass
                    # print("\n\n\n\n\the get_products_list recv is:", jdata)
                    # TODO：业务处理
                start_page+=1
                # return jdata
        except:
            traceback.print_exc()    

    async def get_orders_list(self):
        """
        获取订单列表
        """
        try:
            start_time = await self.get_db_lastest_order()

            # print ("the self.refresh_token",self.refresh_token)
            method = "order.searchList"
            uri = "order/searchList"
            page, size = 0, 10
            while True:
                create_time_start = start_time  # TODO 每次去数据库查询最近的 update_time
                param_json = json.dumps({"create_time_start": create_time_start, "page": page, "size": size}).replace(
                    ' ', '')
                jdata = await self.base_request_data_doushop(method, uri, param_json)

                print("the get_orders_list recv is:", jdata)
                if not jdata.get("data") and jdata.get("data").get("shop_order_list"):
                    break
                order_list = jdata.get("data").get("shop_order_list")
                for order in order_list:
                    print('the order is:",order)
                page += 1
                if len(order_list) < size:
                    return
                await asyncio.sleep(5)
            # https://openapi-fxg.jinritemai.com/shop/getShopCategory?app_key=your_app_key_here&method=shop.getShopCategory&access_token=your_accesstoken_here&param_json={"cid":"0"}&timestamp=2018-06-19 16:06:59&v=2&sign=your_sign_here

        except:
            traceback.print_exc()
            return None

    def get_orders_detail(self, order_id=""):
        try:
            # print ("the self.refresh_token",self.refresh_token)
            method = "order.orderDetail"
            uri = "order/orderDetail"
            param_json = json.dumps({"shop_order_id": order_id}).replace(' ', '')
            jdata = self.base_request_data_doushop(method, uri, param_json)
            print("the get_orders_detail recv is:", jdata)
            # https://openapi-fxg.jinritemai.com/shop/getShopCategory?app_key=your_app_key_here&method=shop.getShopCategory&access_token=your_accesstoken_here&param_json={"cid":"0"}&timestamp=2018-06-19 16:06:59&v=2&sign=your_sign_here

        except:
            traceback.print_exc()

    async def base_request_data_doushop(self, method, uri, param_json):
        timestamp = self.get_date()
        sign = self.create_sign(method, param_json, timestamp)
        token_url = self.base_url.format(
            uri) + "method=" + method + "&access_token=" + self.access_token + "&param_json=" + param_json + "&timestamp=" + timestamp + "&v=2&sign=" + sign

        token_url = whatwg_url.urlparse(token_url)
        token_url = token_url.geturl()

        res = requests.get(token_url)
        resp = await self.async_client.fetch(HTTPRequest(token_url))
        jdata = json.loads(resp.body)
        print(jdata)
        message = jdata.get("message", "")
        if message == "success":
            return jdata
        return None

    async def base_request_logistic_company_list(self):
        method = "order.logisticsCompanyList"
        url = "order/logisticsCompanyList"
        res = await self.base_request_data_doushop(method, url, "{}")
        if not res:
            return []
        return res.get("data")

    async def update_logistic_company(self):
        logistic_company_list = await self.base_request_logistic_company_list()
        for company in logistic_company_list:
            name = company.get("name")
            code = company.get("code")
            if all((name, code)):
                self.logistic_company.setdefault(name, code)

    async def post_order_logisticsAdd(self, order_id, company, logistics_code):
        """
        该接口是发所有订单中只有一个货物的订单

        order_id  订单号
        company 物流公司名称 eg: 顺丰
        logistics_code 快递单号
        """
        # 订单发货接口,当该订单只包含一个sku时，调用该接口，
        company_code = None
        if not self.logistic_company.get(company):
            await self.update_logistic_company()
        company_code = self.logistic_company.get(company)
        if not company_code:
            print(f"company: {company} not found")
            return
        try:
            method = "order.logisticsAdd"
            uri = "order/logisticsAdd"
            param_json = json.dumps(
                {"company_code": company_code, "logistics_code": logistics_code, "order_id": order_id}).replace(' ', '')
            print("the param_json got:", param_json)
            jdata = await self.base_request_data_doushop(method, uri, param_json)
            print("the get_orders_list recv is:", jdata)
            # https://openapi-fxg.jinritemai.com/shop/getShopCategory?app_key=your_app_key_here&method=shop.getShopCategory&access_token=your_accesstoken_here&param_json={"cid":"0"}&timestamp=2018-06-19 16:06:59&v=2&sign=your_sign_here
            # import pdb;pdb.set_trace()
        except:
            traceback.print_exc()

    async def post_order_logisticsAddMultiPack(self, order_id, shipped_order_id, company, logistics_code, item_num):
        """
        该接口是发订单中有多个货物的订单

        order_id  父订单号
        shipped_order_id 所发货物子订单号
        company 物流公司名称 eg: 顺丰
        logistics_code 快递单号
        item_num skulist 中的参数，原样传入即可
        """
        # 一个父订单发多个货接口，一个父订单包含多个skulist
        company_code = None
        if not self.logistic_company.get(company):
            await self.update_logistic_company()

        company_code = self.logistic_company.get(company)
        if not company_code:
            print(f"company: {company} not found")
            return

        request_id = str(uuid.uuid1())
        try:
            method = "order.logisticsAddMultiPack"
            uri = "order/logisticsAddMultiPack"
            param_json = json.dumps(
                {"order_id": order_id,
                 "pack_list": [
                     {
                         "company_code": company_code,
                         "logistics_code": logistics_code,
                         "shipped_order_info": [
                             {
                                 "shipped_num": item_num,
                                 "shipped_order_id": shipped_order_id
                             }
                         ]
                     }
                 ],
                 "request_id": request_id}).replace(' ', '')
            print("the param_json", param_json)
            jdata = await self.base_request_data_doushop(method, uri, param_json)
            print("the get_orders_list recv is:", jdata)
            # https://openapi-fxg.jinritemai.com/shop/getShopCategory?app_key=your_app_key_here&method=shop.getShopCategory&access_token=your_accesstoken_here&param_json={"cid":"0"}&timestamp=2018-06-19 16:06:59&v=2&sign=your_sign_here
            # import pdb;pdb.set_trace()
        except:
            traceback.print_exc()




if __name__ == '__main__':
    d = DouShopProxy()
    import asyncio
    # 获取token
    IOLoop.current().run_sync(d.get_access_token)
    # 获取订单列表
    IOLoop.current().run_sync(d.get_orders_list)



