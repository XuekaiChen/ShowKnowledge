from flask import Flask, render_template, request, jsonify, json
from neo_db.query_graph import query, get_details, get_all_graph
from neo_db.robot_answer import get_robot_answer

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/query_node', methods=['GET', 'POST'])
def search_page():
    return render_template('query_node.html')


@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


@app.route('/dialogue', methods=['GET', 'POST'])
def dialogue_page():
    # 需要返回json数据格式嵌入HTML
    return render_template('dialogue.html')


@app.route('/get_profile',methods=['GET','POST'])
def get_profile():
    choice = request.args.get('choice')
    limit = request.args.get('limit')
    json_data = get_all_graph(choice, limit)
    return jsonify(json_data)


@app.route('/search_node', methods=['GET', 'POST'])
def search_node():
    choice = request.args.get('choice')
    name = request.args.get('name')
    json_data = query(choice, str(name))
    return jsonify(json_data)


@app.route('/get_chart', methods=['GET', 'POST'])
def get_chart():
    node_or_edge = json.loads(request.form.get('type'))   # $.ajax传多个参数只能post请求，对应form
    data = json.loads(request.form.get('data'))
    nodes = json.loads(request.form.get('nodes'))
    json_data = get_details(node_or_edge, data, nodes)
    return jsonify(json_data)


@app.route('/dialogue_answer', methods=['GET', 'POST'])
def dialogue_answer():
    question = request.args.get('name')
    robot_answer = get_robot_answer(str(question).strip())
    json_data = {'data': robot_answer}
    json_data['data'].replace("\n", "<br>")
    return jsonify(json_data)


if __name__ == '__main__':
    app.debug = True
    app.run()
