import ply.lex as lex
import ply.yacc as yacc

# ---------------------- Lexer ----------------------
tokens = ('A', 'B', 'NL')

t_A = r'[aA]'
t_B = r'[bB]'
t_NL = r'\n'
t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------------------- Parser ----------------------
error_occurred = False

def p_stmt(p):
    'stmt : S NL'
    if not error_occurred:
        print("valid string")

def p_S_rec(p):
    'S : A S B'
    pass

def p_S_empty(p):
    'S : '
    pass

def p_error(p):
    global error_occurred
    error_occurred = True
    print("invalid string")

parser = yacc.yacc()

# ---------------------- Main ----------------------
if __name__ == '__main__':
    print("Enter the string (end it with Enter key):")
    error_occurred = False
    user_input = input() + "\n"
    parser.parse(user_input)
