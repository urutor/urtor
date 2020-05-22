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

