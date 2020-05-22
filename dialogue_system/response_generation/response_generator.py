class ResponseGenerator():
    """
    応答生成を扱うクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def get_response(self, system_action):
        """
        応答生成結果を返すメソッド
        """
        return {'utt': '', 'end': False} # 辞書型として返す

class ResponseGeneratorEcho(ResponseGenerator):
    """
    選択した行動内の発話をそのまま応答結果として返すクラス
    """
    def get_response(self, system_action):
        """
        選択した行動内の発話をそのまま応答結果として返すメソッド
        """
        return system_action # 辞書型として返す

