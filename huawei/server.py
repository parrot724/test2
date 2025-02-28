import json
import base64
import os
import random
import string

from flask import Flask, url_for, request, make_response, redirect, session, escape
from pymongo import MongoClient
from PIL import Image
from pdf2image import convert_from_path

client = MongoClient()

app = Flask(__name__)
app.secret_key = b'you_can-never-guess/me/haha|yeah'
os.environ['FLASK_DEBUG'] = str(1)

if not os.path.exists(os.path.abspath('./tmp/classes')):
    os.makedirs(os.path.abspath('./tmp/classes'))

@app.errorhandler(404)
def page_not_found(error):
    return "path is wrong, check your path"


@app.route("/")
def root():
    return 'hello flask'


def write_class_data_to_file(className):
    try:
        classPages = client.socog.hwclass.find_one({'className': className})
        classPages['_id'] = None
        with open('tmp/classes/%s.json' % className, 'w', encoding="utf-8") as f:
            f.write(json.dumps(classPages, ensure_ascii=False))
        with open('tmp/classes/%s.txt' % className, 'w', encoding="utf-8") as f:
            for pagex, page in enumerate(classPages['pages']):
                if len(page['pageNotes']) is not 0:
                    f.write(str(pagex + 1))
                for notex, note in enumerate(page['pageNotes']):
                    f.write('-%s:%s:(%s, %s, %s, %s)' % (
                    notex + 1, note['noteContent'], note['x'], note['y'], note['width'], note['height']))
                f.write('\n')
    except Exception as e:
        print(e)

@app.route("/get_class_data")
def get_class_data():
    className = request.args.get("className", None)
    if className is None:
        res = make_response(json.dumps({'ok': False, 'message': 'no className parameter'}))
        res.headers['access-control-allow-origin'] = '*'
        return res
    try:
        classPages = client.socog.hwclass.find_one({'className': className})
        classPages['_id'] = None
        res = make_response(json.dumps({'ok': True, 'data': classPages}))
    except Exception as e:
        # print(e)
        res = make_response(json.dumps({'ok': False, 'message': type(e)}))
    res.headers['access-control-allow-origin'] = '*'
    return res


@app.route("/update_class_data", methods=["POST"])
def update_class_data():
    body = request.get_data().decode('utf8')
    body = json.loads(body)
    className = body['className']
    pageIndex = body['pageIndex']
    pageNotes = body['pageNotes']
    keyOfPageNotes = "pages." + str(pageIndex) + ".pageNotes"
    updateObject = {
        "$set": {
            keyOfPageNotes: pageNotes
        }
    }
    # client.socog.hwclass.update_one({'className': className}, updateObject)
    try:
        client.socog.hwclass.update_one({'className': className}, updateObject)
        write_class_data_to_file(className)
        res = make_response(json.dumps({'ok': True}))
    except Exception as e:
        print(e)
        res = make_response(json.dumps({'ok': False, 'message': e}))
    res.headers['access-control-allow-origin'] = '*'
    return res


@app.route("/upload_class", methods=["POST"])
def upload_class():
    body = request.get_data().decode('utf8')
    body = json.loads(body)
    className = body['className']
    body = body['base64Data']
    try:
        type = body.split(',')[0]
        data = body.split(',')[1]
        if type == 'data:application/pdf;base64':
            with open('./tmp/example.pdf', 'wb') as f:
                f.write(base64.b64decode(data))
                salt = ''.join(random.sample(string.ascii_letters + string.digits, 3))
                className = salt + '-' + className

                images = convert_from_path('./tmp/example.pdf', output_file="page", fmt="jpeg", thread_count=4)
                newClass = {
                    'className': className,
                    'pages': []
                }
                if not os.path.exists(os.path.abspath('./tmp/classes/%s' % className)):
                    os.mkdir(os.path.abspath('./tmp/classes/%s' % className))
                for index, image in enumerate(images):
                    print(index)
                    image = image.resize((700, 700), Image.ANTIALIAS)
                    print(image.size)

                    image.save('./tmp/classes/%s/%s.jpg' % (className, index), 'jpeg')
                    newClass['pages'].append({
                        'pageNotes': []
                    })

                print(newClass)
                client.socog.hwclass.insert_one(newClass)
                res = make_response(json.dumps({"ok": True, "data": {"className": className}}))
        else:
            res = make_response(json.dumps({"ok": False, "message": 'not a pdf file'}))
    except Exception as e:
        print(e)
        res = make_response(json.dumps({"ok": False, "message": e}))
    res.headers['access-control-allow-origin'] = '*'
    return res


@app.route("/get_class_list")
def get_class_list():
    try:
        cursor = client.socog.hwclass.find({}, {'className': 1})
        classes = []
        try:
            while True:
                classes.append(cursor.next()['className'])
        except Exception as e:
            # print(e)
            pass
        res = make_response(json.dumps({"ok": True, "data": classes}))
    except Exception as e:
        print(e)
        res = make_response(json.dumps({"ok": False, "message": e}))

    res.headers['access-control-allow-origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
