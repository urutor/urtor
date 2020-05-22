"""
Terminal上で動作するbotプログラム
"""
import configparser                               # 設定ファイルの読み込みのためにロード
from dialogue_system.agent import Agent           # dialogue_systemパッケージのAgentクラスを利用するためにロード

def main():
    agent = Agent()                               # エージェントを生成
    bot = TerminalBot(agent)                      # ターミナル上のbotを生成
    bot.run()                                     # botを実行

class TerminalBot:
    """
    ターミナル上での対話を扱うクラス
    """
    def __init__(self, agent):
        """
        コンストラクタ
        """
        self.agent = agent                        # エージェントをセット
        self.cfg = self.__read_config()           # 設定情報をcfg属性にセット

    def __read_config(self):
        """
        設定ファイルを読み込むメソッド
        """
        cfg = configparser.ConfigParser()         # 設定ファイルを読み込むConfigParserを生成
        cfg.read('./bot_config.ini')              # 設定ファイルの読み込み
        return cfg['BOT']                         # 設定ファイル内の'BOT'セクションを返す

    def __get_start_signal(self, name='USER'):
        """
        開始判定と開始メッセージを返すメソッド
        """
        while True:
            utterance = self.__get_utterance(name) # ユーザからの発話を取得
            if utterance == 'start':               # 開始記号が入力されたらbreak
                break
        return self.agent.initial_message()        # 開始メッセージを返す

    def __get_utterance(self, name='USER'):
        """
        ユーザからの発話を取得するメソッド
        """
        utterance = input(name + ': ')            # ユーザからの発話を取得
        return utterance                          # 発話(utterance)を返す

    def __show_response(self, name, response):
        """
        エージェントからの応答を表示するメソッド
        """
        print (name + ': ' + response)            # エージェントからの応答を表示

    def run(self):
        """
        対話を実行するメソッド
        """
        state = self.agent.manager.internal_state.state              # 内部状態を参照
        init_message = self.__get_start_signal(self.cfg['UserName']) # 開始メッセージを取得
        self.__show_response(self.agent.name, init_message['utt'])   # 開始メッセージを表示
        self.agent.update_history('start', init_message['utt'], self.cfg['UserName']) # 発話と応答の履歴を更新

        while True:
            if state['turn']>self.cfg.getint('NumOfTurn'):         # ターン数が既定値より大きくなったら終了
                self.agent.write_history()                         # 対話履歴を書き出し
                break
            utterance = self.__get_utterance(self.cfg['UserName']) # ユーザからの発話を取得
            response = self.agent.get_response({'utt': utterance, 'turn': state['turn'], 'end': False}) # エージェントからの応答を取得
            self.__show_response(self.agent.name, response['utt']) # エージェントからの応答を表示
            self.agent.update_history(utterance, response['utt'], self.cfg['UserName']) # 発話と応答の履歴を更新

if __name__ == "__main__": # 本モジュールが主プログラムのときのみif以下を実行するためのif文
    main()

