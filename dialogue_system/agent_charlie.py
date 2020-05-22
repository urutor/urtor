"""
３種類のいずれかの方法で応答を返す対話エージェント(CHARLIE)プログラム
（エージェントBETAに、パターンに応じた応答を返す機能を追加）
"""
import random                                     # ランダムな取得のためにロード
import re                                         # 正規表現操作のためにロード
import numpy as np                                # 確率分布に従った取得のためにロード

def main():
    agent = Agent('CHARLIE')                      # エージェントを生成
    while True:
        utterance = get_utterance()               # ユーザからの発話を取得
        if utterance == '':                       # 改行のみの入力で終了
            agent.write_history()                 # 対話履歴を書き出し
            break
        response  = agent.get_response(utterance) # エージェントからの応答を取得
        show_response(agent.name, response)       # エージェントからの応答を表示
        agent.update_history(utterance, response) # 発話と応答の履歴を更新

def get_utterance(name='USER'):
    """
    ユーザからの発話を取得する
    """
    utterance = input(name + ': ')                # ユーザからの発話を取得
    return utterance                              # 発話(utterance)を返す

def show_response(name, response):
    """
    エージェントからの応答を表示する
    """
    print (name + ': ' + response)                # エージェントからの応答を表示

class Agent():
    """
    エージェントを扱うクラス
    """
    def __init__(self, name):
        self.name = name                                   # エージェントの名前をname属性に設定
        self.history = []                                  # 対話履歴を記録する リストをhistory属性に設定
        self.history_filename = './dialogue_management/reference/history.txt'            # 対話履歴を記録するファイル名をhistory_filename属性に設定
        self.reference = Reference(
            random = './dialogue_management/reference/random.txt',
            pattern = './dialogue_management/reference/pattern.txt',
        )                                                  # 参照データを扱うインスタンス(応答リストrandom.txt、パターン集pattern.txtを読み込み済みのインスタンス)を生成し、reference属性に設定
        self.responder = []                                # 応答を返すインスタンスを格納するためのリスト
        self.responder.append(PatternResponder('pattern', self.reference))      # パターンに応じた応答を返すPatternResponderを生成し、responder属性に追加
        self.responder.append(RandomResponder('random', self.reference.random)) # 応答リストからランダムに応答を返すRandomResponderを生成し、responder属性に追加
        self.responder.append(WhatResponder('what', None)) # 聞き返しの応答を返すWhatResponderを生成し、responder属性に追加

    def select_responder(self):
        """
        responderをランダムに選択するメソッド
        """
        return np.random.choice(self.responder, p=[0.8, 0.1, 0.1]) # 応答を返すインスタンスのリストから、pで指定された確率分布で(ここではself.responderの各要素が、[0.8, 0.1, 0.1]の確率として)一つの要素を選択

    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        responder = self.select_responder()          # responderをランダムに選択する
        response = responder.get_response(utterance) # responderから応答を取得する
        return response                              # 応答を返す

    def update_history(self, utterance, response, user='USER'):
        """
        対話履歴を更新するメソッド
        """
        self.history.append(                         # 対話履歴(self.history)に、発話と応答のタプルを追加
            ('{}: {}'.format(user, utterance),       # ユーザ名と発話の文字列
             '{}: {}'.format(self.name, response))   # エージェント名と応答の文字列
        )

    def write_history(self):
        """
        対話履歴を書き出すメソッド
        """
        with open(self.history_filename, 'w') as f:  # 書き出し専用ファイルとしてオープン
            f.write(''.join(map(lambda x:x[0]+'\n'+x[1]+'\n', self.history))) # 対話履歴の各要素(タプル)の0番目と1番目の要素に改行をつけて連結した文字列のリストについて、各要素を連結したものを書き出す

class Reference():
    """
    参照データを扱うクラス
    """
    def __init__(self, random, pattern):
        """
        コンストラクタ
        """
        self.random  = self.read_sample_responses(random) # 応答リスト(random)を読み込み、random属性に設定
        self.pattern = self.read_sample_pattern(pattern)  # パターン集(pattern)を読み込み、pattern属性に設定

    def read_sample_pattern(self, sample_file):
        """
        パターン集(sample_file)を読み込むメソッド
        """
        pattern = []                                      # パターン集を格納するリストを用意
        with open(sample_file, 'r') as f:                 # 読み込み専用ファイルとしてオープン
            for l in f.read().splitlines():               # 全体を読み込み、改行で分割したリストの各要素について繰り返し
                pat, *phrases = l.split()                 # 各行を空白(タブ含む)で分割した結果を左からpat, phrasesにそれぞれ取得
                if pat=='' or len(phrases)==0:            # patが長さ0の文字列、あるいは、phrases(リスト)の要素数が0ならば、次の繰り返しへ
                    continue
                pattern.append((pat, phrases[0]))         # patとphrases[0]のタプルをpattern(リスト)に追加
        return sorted(pattern, key=lambda x:len(x[0]), reverse=True) # patternの各要素(タプル)について、タプルの0番目の要素(文字列)の長さの降順にソートした結果を返す

    def read_sample_responses(self, sample_file):
        """
        応答リスト(sample_file)を読み込むメソッド
        """
        with open(sample_file, 'r') as f:         # 読み込み専用ファイルとしてオープン
            return f.read().splitlines()          # 全体を読み込み、改行で分割したものをリストとして返す

class Responder():
    """
    応答を扱うクラス
    """
    def __init__(self, name, reference):
        """
        コンストラクタ
        """
        self.name = name                          # 応答クラスの名前を設定
        self.reference = reference                # 聞き返しの応答を返す

    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        return ''

class PatternResponder(Responder):
    """
    パターンに応じて応答を返す応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        for item in self.reference.pattern:              # 参照データ(self.reference)のパターン属性(pattern)の各要素itemについて繰り返し
            m = re.search(item[0], utterance)            # 各要素の0番目の内容(item[0], すなわちパターン)が発話に含まれているかどうかを順に検索
            if m:                                        # もし最初の検索結果が存在すれば
                return random.choice(item[1].split('|')) # その要素の1番目の内容(item[1], すなわちパターンに応じた応答集)を'|'で分割しリストとしたものから、ランダムに要素を一つ選択し、返す
        return random.choice(self.reference.random)      # もし全要素について検索に該当する結果がなければ、randomモジュールのchoice関数で応答リスト(self.reference.random)からランダムに応答を取得し、返す

class RandomResponder(Responder):
    """
    応答リストからランダムに応答を返す応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        return random.choice(self.reference)      # randomモジュールのchoice関数で応答リスト(self.reference)からランダムに応答を取得し、返す

class WhatResponder(Responder):
    """
    聞き返ししかしない応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        return utterance + 'って何？'             # 聞き返しの応答を返す

if __name__ == '__main__': # 本モジュールが主プログラムのときのみif以下を実行するためのif文
    main()

