from flask import Flask
from flask import render_template,redirect,request
from datetime import datetime
import gspread
from pprint import pprint
import json
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('sanix-flask-spreadsheet.json', scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1-DSJNKWYoV2k-UMD50wraPKkHU9kuP4lqDU0BJ1duTU'

app = Flask(__name__)

works = [
    'オーナー',
    '家賃集金・管理',
    '入居募集業務（対業者）',
    'クレーム対応・更新業務',
    '付帯商品販売（管理）',
    '各種工事手配',
    '自社所有',
    'サブリース',
    '現状回復工事',
    '設備不具合対応',
    'リフォーム・外壁塗装など',
    '建築・大規模改修など',
    '仲介店舗運営',
    '賃貸物件仲介（自社・他社）',
    '付帯商品販売（原則売切り）',
    '物件情報公開（賃貸）',
    '反響対応など（賃貸）',
    '売買物件仲介',
    '付帯商品販売（売買）',
    '物件情報公開（売買）',
    '反響営業など（売買）',
    '相続',
    '自社保証会社',
    'コインパーキング・コインランドリーなど'
]



@app.route('/')
def index():
    return render_template('index.html',works=works)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/<work>/update', methods=['GET','POST'])
def update(work):
    return render_template('/prj/update.html',work=work)


@app.route('/<work>/post', methods=['GET','POST'])
def post(work):

    #共有設定したtest-sheetを開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet(work)
    # 現在時刻
    dt_now = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    new_text = request.form.get('body')
    data = [dt_now, new_text]
    # ワークシートに書き込み
    worksheet.append_row(data)

    return redirect('/')



if __name__ == '__main__':
    app.run()