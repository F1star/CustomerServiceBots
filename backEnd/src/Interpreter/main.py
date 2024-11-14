from Lexical import Lexical
from Grammar import Grammar


def main():
    print("Lexical Analysis")
    lex = Lexical('../Test/Example/test1.txt')
    lex.printTokens()
    grm = Grammar(lex.getTokens())
    print(grm.getGrmTree().getStep())
    print(grm.getGrmTree().getVarName())
    print(grm.getGrmTree().getBranch())


if __name__ == "__main__":
    main()
