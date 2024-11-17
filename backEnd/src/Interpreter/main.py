from Lexical import Lexical
from Grammar import Grammar
from Interpreter import Interpreter


def main():
    print("Lexical Analysis")
    lex = Lexical('backEnd/src/Test/Example/test1.txt')
    lex.printTokens()
    grm = Grammar(lex.getTokens())
    print(grm.getGrmTree().getStep())
    print(grm.getGrmTree().getVarName())
    print(grm.getGrmTree().getBranch())
    user1 = Interpreter(grm.getGrmTree())
    user1.dispatch()

if __name__ == "__main__":
    main()
