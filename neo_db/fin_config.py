from py2neo import Graph

# 加载知识图谱
graph = Graph("http://localhost:7474", auth=("neo4j", "neo4j123"))

# 知识语料路径
entity_corpus_path = 'data/knowledge/'

# 实体搜索器存储路径
entity_searcher_save_path = 'checkpoints/entity_searcher/search_tree.pkl'

# 实体搜索器加载路径
entity_searcher_load_path = 'checkpoints/entity_searcher/search_tree.pkl'

# 分类器语料路径
classifier_corpus_path = 'data/classifier/chat.train'

# 分类器模型存储路径
classifier_save_path = 'checkpoints/classifier/model.bin'

# 分类器模型加载路径
classifier_load_path = 'checkpoints/classifier/model.bin'

# 闲聊回复语料库
chat_responses = {
    'qa': [],
    'greet': [
        'hello，很高兴为您服务，有什么可以为您效劳的呢？',
        '您好，可以输入股票名称或者代码查看详细信息哦',
        '您好，有股票相关的问题可以问我哦'
    ],
    'goodbye': [
        '再见',
        '有什么问题可以下次继续问我哦',
        '拜拜喽，别忘了给个小红心啊',
    ],
    'bot': [
        '没错，我就是集美貌与才智于一身的智能问答机器人',
        '为了防止世界被破坏，为了维护世界的和平，有任何需要我都会帮助你的'
    ],
    'safe': [
        '不好意思，您的问题我没太听懂，可以换一种说法嘛',
        '亲亲，这里好像没有您想要的答案'
    ]
}

# 问题类型
question_types = {
    'concept':
        ['概念', '特征'],
    'holder':
        ['股东'],
    'stock':
        ['股票', '持有', '控股', '控制'],
    'industry':
        ['行业', '领域'],
}

# 存储对话历史中上一次涉及的问题类型和实体
contexts = {
    'ques_types': None,
    'entities': None
}

# 节点Legend列表
CA_LIST = {"股东": 0, "股票": 1, "概念": 2}

d={
  "segments": [
    {
      "start": {
"identity": 0,
"labels": [
          "股票"
        ],
"properties": {
"股票名称": "泛海控股",
"TS代码": "000046.SZ",
"行业": "多元金融",
"股票代码": 46
        }
      },
      "relationship": {
"identity": 9601,
"start": 0,
"end": 4301,
"type": "所属概念",
"properties": {

        }
      },
      "end": {
"identity": 4301,
"labels": [
          "概念"
        ],
"properties": {
"概念代码": "TS199",
"概念名称": "房地产"
        }
      }
    }
  ],
  "length": 1.0
}
