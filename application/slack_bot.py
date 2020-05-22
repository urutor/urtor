"""
Slack上で動作するbotプログラム
"""
from slackbot.bot import Bot # slackbotパッケージのBotクラスを使うためのロード

def main():
    bot = Bot() # Botを生成
    bot.run()   # Botを実行
 
if __name__ == "__main__":   # 本モジュールが主プログラムのときのみif以下を実行するためのif文
    main()

