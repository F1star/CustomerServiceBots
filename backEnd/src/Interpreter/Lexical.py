import re

class Lexical:
    """
    词法分析器，解析文件中的内容为词法单元。
    """
    def __init__(self, fileName):
        """
        初始化，接收文件名并初始化相关变量。
        """
        self.fileName = fileName
        self.index = 0
        self.tokens = []  # 存储所有词法单元
        self.parserFile()  # 解析文件

    def parserFile(self):
        """
        逐行读取文件，跳过空行和注释行，解析有效内容。
        """
        with open(self.fileName, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()  # 去掉行首和行尾空白
                if line != '' and line[0] != '#':  # 跳过空行和注释行
                    self.parserLine(line)  # 解析每一行

    def parserLine(self, line):
        """
        使用正则表达式解析每一行，提取出词法单元。
        """
        wordList = []
        # 匹配双引号中的字符串或其他非空白单词
        pattern = r'\"[^\"]*\"|\S+'
        matches = re.findall(pattern, line)
        
        for word in matches:
            if word.startswith('#'):  # 如果是注释，停止解析
                break
            wordList.append(word)  # 添加有效单词
        
        self.tokens.append(wordList)  # 将词汇列表添加到tokens中

    def getTokens(self):
        """
        返回所有已解析的词法单元。
        """
        return self.tokens

    def printTokens(self):
        """
        打印所有的词法单元。
        """
        for token in self.tokens:
            print(token)

