# 爬虫设置
SPIDER_CONF={
    'zbytb':{
        'name':'zbytb',
        'db_type':'mongo',#存储数据库类型
        'db_name':'GatherDatas',#数据库名
        'col_name':'GatherDatas',#集合名
        'db_connection':'mongodb://192.168.0.56:27017',
        'proxy_type':'free',
        'is_proxy':True,
        'url_parse':{
            'parse_type':'xpath',
            'pattern':['//td[@class="zblist_xm"]/a/@href']
        },
        'content_parse':{
            'pattern':{
                'title':['xpath','//p[@id="title"]/text()',0],#第一个参数解析方式，第二个是解析模式，第三个是具体位置
                'public_time':['xpath','//p[@class=" t_c h_50"]/span/text()',0],
                'area':['xpath','//tr/td/text()',1],
                'procurement_unit':['re','\u53d7.*[\u53f8]',0,1],#第一个是下标 第二是截取长度
                'description':['third',['//div[@class="texts"]/text()']],
                'open_tendering_date':['re','\u62a5\u540d\u65f6\u95f4\uff1a.*|\u5f00\u6807\uff1a.*|\u53d1\u5e03\u65e5\u671f\uff1a.*',0,4],

            },
        },
        'store_html':True,#存储原网页
        'is_write':True,#是否写入
        'kws':["银行", '信贷、银行', '银行、信贷','信贷','消费金融、银行', '反欺诈、银行', '风控、银行','风险控制、银行','征信报告、银行', '模型、银行', '零售、信用卡'],

    },
    'ccgp':{
        'name':'ccgp',
        'db_type':'mongo',
        'db_name':'GatherDatas',
        'col_name':'GatherDatas',
        'db_connection':'mongodb://192.168.0.56:27017',
        'proxy_type':'free',
        'is_proxy':False,
        'url_parse':{
            'parse_type':'xpath',
            'pattern':['//ul[@class="vT-srch-result-list-bid"]/li/a/@href']
        },
        'content_parse':{
            'pattern':{
                'title':['xpath','//td[@class="title"]/following-sibling::td/text()',0],#第一个参数解析方式，第二个是解析模式，第三个是具体位置
                'public_time':['xpath','//span[@id="pubTime"]/text()',0],
                'area':['xpath','//td[@width="168"]/text()',0],
                'procurement_unit':['xpath','//td[@colspan="3"]/text()',1],#第一个是下标 第二是截取长度
                'description':['third',['//table/tr/td/text()','//div[@class="vF_detail_content"]']],
                'open_tendering_date':['xpath',' ',0],

            },
        },
        'store_html':True,#存储原网页
        'is_write':True,#是否写入
        'kws':["银行", '信贷、银行', '银行、信贷','信贷','消费金融、银行', '反欺诈、银行', '风控、银行','风险控制、银行','征信报告、银行', '模型、银行', '零售、信用卡'],


    },
    'jincai': {
        'name':'jincai',
        'db_type':'mongo',
        'db_name':'GatherDatas',
        'col_name':'GatherDatas',
        'db_connection':'mongodb://192.168.0.56:27017',
        'proxy_type':'free',
        'is_proxy':False,
        'url_parse':{
            'parse_type':'xpath',
            'pattern':['//p[@class="cfcpn_list_title"]/a/@href']
        },
        'content_parse':{
            'pattern':{
                'title':['xpath','//p[@class="cfcpn_news_title"]/text()',0],#第一个参数解析方式，第二个是解析模式，第三个是具体位置
                'public_time':['xpath','//p[@class="cfcpn_news_date"]/text()',0],
                'area':['xpath','//p[@style="margin-bottom:0px;"]/following-sibling::p/text()',2],
                'procurement_unit':['xpath','//p[@style="margin-bottom:0px;"]/following-sibling::p/text()',0],#第一个是下标 第二是截取长度
                'description':['third',['//div[@class="notice_describe"]/p/span/text()']],
                'open_tendering_date':['re','\u65e5\u671f\uff1a.*|\u65f6\u95f4\uff1a.*|' ,0,3],

            },
        },
        'store_html':True,#存储原网页
        'is_write':True,#是否写入
        'kws':["银行", '信贷、银行', '银行、信贷','信贷','消费金融、银行', '反欺诈、银行', '风控、银行','风险控制、银行','征信报告、银行', '模型、银行', '零售、信用卡'],



    },
}

# 重试次数
RETYE_TIME=3
# 没有响应时默认的抓取页数
DEFAULT_PAGE=20
#报警时间s
ALARM_TIME=30*60