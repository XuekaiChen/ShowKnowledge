from py2neo import Graph


class GraphMatcher:
    """基于 cypher 语句查询数据库"""

    def __init__(self):
        self.graph = Graph('http://localhost:7474/finance_demo/db/', auth=('neo4j', 'neo4j123'))

    def parse_graph(self, ques_types, entities):
        """转换成 cypher 语句查询"""

        response = ""
        for each_ques_type in ques_types:
            # 问所属概念
            if each_ques_type == 'concept':
                for entity_name, entity_type in entities.items():
                    # 1、问股票的概念
                    if entity_type == '股票':
                        cypher_sql = f'MATCH (s:`股票`)-[r:所属概念]->(c:`概念`) where s.股票名称 = "{entity_name}" return c.概念名称'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'{entity_name}所属概念有{"、".join([i["c.概念名称"] for i in rtn])}<br>'
                    # 2、问概念有哪些股票
                    elif entity_type == '概念':
                        cypher_sql = f'MATCH (s:`股票`)-[r:所属概念]->(c:`概念`) where c.概念名称 = "{entity_name}" return s.股票名称'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'{entity_name}概念下有{"、".join([i["s.股票名称"] for i in rtn])}这些股票<br>'

            # 问股东的股票
            elif each_ques_type == 'stock':
                for entity_name, entity_type in entities.items():
                    cypher_sql = f'MATCH (s:`股东`)-[r:持有]->(c:`股票`) where s.股东名称 = "{entity_name}" return c.股票名称, r.持有量, r.占比'
                    rtn = self.graph.run(cypher_sql).data()
                    response = f'{entity_name}持有股票的情况如下:\n'
                    for i in rtn:
                        response += f'{i["c.股票名称"]}，持有股份{i["r.持有量"]}，占比{i["r.占比"]}%<br>'

            # 问股票的股东
            elif each_ques_type == 'holder':
                for entity_name, entity_type in entities.items():
                    cypher_sql = f'MATCH (s:`股东`)-[r:持有]->(c:`股票`) where c.股票名称 = "{entity_name}" return s.股东名称, r.持有量, r.占比'
                    rtn = self.graph.run(cypher_sql).data()
                    response = f'{entity_name}的股东是:\n'
                    for i in rtn:
                        response += f'{i["s.股东名称"]}，持有股份{i["r.持有量"]}，占比{i["r.占比"]}%<br>'

            # 问行业、领域
            elif each_ques_type == 'industry':
                # 提示：match 股票 return 行业
                for entity_name, entity_type in entities.items():
                    # 1、股票所属行业
                    if entity_type == '股票':
                        cypher_sql = f'MATCH (s:`股票`) where s.股票名称="{entity_name}" return s.行业'
                        rtn = self.graph.run(cypher_sql).data()
                        response += f'{entity_name}所属行业是{rtn[0]["s.行业"]}<br>'
                pass
        return response.strip()

    def predict(self, semantics):
        """预测 query"""
        response = self.parse_graph(semantics['ques_types'], semantics['entities'])
        return response
