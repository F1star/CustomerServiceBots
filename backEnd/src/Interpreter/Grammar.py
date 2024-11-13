class Grammar:
    def __init__(self, tokens):
        self.tokens = tokens
        self.processTokens()

    def processTokens(self):
        for token in self.tokens:
            if token[0] == "Step":
                self.processStep(token)
            elif token[0] == "Speak":
                self.processSpeak(token)
            elif token[0] == "Expression":
                self.processExpression(token)
            elif token[0] == "Listen":
                self.processListen(token)
            elif token[0] == "Branch":
                self.processBranch(token)
            elif token[0] == "Silence":
                self.processSilence(token)
            elif token[0] == "Default":
                self.processDefault(token)
            elif token[0] == "Exit":
                self.processExit(token)
            else:
                print("Unknown token type:", token[0])
                break


    def processStep(self, token):
        pass

    def processSpeak(self, token):
        pass

    def processExpression(self, token):
        pass

    def processListen(self, token):
        pass

    def processBranch(self, token):
        pass

    def processSilence(self, token):
        pass

    def processDefault(self, token):
        pass

    def processExit(self, token):
        pass