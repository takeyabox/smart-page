from flask import Flask, render_template, request, url_for, redirect, session, stream_with_context
import os
import uuid

from run_yomitoku import run_yomitoku

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_PERMANENT'] = False

@app.route('/')
def index():
    if 'username' not in session:
        print("Guest not found")
        session['username'] = str(uuid.uuid4())
    else:
        print(f"Guest found. {session['username']}")

    session['visits'] = session.get('visits', 0) + 1

    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        if 'username' not in session:
            return '不正なページ遷移'

        return render_template('upload.html')

    elif request.method == 'POST':
        file = request.files['example']
        session['src_image'] = os.path.join('./static/image', session['username']+file.filename)
        file.save(session['src_image'])
        return redirect(url_for('uploaded_file'))


@app.route('/uploaded_file', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'GET':
        if 'src_image' not in session:
            return '不正なページ遷移'

        return render_template('uploaded_file.html', filename=session['src_image'])
    elif request.method == 'POST':
        session['tmp_dir'] = os.path.join('./static/image', session['username']+'_tmp')
        return app.response_class(stream_with_context(ocr_progress()))

def ocr_progress():
    yield "OCRを開始<br>"
    run_yomitoku(src_image=session['src_image'], output_dir=session['tmp_dir'])
    yield  "完了<br>"
    next_url = url_for('show_ocr_result')
    yield F'<button onclick="window.location.href=\'{next_url}\';">結果を見る</button>'

@app.route('/show_ocr_result')
def show_ocr_result():
    return render_template('show_ocr_result.html', ocr_image=session['tmp_dir']+'/ocr.jpg')

if __name__ == '__main__':
    # app.run(port=1313, debug=True)
    app.run(host='2405:6581:3e00:2a00:e356:d162:96e7:b323', port=5000) # Replace 'your_ipv6_address'
