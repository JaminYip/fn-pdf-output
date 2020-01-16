# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response
from flask_api import status
from urllib.parse import urlparse
import datetime
import os
import pdf_output
import random
import redis
import string
import sys
import traceback
import urllib

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Redisに接続する
r = redis.Redis(host='localhost', port=6379, db=0)


# pdfのurlを取得する
@app.route('/', methods=['GET'])
def get_pdf_url():
    pdf_filename = ''
    # noinspection PyBroadException
    try:
        pdf_filename = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f') + '.pdf'
        pdf_output.create_pdf(pdf_filename)

        # pdfをredisに一時保存する
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=60))
        r.rpush(
            key,
            pdf_filename,
            open('./' + pdf_filename, "rb").read()
        )
        r.expire(key, 180)

        # pdfのurlを返す
        return '{uri.scheme}://{uri.netloc}/pdf/'.format(uri=urlparse(request.url)) + key, status.HTTP_200_OK
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return jsonify(res='Internal Server Error'), status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        if os.path.isfile('./' + pdf_filename):
            os.remove('./' + pdf_filename)


# pdfを取得する
@app.route('/pdf/<string:key>', methods=['GET'])
def get_pdf(key):
    # noinspection PyBroadException
    try:
        # 一時保存されたpdfを取得する
        if r.exists(key) == 1:
            data = r.lrange(key, 0, 1)
        else:
            return jsonify(res='Not Found'), status.HTTP_404_NOT_FOUND

        # pdfを返す
        response = make_response()
        pdf_filename = str(data[0].decode())
        pdf_filename = urllib.parse.quote(pdf_filename)
        response.data = data[1]
        # response.headers['Content-Disposition'] = 'attachment;' # ダウンロード
        response.headers['Content-Disposition'] = 'inline;'  # ブラウザに表示
        response.headers['Content-Disposition'] = "filename='{}'; filename*=UTF-8''{}".format(pdf_filename, pdf_filename)
        response.content_type = 'application/pdf'

        return response, status.HTTP_200_OK
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return jsonify(res='Internal Server Error'), status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run()
