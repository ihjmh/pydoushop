"""
初始化及一些配置
"""
logistic_company = {
    '当当物流': 'dangdang',
    '海信物流': 'savor',
    '壹米滴答': 'yimidida',
    '众邮快递': 'zhongyouex',
    '天地华宇': 'tiandihuayu',
    '南方传媒物流': 'ndwl',
    '安迅物流': 'anxl',
    '东风快递': 'dfkuaidi',
    '中铁快运': 'ztky',
    '盛丰物流': 'sfwl',
    '安能物流': 'annengwuliu',
    '京广速递': 'jinguangsudikuaijian',
    '安得物流': 'annto',
    '丰通快运': 'ftky365',
    '圆通快递(常用)': 'yuantong',
    '百世快递(常用)': 'huitongkuaidi',
    '顺丰速运(常用)': 'shunfeng',
    '盛辉物流': 'shenghuiwuliu',
    '宅急送': 'zhaijisong',
    '九曳供应链': 'jiuyescm',
    '顺心捷达': 'sxjdfreight',
    '优速物流': 'youshuwuliu',
    '日日顺物流': 'rrs',
    '林氏物流': 'linshiwuliu',
    '百事亨通': 'bsht',
    '丹鸟': 'danniao',
    '泰进物流': 'taijin',
    '当当': 'dangdangorder',
    '黄马甲': 'huangmajia',
    '丰网速运': 'fengwang',
    '安鲜达': 'exfresh',
    '韵达快运': 'yundakuaiyun',
    '加运美速递': 'jym56',
    '品骏快递': 'pjbest',
    '天天快递': 'tiantian',
    '中通快运': 'zhongtongkuaiyun',
    '特急送': 'lntjs',
    '全峰快递': 'quanfengkuaidi',
    '圆通快运': 'yuantongkuaiyun',
    '中通速递(常用)': 'zhongtong',
    '申通快递(常用)': 'shentong',
    '如风达': 'rufengda',
    '万象物流': 'wanxiangwuliu',
    '运通中港快递': 'ytkd',
    '邮政国内': 'yzguonei',
    'EMS(常用)': 'ems',
    '微特派': 'weitepai',
    '极兔速递': 'jtexpress',
    '国通快递': 'guotongkuaidi',
    '芝麻开门': 'zhimakaimen',
    '中粮鲜到家物流': 'zlxdjwl',
    '中邮速递': 'wondersyd',
    '韵达快递(常用)': 'yunda',
    '佳怡物流': 'jiayiwuliu',
    '苏宁物流': 'suning',
    '增益速递': 'zengyisudi',
    '邮政快递包裹': 'youzhengguonei',
    '佳吉快运': 'jiajiwuliu',
    'D速快递': 'dsukuaidi',
    '速尔快递': 'suer',
    '跨越速运': 'kuayue',
    '快捷快递': 'kuaijiesudi',
    '京东物流(常用)': 'jd',
    '顺丰快运': 'shunfengkuaiyun',
    '山西建华': 'shanxijianhua',
    '德邦快递(常用)': 'debangwuliu',
    '百世快运': 'baishiwuliu'
}


class ConfDoushop(object):
    """docstring for ConfDoushop"""

    def __init__(self):
        self.APP_KEY = "app_key"
        self.APP_SECRET = "APP_SECRET"
        self.shop_id = 4343434
        self.get_token_time = 1626863610
        self.expires_in = 523957
        self.access_token = "access_token"
        self.refresh_token = "refresh_token"
        self.logistic_company = logistic_company
        self.sync_order_faild_time = 60*60*24  # 如果数据同步失败，或者没有找到最老的数据，就拉取24小时之前的
        self.sync_order_timer = 60*60 # 订单定时同步时间，目前是一小时一次
        

