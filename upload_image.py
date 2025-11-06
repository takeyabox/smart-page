from flask import Flask, render_template, request, url_for, redirect, session, stream_with_context
import os
import uuid
from openai import OpenAI
import json

from run_yomitoku import run_yomitoku

api_key_str = os.environ.get("CHATGPT_API_KEY")
if api_key_str is None:
    print("Error: CHATGPT_API_KEY environment variable not set")
else:
    print (f"your api key is <{api_key_str[:5]}.....>")

client = OpenAI(api_key=api_key_str)

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_PERMANENT'] = False

@app.route('/')
def index():
    if 'username' not in session:
        print("Guest not found")
        session['username'] = str(uuid.uuid4())
        print("user id has been assigned")
    else:
        print(f"Guest found. {session['username']}")

    session['visits'] = session.get('visits', 0) + 1
    print("redirecrt to upload")
    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        if 'username' not in session:
            return '不正なページ遷移'

        print("render upload.html")
        return render_template('upload.html')

    elif request.method == 'POST':
        print("received POST at upload.html")
        file = request.files['example']
        print("received files")
        session['src_image'] = os.path.join('./static/image', session['username']+file.filename)
        file.save(session['src_image'])
        print("saved files. redirect to uploaded_file.")
        return redirect(url_for('uploaded_file'))


@app.route('/uploaded_file', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'GET':
        if 'src_image' not in session:
            return '不正なページ遷移'

        print("render uploaded_file.html")
        return render_template('uploaded_file.html', filename=session['src_image'])
    elif request.method == 'POST':
        print("received POST at uploaded_file.html")
        session['tmp_dir'] = os.path.join('./static/image', session['username']+'_tmp')
        return app.response_class(stream_with_context(ocr_progress()))

def ocr_progress():
    yield "OCRを開始<br>"
    print("run OCR")
    run_yomitoku(src_image=session['src_image'], output_dir=session['tmp_dir'])
    print("OCR finished")
    yield  "完了<br>"
    next_url = url_for('show_ocr_result')
    yield F'<button onclick="window.location.href=\'{next_url}\';">結果を見る</button>'

@app.route('/show_ocr_result', methods=['GET', 'POST'])
def show_ocr_result():
    if request.method == 'GET':
        print("show OCR result")
        return render_template('show_ocr_result.html', ocr_image=session['tmp_dir']+'/ocr.jpg')
    elif request.method == 'POST':
        print("received POST at show_ocr_result.html")
        return redirect(url_for('generate_quiz'))

@app.route('/generate_quiz', methods=['GET', 'POST'])
def generate_quiz():
    if request.method == 'GET':
        print("render generate_quiz.html")
        json_path = os.path.join(session['tmp_dir'], 'ocr.md')
        with open(json_path, 'r', encoding='utf-8') as f:
            ocr_data = f.read()

        prompt = f"""あなたは高校生に向けて与えられた文章からいくつかの問題を作り出す優秀な教育アシスタントです。
以下の指示から指定の出力構造で結果を出力してください。


## 指示
- 以下の長文から理解度を図るための問題を出力構造のとおりに出力してください
- 問題は３つ作ってください。
- 各問題には、問題文、４つの選択肢（そのうち１つは正解）、正解、解説を設けてください
- 出力は必ずJSON形式とし、以下のキーと値の構造に従ってください
- explanationの値は引用を書かず、解説のみ書くこと


＜JSONの出力構造＞
{{ 
　"title": "（ここに問題のタイトル、例：長文読解問題）", 
　"questions": [
　　 {{ 
　　　"id": 1, 
　　　"question_text": "（ここに問題文）", 
　　　"options": [ "（選択肢1）", "（選択肢2）", "（選択肢3）", "（選択肢4）" ], 
　　　"correct_answer": "（ここに正しい答えのテキスト）", 
　　　"explanation": "（ここに解説）"
　　 }}, {{
　　　"id": 2,
　　　"question_text": "（ここに問題文）", 
　　　"options": [ "（選択肢1）", "（選択肢2）", "（選択肢3）", "（選択肢4）" ],
　　　"correct_answer": "（ここに正しい答えのテキスト）", 
　　　"explanation": "（ここに解説）"
　　 }}, {{ 
　　　"id": 3,
　　　"question_text": "（ここに問題文）", 
　　　"options": [ "（選択肢1）", "（選択肢2）", "（選択肢3）", "（選択肢4）" ], 
　　　"correct_answer": "（ここに正しい答えのテキスト）", 
　　　"explanation": "（ここに解説）" 
　　}}
　]
 }}


＜長文＞
{ocr_data}"""



        print("send prompt to OpenAI")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates quizzes."},
                {"role": "user", "content": prompt}
            ]
        )


        quiz = response.choices[0].message.content
        checkStringArray = ["{" ,"title", "questions", "id", "question_text", "options", "correct_answer", "explanation", "}"]
        for checkstring in checkStringArray:
            checkerrors = quiz.find(checkstring)
        if checkerrors == -1:
            print(f"Error: {checkstring} not found")

        delete_before = quiz.find("{")
        delete_after = quiz.rfind("}") + 1
        quiz = quiz[delete_before:delete_after]
        with open(session['tmp_dir'] + "/gpt.json", "w", encoding="utf-8") as file:
            file.write(quiz)
        print("received quiz from OpenAI")
        return render_template('generate_quiz.html', quiz=quiz)
    
    elif request.method == 'POST':
        print("received POST at generate_quiz.html")


        return  redirect(url_for('play_quiz'))


quiz_number = 0
@app.route('/play_quiz', methods=['GET','POST'])
def play_quiz():
    if request.method == 'GET':
        global quiz_number
        json_loaded = json.load(open(os.path.join(session['tmp_dir'], 'gpt.json'), 'r', encoding='utf-8'))
        print("render play_quiz.html")
        id = json_loaded["questions"][quiz_number]["id"]
        question_text = json_loaded["questions"][quiz_number]["question_text"]
        options = json_loaded["questions"][quiz_number]["options"]
        correct_answer = json_loaded["questions"][quiz_number]["correct_answer"]
        explanation = json_loaded["questions"][quiz_number]["explanation"]

        return render_template('play_quiz.html', id=id, question_text=question_text, options=options, correct_answer=correct_answer, explanation=explanation, quiz_number=quiz_number)
    elif request.method == 'POST':
        print("received POST at play_quiz.html")
        if quiz_number >= 2:
            quiz_number = 0
            return redirect(url_for('upload'))
        else:
            quiz_number += 1
            return redirect(url_for('play_quiz'))
    

if __name__ == '__main__':
    app.run(port=1313, debug=True)
    app.run(host='127.0.0.1', port=5000) # Replace 'your_ipv6_address'
