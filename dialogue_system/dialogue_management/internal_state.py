import pprint          # 内部状態を文字列としてきれいに出力するためにロード

class InternalState():
    """
    エージェントの内部状態を扱うクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.state = {'utt': None, 'turn': None, 'topic': None, 'mode': None, 'end': False} # 内部状態を辞書型で格納。topicやmodeはあくまで例として示している。例えば、対話の話題についてはtopicを用いることが考えられる

    def init_turn(self):
        """
        ターン数を初期化するメソッド
        """
        self.state['turn'] = 1   # ターン数を1で初期化する

    def increment_turn(self):
        """
        ターン数をインクリメントするメソッド
        """
        self.state['turn'] += 1  # ターン数をインクリメントする

    def update(self, analysis_result):
        """
        内部状態を更新するメソッド
        """
        for k in analysis_result:              # analysis_resultの各項目で
            self.state[k] = analysis_result[k] # 内部状態の該当項目を上書き更新する

    def has(self, name):
        """
        与えられた属性が内部状態に存在するかどうかを確認するメソッド
        """
        return self.state.get(name, None) != None # nameで与えられた属性が内部状態に存在するかどうかを返す

    def clear(self):
        """
        内部状態をクリアするメソッド
        """
        self.__init__() # 内部状態を初期状態(コンストラクタがかかった直後の状態)に戻す

    def __str__(self):
        """
        内部状態を文字列型として返すメソッド
        """
        return pprint.pformat(self.state) # 内部状態をpprintできれいに出力する

