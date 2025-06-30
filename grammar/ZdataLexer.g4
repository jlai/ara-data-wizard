/*
 * Portions of this file are based on the ANTLR grammar for JavaScript
 * https://github.com/antlr/grammars-v4/blob/master/javascript/javascript/JavaScriptLexer.g4 The MIT
 * License (MIT)
 * 
 * Copyright (c) 2014 by Bart Kiers (original author) and Alexandre Vitorelli (contributor -> ported to CSharp)
 * Copyright (c) 2017-2020 by Ivan Kochurkin (Positive Technologies):
 *  added ECMAScript 6 support, cleared and transformed to the universal grammar.
 * Copyright (c) 2018 by Juan Alvarez (contributor -> ported to Go)
 * Copyright (c) 2019 by Student Main (contributor -> ES2020)
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

lexer grammar ZdataLexer;

OpenBracket: '[';
CloseBracket: ']';
OpenParen: '(';
CloseParen: ')';
OpenBrace: '{';
CloseBrace: '}';
SemiColon: ';';
Comma: ',';
Colon: ':';
Assign: '=';
Dot: '.';
BitOr: '|';
LessThan: '<';
MoreThan: '>';
Plus: '+';
Minus: '-';
BitNot: '~';
Not: '!';
Multiply: '*';
Divide: '/';

WhiteSpace: [ \t\r\n\u000C\u2028\u2029]+ -> channel(HIDDEN);
String: '"' (~ '"')* '"';
MultiLineComment: '/*' .*? '*/' -> channel(HIDDEN);
SingleLineComment:
	'//' ~[\r\n\u2028\u2029]* -> channel(HIDDEN);
DoubleBracketComment: '[[' .*? ']]' -> channel(HIDDEN);

// These should use predicates like PHP/BASH HEREDOCs, but hardcoded for now
RawString:
	'@"RXML(' [\u0000-\uFFFE]*? ')RXML"'
	| '@"MODS(' [\u0000-\uFFFE]*? ')MODS"'
	| '@"ATTR(' [\u0000-\uFFFE]*? ')ATTR"';

Integer: '-'? [0-9]+ ('i' | 'uu' | 'u8' | 'u' | 'i8')?;
Float:
	'-'? ([0-9]+ '.' [0-9]* | [0-9]* '.' [0-9]+) (
		'e' ('+' | '-') [0-9]+
	)? 'f'?;

EXPORT: 'export';
DEFAULT: 'default';
SCHEMA: 'schema';

Identifier: IdentifierStart IdentifierPart*;

fragment IdentifierPart:
	IdentifierStart
	| [\p{Mn}]
	| [\p{Nd}]
	| [\p{Pc}];

fragment IdentifierStart: [\p{L}] | [$_];
