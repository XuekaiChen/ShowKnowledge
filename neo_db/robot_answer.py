from neo_db.classifier import Classifier
from neo_db.semantic_parser import SemanticParser
from neo_db.graph_matcher import GraphMatcher
from neo_db.fin_config import classifier_load_path, entity_searcher_load_path, chat_responses, question_types
from random import choice

# 加载闲聊分类器
classifier = Classifier(classifier_load_path)

# 加载语义解析器，预测问题类型和涉及的实体
semantic_parser = SemanticParser(entity_searcher_load_path, question_types)

# 加载图数据库查询
graph_matcher = GraphMatcher()


def get_robot_answer(query):
    # 预测 label 和概率
    query_intent_label, query_intent_prob = classifier.predict(query)
    response = ""
    # 知识问答
    semantics = semantic_parser.predict(query)
    if len(semantics['ques_types']) > 0 and len(semantics['entities']) > 0:
        response = graph_matcher.predict(semantics)
    # 闲聊
    elif query_intent_prob > 0.8:
        response = choice(chat_responses[query_intent_label])
    if response == "":
        response = choice(chat_responses['safe'])

    return response


if __name__ == '__main__':
    print(get_robot_answer('中信证券持有的股票有哪些？'))
    print("-"*100)
    print(get_robot_answer('宁德时代的概念是什么？'))

