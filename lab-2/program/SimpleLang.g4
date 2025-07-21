grammar SimpleLang;

prog: stat+ EOF ;

stat: expr NEWLINE ;

expr
    : <assoc=right> expr '^' expr    # Power
    | expr '%' expr                  # Mod
    | expr op=('*'|'/') expr         # MulDiv
    | expr op=('+'|'-') expr         # AddSub
    | INT                             # Int
    | FLOAT                           # Float
    | STRING                          # String
    | BOOL                            # Bool
    | '(' expr ')'                    # Parens
    ;

INT    : [0-9]+ ;
FLOAT  : [0-9]+'.'[0-9]* ;
STRING : '"' (~["\r\n])* '"' ;
BOOL   : 'true' | 'false' ;
NEWLINE: '\r'? '\n' ;
WS     : [ \t]+ -> skip ;
COMMENT: '//' ~[\r\n]* -> skip ;
