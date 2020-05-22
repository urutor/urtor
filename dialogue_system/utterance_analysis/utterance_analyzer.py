class UtteranceAnalyzer():
    """
    発話理解を扱うクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        pass # 何もしない

    def get_result(self, utterance):
        """
        理解結果を返すメソッド
        """
        return {'utt': ''} # 辞書型として返す

class UtteranceAnalyzerEcho(UtteranceAnalyzer):
    """
    入力を理解結果としてそのまま返すクラス
    """
    def get_result(self, utterance):
        """
        理解結果を返すメソッド
        """
        return {'utt': utterance} # 辞書型として返す

