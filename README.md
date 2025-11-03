apitest-3.pyの10行目｛｝の中の「"role": "user", "content": "ここ！！"」がプロンプトになっているので編集できます。また、7行目のmodel=...がモデル名になっているので...部分を編集できます。

実行環境は、windowsにWSL2をインストール、その後ubuntuをインストールし、次のようにコマンドを入力してください。
最後のコマンドを実行する前に、エクスプローラーの「"\\wsl.localhost\Ubuntu\home\**username**\apitest\apitest-3.py"」あたり（mkdirコマンドで作成したディレクトリ内）にapitest.pyを配置してください。

sudo apt update

sudo apt upgrade

sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.10

sudo apt install python3.10-venv

mkdir webtest

cd webtest

python3.10 -m venv venv

source venv/bin/activate

pip install yomitoku flask openai

pip install -U openai

python apitest-3.py


環境変数の設定
コントロールパネルから環境変数の設定を開き、WSLENVという環境変数を作成し、その値にWSLから使いたい環境変数名を入れる。（：で区切って複数入る）
環境変数名は"CHATGPT_API_KEY"
