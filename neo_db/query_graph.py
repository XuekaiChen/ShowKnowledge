# -*- coding: utf-8 -*-
# Date        : 2022/5/19
# Author      : Chen Xuekai
# Description :

import sys
import json
from neo_db.fin_config import graph
from pprint import pprint


# 因为数据格式实在不固定，只能每类单独写了
def query(node_cate, q_content):
    json_data = {'nodes': [], "links": []}

    # 总布局：股东-[持有]->股票-[所属概念]->概念
    if node_cate == '0':  # 股东
        data = graph.run("match(p:`股东`{`股东名称`:'%s'})-[r]->(n) return n" % q_content)
        data = list(data)

        if len(data) == 0:
            pass
        else:
            # 添加查询节点
            node = {
                'id': 0,
                'name': q_content,
                'category': 0  # 股东
            }
            json_data['nodes'].append(node)
            # # 添加受体节点
            for idx, n in enumerate(data):
                node = {
                    'id': idx + 1,
                    'name': n['n']['股票名称'],
                    'category': 1  # 股票
                }
                json_data['nodes'].append(node)
            # 添加关系
            for idx in range(len(data)):
                link = {
                    'source': 0,
                    'target': idx + 1,
                    'value': "持有"
                }
                json_data['links'].append(link)

    elif node_cate == '1':  # 股票
        data1 = list(graph.run("match(p)-[r]->(n:`股票`{`股票名称`:'%s'}) return p" % q_content))
        if len(data1) == 0:
            pass
        else:
            # 添加查询节点
            node = {
                'id': 0,
                'name': q_content,
                'category': 1  # 股票
            }
            json_data['nodes'].append(node)
            # 添加节点
            for idx, n in enumerate(data1):
                node = {
                    'id': idx + 1,
                    'name': n['p']['股东名称'],
                    'category': 0
                }
                json_data['nodes'].append(node)
            # 添加关系
            for idx in range(len(data1)):
                link = {
                    'source': idx + 1,
                    'target': 0,
                    'value': "持有"
                }
                json_data['links'].append(link)

        data2 = list(graph.run("match(p:`股票`{`股票名称`:'%s'})-[r]->(n) return n" % q_content))
        if len(data2) == 0:
            pass
        else:
            if len(data1) == 0:
                node = {
                    'id': 0,
                    'name': q_content,
                    'category': 1  # 股票
                }
                json_data['nodes'].append(node)
            else:
                existing = len(json_data['nodes'])
                # 添加受体节点
                for idx, n in enumerate(data2):
                    node = {
                        'id': existing + idx,
                        'name': n['n']['概念名称'],
                        'category': 2
                    }
                    json_data['nodes'].append(node)
                # 添加关系
                for idx in range(len(data2)):
                    link = {
                        'source': 0,
                        'target': existing + idx,
                        'value': "所属概念"
                    }
                    json_data['links'].append(link)

    elif node_cate == '2':  # 概念
        data = graph.run("match(p)-[r]->(n:`概念`{`概念名称`:'%s'}) return p" % q_content)
        data = list(data)

        if len(data) == 0:
            pass
        else:
            # 添加查询节点
            node = {
                'id': 0,
                'name': q_content,
                'category': 2  # 概念
            }
            json_data['nodes'].append(node)
            # 添加节点
            for idx, n in enumerate(data):
                node = {
                    'id': idx + 1,
                    'name': n['p']['股票名称'],
                    'category': 1  # 股票
                }
                json_data['nodes'].append(node)
            # 添加关系
            for idx in range(len(data)):
                link = {
                    'source': idx + 1,
                    'target': 0,
                    'value': "所属概念"
                }
                json_data['links'].append(link)

    else:
        sys.exit()

    return json_data  # 返回列表[json_data{data:[],links:[]}, detail_chart{key:value}]


# 点击echarts元素时获取信息表
def get_details(node_or_edge, data, nodes):  # json类型的p/r/n
    """
    node_or_edge: node
    data: {'category': 0, 'id': 0, 'name': '王石'}
    nodes: [{'category': 0, 'id': 0, 'name': '王石'}, {'category': 1, 'id': 1, 'name': '宝莱特'}]

    edge
    {'source': 0, 'target': 1, 'value': '持有'}
    [{'category': 0, 'id': 0, 'name': '王石'}, {'category': 1, 'id': 1, 'name': '宝莱特'}]
    """
    result = {}
    if node_or_edge == 'node':
        if data['category'] == 0:  # 股东
            result = {'id': data['id'], '股东名称': data['name']}
        elif data['category'] == 1:  # 股票
            result['id'] = data['id']
            response = list(graph.run("MATCH (n:`股票`{`股票名称`:'%s'}) RETURN n" % data['name']))
            for i in response[0]['n']:
                result[i] = str(response[0]['n'][i])

        elif data['category'] == 2:  # 概念
            result['id'] = data['id']
            response = list(graph.run("MATCH (n:`概念`{`概念名称`:'%s'}) RETURN n" % data['name']))
            for i in response[0]['n']:
                result[i] = str(response[0]['n'][i])

    elif node_or_edge == 'edge':
        if data['value'] == '持有':
            result['关系类型'] = '持有'
            source = [item['name'] for item in nodes if item['id']==data['source']][0]
            target = [item['name'] for item in nodes if item['id']==data['target']][0]
            response = list(
                graph.run("MATCH l=(p:`股东`{`股东名称`:'%s'})-[r:`持有`]->(n:`股票`{`股票名称`:'%s'}) RETURN r" % (source, target))
            )
            for i in response[0]['r']:
                result[i] = response[0]['r'][i]
                if i == '占比':
                    result[i] = str(response[0]['r'][i]) + '%'

        elif data['value'] == '所属概念':
            result = {'关系类型': '所属概念'}

    else:
        sys.exit()

    chart = dict_to_html(result)
    return chart


# 将get_details得到的dict转换为html格式
def dict_to_html(info_dict):  # dict{key: value}
    s = ''
    for key, value in info_dict.items():
        st = "<dt class = \"basicInfo-item name\" >" + str(key) + " \
                    <dd class = \"basicInfo-item value\" >" + str(value) + "</dd >"
        s += st
    return s


#
def get_all_graph(choice, limit):
    json_data = {'nodes': [], "links": []}

    if choice == '0':  # 持有
        response = graph.run("MATCH (p)-[r:`持有`]->(n) RETURN p,id(p),labels(p),r,n,id(n),labels(n) LIMIT %d" % int(limit)).data()  # list
        exist_name = []
        for line in response:
            if line['p']['股东名称'] not in exist_name:
                source = {
                    'id': len(exist_name),
                    'name': line['p']['股东名称'],
                    'category': 0
                }
                exist_name.append(line['p']['股东名称'])
                json_data['nodes'].append(source)
            else: pass
            if line['n']['股票名称'] not in exist_name:
                target = {
                    'id': len(exist_name),
                    'name': line['n']['股票名称'],
                    'category': 1
                }
                exist_name.append(line['n']['股票名称'])
                json_data['nodes'].append(target)
            else: pass
            link = {
                'source': exist_name.index(line['p']['股东名称']),
                'target': exist_name.index(line['n']['股票名称']),
                'value': '持有'
            }
            json_data['links'].append(link)

    elif choice == '1':  # 所属概念
        response = graph.run("MATCH (p)-[r:`所属概念`]->(n) RETURN p,id(p),labels(p),r,n,id(n),labels(n) LIMIT %d" % int(limit)).data()  # list
        exist_name = []
        for line in response:
            if line['p']['股票名称'] not in exist_name:
                source = {
                    'id': len(exist_name),
                    'name': line['p']['股票名称'],
                    'category': 1
                }
                exist_name.append(line['p']['股票名称'])
                json_data['nodes'].append(source)
            else:
                pass
            if line['n']['概念名称'] not in exist_name:
                target = {
                    'id': len(exist_name),
                    'name': line['n']['概念名称'],
                    'category': 2
                }
                exist_name.append(line['n']['概念名称'])
                json_data['nodes'].append(target)
            else:
                pass
            link = {
                'source': exist_name.index(line['p']['股票名称']),
                'target': exist_name.index(line['n']['概念名称']),
                'value': '所属概念'
            }
            json_data['links'].append(link)

    return json_data


if __name__ == "__main__":
    # js_data0 = query(0, "中信证券")
    # pprint(js_data0)
    # print("-" * 100)
    # js_data1 = query(1, "宁德时代")
    # pprint(js_data1)
    # print("-"*100)
    # js_data2 = query(2, "券商")
    # pprint(js_data2)

    # node_or_edge = 'node'
    # data = {'category': 0, 'id': 0, 'name': '王石'}
    # nodes = [{'category': 0, 'id': 0, 'name': '王石'}, {'category': 1, 'id': 1, 'name': '宝莱特'}]
    # node_or_edge = 'edge'
    # data = {'source': 0, 'target': 1, 'value': '持有'}
    # nodes = [{'category': 0, 'id': 0, 'name': '王石'}, {'category': 1, 'id': 1, 'name': '宝莱特'}]
    # get_details(node_or_edge, data, nodes)

    js_data = get_all_graph('0', '25')
    pprint(js_data)

