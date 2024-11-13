from Lexical import Lexical

def main():
    print("Lexical Analysis")
    lex = Lexical('../Test/Example/test1.txt')
    lex.printTokens()

if __name__ == "__main__":
    main()