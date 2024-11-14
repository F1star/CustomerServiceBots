class Lexical:
    # 词法分析器
    def __init__(self, fileName):
        self.fileName = fileName
        self.index = 0
        self.tokens = []
        self.parserFile()

    def parserFile(self):
        with open(self.fileName, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # 逐行读取
                line = line.strip()  # 去掉行首空白
                if line != '' and line[0] != '#':  # 跳过空行和注释行
                    self.parserLine(line)

    def parserLine(self, line):
        wordList = []
        words = line.split()
        for word in words:  # 分割单词
            if word[0] == '#':
                break
            wordList.append(word)
        self.tokens.append(wordList)

    def getTokens(self):
        return self.tokens

    def printTokens(self):
        for token in self.tokens:
            print(token)
