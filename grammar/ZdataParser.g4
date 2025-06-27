parser grammar ZdataParser;

options {
	tokenVocab = ZdataLexer;
}

program: statement* EOF;

statement: (
		assignmentStatement
		| schemaStatement
		| exportStatement
		| // empty
	) ';';

schemaStatement: 'schema' Identifier;

exportStatement: 'export' assignmentStatement;

assignmentStatement:
	type = Identifier variableName = Identifier (
		'[' size = expression ']'
	)? '=' right = expression;

expression:
	literal													# literalExpression
	| expression ('.' Identifier)+							# memberAccessExpression
	| left = expression op = ('*' | '/') right = expression	# multiplicativeExpression
	| left = expression op = ('+' | '-') right = expression	# additiveExpression
	| left = expression '|' right = expression				# unionExpression
	| Identifier											# variableAccessExpression
	| '(' expression ')'									# groupingExpression
	| base = expression '[' index = expression ']'			# indexingExpression
	| expression '(' expressionSequence? ')' arrayLiteral?	# functionCallExpression;

expressionSequence: expression (',' expression)* ','?;

literal: arrayLiteral | String | RawString | Integer | Float;

arrayLiteral: '{' (arrayItem (',' arrayItem)*)? ','? '}';

arrayItem: expression | defaultPair | keyedPair | indexedPair;

indexedPair: '[' left = expression ']' '=' right = expression;

defaultPair: 'default' '=' expression;

keyedPair:
	'.' key = (Identifier | String) '=' value = expression;
