# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,32,159,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,5,0,
        28,8,0,10,0,12,0,31,9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,39,8,1,1,1,1,
        1,1,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,55,8,4,1,4,
        1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,67,8,5,1,5,1,5,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,4,5,81,8,5,11,5,12,5,82,1,5,1,5,1,
        5,1,5,1,5,1,5,1,5,1,5,3,5,93,8,5,1,5,1,5,3,5,97,8,5,5,5,99,8,5,10,
        5,12,5,102,9,5,1,6,1,6,1,6,5,6,107,8,6,10,6,12,6,110,9,6,1,6,3,6,
        113,8,6,1,7,1,7,1,7,1,7,1,7,3,7,120,8,7,1,8,1,8,1,8,1,8,5,8,126,
        8,8,10,8,12,8,129,9,8,3,8,131,8,8,1,8,3,8,134,8,8,1,8,1,8,1,9,1,
        9,1,9,1,9,3,9,142,8,9,1,10,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,
        11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,0,1,10,13,0,2,4,6,8,10,12,
        14,16,18,20,22,24,0,3,1,0,19,20,1,0,15,16,2,0,22,22,32,32,173,0,
        29,1,0,0,0,2,38,1,0,0,0,4,42,1,0,0,0,6,45,1,0,0,0,8,48,1,0,0,0,10,
        66,1,0,0,0,12,103,1,0,0,0,14,119,1,0,0,0,16,121,1,0,0,0,18,141,1,
        0,0,0,20,143,1,0,0,0,22,149,1,0,0,0,24,153,1,0,0,0,26,28,3,2,1,0,
        27,26,1,0,0,0,28,31,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,32,1,
        0,0,0,31,29,1,0,0,0,32,33,5,0,0,1,33,1,1,0,0,0,34,39,3,8,4,0,35,
        39,3,4,2,0,36,39,3,6,3,0,37,39,1,0,0,0,38,34,1,0,0,0,38,35,1,0,0,
        0,38,36,1,0,0,0,38,37,1,0,0,0,39,40,1,0,0,0,40,41,5,7,0,0,41,3,1,
        0,0,0,42,43,5,31,0,0,43,44,5,32,0,0,44,5,1,0,0,0,45,46,5,29,0,0,
        46,47,3,8,4,0,47,7,1,0,0,0,48,49,5,32,0,0,49,54,5,32,0,0,50,51,5,
        1,0,0,51,52,3,10,5,0,52,53,5,2,0,0,53,55,1,0,0,0,54,50,1,0,0,0,54,
        55,1,0,0,0,55,56,1,0,0,0,56,57,5,10,0,0,57,58,3,10,5,0,58,9,1,0,
        0,0,59,60,6,5,-1,0,60,67,3,14,7,0,61,67,5,32,0,0,62,63,5,3,0,0,63,
        64,3,10,5,0,64,65,5,4,0,0,65,67,1,0,0,0,66,59,1,0,0,0,66,61,1,0,
        0,0,66,62,1,0,0,0,67,100,1,0,0,0,68,69,10,7,0,0,69,70,7,0,0,0,70,
        99,3,10,5,8,71,72,10,6,0,0,72,73,7,1,0,0,73,99,3,10,5,7,74,75,10,
        5,0,0,75,76,5,12,0,0,76,99,3,10,5,6,77,80,10,8,0,0,78,79,5,11,0,
        0,79,81,5,32,0,0,80,78,1,0,0,0,81,82,1,0,0,0,82,80,1,0,0,0,82,83,
        1,0,0,0,83,99,1,0,0,0,84,85,10,2,0,0,85,86,5,1,0,0,86,87,3,10,5,
        0,87,88,5,2,0,0,88,99,1,0,0,0,89,90,10,1,0,0,90,92,5,3,0,0,91,93,
        3,12,6,0,92,91,1,0,0,0,92,93,1,0,0,0,93,94,1,0,0,0,94,96,5,4,0,0,
        95,97,3,16,8,0,96,95,1,0,0,0,96,97,1,0,0,0,97,99,1,0,0,0,98,68,1,
        0,0,0,98,71,1,0,0,0,98,74,1,0,0,0,98,77,1,0,0,0,98,84,1,0,0,0,98,
        89,1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,11,
        1,0,0,0,102,100,1,0,0,0,103,108,3,10,5,0,104,105,5,8,0,0,105,107,
        3,10,5,0,106,104,1,0,0,0,107,110,1,0,0,0,108,106,1,0,0,0,108,109,
        1,0,0,0,109,112,1,0,0,0,110,108,1,0,0,0,111,113,5,8,0,0,112,111,
        1,0,0,0,112,113,1,0,0,0,113,13,1,0,0,0,114,120,3,16,8,0,115,120,
        5,22,0,0,116,120,5,26,0,0,117,120,5,27,0,0,118,120,5,28,0,0,119,
        114,1,0,0,0,119,115,1,0,0,0,119,116,1,0,0,0,119,117,1,0,0,0,119,
        118,1,0,0,0,120,15,1,0,0,0,121,130,5,5,0,0,122,127,3,18,9,0,123,
        124,5,8,0,0,124,126,3,18,9,0,125,123,1,0,0,0,126,129,1,0,0,0,127,
        125,1,0,0,0,127,128,1,0,0,0,128,131,1,0,0,0,129,127,1,0,0,0,130,
        122,1,0,0,0,130,131,1,0,0,0,131,133,1,0,0,0,132,134,5,8,0,0,133,
        132,1,0,0,0,133,134,1,0,0,0,134,135,1,0,0,0,135,136,5,6,0,0,136,
        17,1,0,0,0,137,142,3,10,5,0,138,142,3,22,11,0,139,142,3,24,12,0,
        140,142,3,20,10,0,141,137,1,0,0,0,141,138,1,0,0,0,141,139,1,0,0,
        0,141,140,1,0,0,0,142,19,1,0,0,0,143,144,5,1,0,0,144,145,3,10,5,
        0,145,146,5,2,0,0,146,147,5,10,0,0,147,148,3,10,5,0,148,21,1,0,0,
        0,149,150,5,30,0,0,150,151,5,10,0,0,151,152,3,10,5,0,152,23,1,0,
        0,0,153,154,5,11,0,0,154,155,7,2,0,0,155,156,5,10,0,0,156,157,3,
        10,5,0,157,25,1,0,0,0,16,29,38,54,66,82,92,96,98,100,108,112,119,
        127,130,133,141
    ]

class ZdataParser ( Parser ):

    grammarFileName = "ZdataParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'('", "')'", "'{'", "'}'", 
                     "';'", "','", "':'", "'='", "'.'", "'|'", "'<'", "'>'", 
                     "'+'", "'-'", "'~'", "'!'", "'*'", "'/'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'export'", 
                     "'default'", "'schema'" ]

    symbolicNames = [ "<INVALID>", "OpenBracket", "CloseBracket", "OpenParen", 
                      "CloseParen", "OpenBrace", "CloseBrace", "SemiColon", 
                      "Comma", "Colon", "Assign", "Dot", "BitOr", "LessThan", 
                      "MoreThan", "Plus", "Minus", "BitNot", "Not", "Multiply", 
                      "Divide", "WhiteSpace", "String", "MultiLineComment", 
                      "SingleLineComment", "DoubleBracketComment", "RawString", 
                      "Integer", "Float", "EXPORT", "DEFAULT", "SCHEMA", 
                      "Identifier" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_schemaStatement = 2
    RULE_exportStatement = 3
    RULE_assignmentStatement = 4
    RULE_expression = 5
    RULE_expressionSequence = 6
    RULE_literal = 7
    RULE_arrayLiteral = 8
    RULE_arrayItem = 9
    RULE_indexedPair = 10
    RULE_defaultPair = 11
    RULE_keyedPair = 12

    ruleNames =  [ "program", "statement", "schemaStatement", "exportStatement", 
                   "assignmentStatement", "expression", "expressionSequence", 
                   "literal", "arrayLiteral", "arrayItem", "indexedPair", 
                   "defaultPair", "keyedPair" ]

    EOF = Token.EOF
    OpenBracket=1
    CloseBracket=2
    OpenParen=3
    CloseParen=4
    OpenBrace=5
    CloseBrace=6
    SemiColon=7
    Comma=8
    Colon=9
    Assign=10
    Dot=11
    BitOr=12
    LessThan=13
    MoreThan=14
    Plus=15
    Minus=16
    BitNot=17
    Not=18
    Multiply=19
    Divide=20
    WhiteSpace=21
    String=22
    MultiLineComment=23
    SingleLineComment=24
    DoubleBracketComment=25
    RawString=26
    Integer=27
    Float=28
    EXPORT=29
    DEFAULT=30
    SCHEMA=31
    Identifier=32

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ZdataParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.StatementContext)
            else:
                return self.getTypedRuleContext(ZdataParser.StatementContext,i)


        def getRuleIndex(self):
            return ZdataParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = ZdataParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 6979321984) != 0):
                self.state = 26
                self.statement()
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
            self.match(ZdataParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SemiColon(self):
            return self.getToken(ZdataParser.SemiColon, 0)

        def assignmentStatement(self):
            return self.getTypedRuleContext(ZdataParser.AssignmentStatementContext,0)


        def schemaStatement(self):
            return self.getTypedRuleContext(ZdataParser.SchemaStatementContext,0)


        def exportStatement(self):
            return self.getTypedRuleContext(ZdataParser.ExportStatementContext,0)


        def getRuleIndex(self):
            return ZdataParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = ZdataParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32]:
                self.state = 34
                self.assignmentStatement()
                pass
            elif token in [31]:
                self.state = 35
                self.schemaStatement()
                pass
            elif token in [29]:
                self.state = 36
                self.exportStatement()
                pass
            elif token in [7]:
                pass
            else:
                raise NoViableAltException(self)

            self.state = 40
            self.match(ZdataParser.SemiColon)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SchemaStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SCHEMA(self):
            return self.getToken(ZdataParser.SCHEMA, 0)

        def Identifier(self):
            return self.getToken(ZdataParser.Identifier, 0)

        def getRuleIndex(self):
            return ZdataParser.RULE_schemaStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchemaStatement" ):
                return visitor.visitSchemaStatement(self)
            else:
                return visitor.visitChildren(self)




    def schemaStatement(self):

        localctx = ZdataParser.SchemaStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_schemaStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(ZdataParser.SCHEMA)
            self.state = 43
            self.match(ZdataParser.Identifier)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXPORT(self):
            return self.getToken(ZdataParser.EXPORT, 0)

        def assignmentStatement(self):
            return self.getTypedRuleContext(ZdataParser.AssignmentStatementContext,0)


        def getRuleIndex(self):
            return ZdataParser.RULE_exportStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportStatement" ):
                return visitor.visitExportStatement(self)
            else:
                return visitor.visitChildren(self)




    def exportStatement(self):

        localctx = ZdataParser.ExportStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_exportStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(ZdataParser.EXPORT)
            self.state = 46
            self.assignmentStatement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type_ = None # Token
            self.variableName = None # Token
            self.size = None # ExpressionContext
            self.right = None # ExpressionContext

        def Assign(self):
            return self.getToken(ZdataParser.Assign, 0)

        def Identifier(self, i:int=None):
            if i is None:
                return self.getTokens(ZdataParser.Identifier)
            else:
                return self.getToken(ZdataParser.Identifier, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)


        def OpenBracket(self):
            return self.getToken(ZdataParser.OpenBracket, 0)

        def CloseBracket(self):
            return self.getToken(ZdataParser.CloseBracket, 0)

        def getRuleIndex(self):
            return ZdataParser.RULE_assignmentStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentStatement" ):
                return visitor.visitAssignmentStatement(self)
            else:
                return visitor.visitChildren(self)




    def assignmentStatement(self):

        localctx = ZdataParser.AssignmentStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_assignmentStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            localctx.type_ = self.match(ZdataParser.Identifier)
            self.state = 49
            localctx.variableName = self.match(ZdataParser.Identifier)
            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 50
                self.match(ZdataParser.OpenBracket)
                self.state = 51
                localctx.size = self.expression(0)
                self.state = 52
                self.match(ZdataParser.CloseBracket)


            self.state = 56
            self.match(ZdataParser.Assign)
            self.state = 57
            localctx.right = self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ZdataParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class LiteralExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(ZdataParser.LiteralContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralExpression" ):
                return visitor.visitLiteralExpression(self)
            else:
                return visitor.visitChildren(self)


    class VariableAccessExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Identifier(self):
            return self.getToken(ZdataParser.Identifier, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableAccessExpression" ):
                return visitor.visitVariableAccessExpression(self)
            else:
                return visitor.visitChildren(self)


    class GroupingExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def OpenParen(self):
            return self.getToken(ZdataParser.OpenParen, 0)
        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)

        def CloseParen(self):
            return self.getToken(ZdataParser.CloseParen, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupingExpression" ):
                return visitor.visitGroupingExpression(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicativeExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.left = None # ExpressionContext
            self.op = None # Token
            self.right = None # ExpressionContext
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)

        def Multiply(self):
            return self.getToken(ZdataParser.Multiply, 0)
        def Divide(self):
            return self.getToken(ZdataParser.Divide, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpression" ):
                return visitor.visitMultiplicativeExpression(self)
            else:
                return visitor.visitChildren(self)


    class AdditiveExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.left = None # ExpressionContext
            self.op = None # Token
            self.right = None # ExpressionContext
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)

        def Plus(self):
            return self.getToken(ZdataParser.Plus, 0)
        def Minus(self):
            return self.getToken(ZdataParser.Minus, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpression" ):
                return visitor.visitAdditiveExpression(self)
            else:
                return visitor.visitChildren(self)


    class UnionExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.left = None # ExpressionContext
            self.right = None # ExpressionContext
            self.copyFrom(ctx)

        def BitOr(self):
            return self.getToken(ZdataParser.BitOr, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnionExpression" ):
                return visitor.visitUnionExpression(self)
            else:
                return visitor.visitChildren(self)


    class MemberAccessExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)

        def Dot(self, i:int=None):
            if i is None:
                return self.getTokens(ZdataParser.Dot)
            else:
                return self.getToken(ZdataParser.Dot, i)
        def Identifier(self, i:int=None):
            if i is None:
                return self.getTokens(ZdataParser.Identifier)
            else:
                return self.getToken(ZdataParser.Identifier, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberAccessExpression" ):
                return visitor.visitMemberAccessExpression(self)
            else:
                return visitor.visitChildren(self)


    class IndexingExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.base = None # ExpressionContext
            self.index = None # ExpressionContext
            self.copyFrom(ctx)

        def OpenBracket(self):
            return self.getToken(ZdataParser.OpenBracket, 0)
        def CloseBracket(self):
            return self.getToken(ZdataParser.CloseBracket, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexingExpression" ):
                return visitor.visitIndexingExpression(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ZdataParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)

        def OpenParen(self):
            return self.getToken(ZdataParser.OpenParen, 0)
        def CloseParen(self):
            return self.getToken(ZdataParser.CloseParen, 0)
        def expressionSequence(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionSequenceContext,0)

        def arrayLiteral(self):
            return self.getTypedRuleContext(ZdataParser.ArrayLiteralContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpression" ):
                return visitor.visitFunctionCallExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ZdataParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5, 22, 26, 27, 28]:
                localctx = ZdataParser.LiteralExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 60
                self.literal()
                pass
            elif token in [32]:
                localctx = ZdataParser.VariableAccessExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 61
                self.match(ZdataParser.Identifier)
                pass
            elif token in [3]:
                localctx = ZdataParser.GroupingExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 62
                self.match(ZdataParser.OpenParen)
                self.state = 63
                self.expression(0)
                self.state = 64
                self.match(ZdataParser.CloseParen)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 100
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 98
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        localctx = ZdataParser.MultiplicativeExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 68
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 69
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==19 or _la==20):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 70
                        localctx.right = self.expression(8)
                        pass

                    elif la_ == 2:
                        localctx = ZdataParser.AdditiveExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 71
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 72
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==15 or _la==16):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 73
                        localctx.right = self.expression(7)
                        pass

                    elif la_ == 3:
                        localctx = ZdataParser.UnionExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 74
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 75
                        self.match(ZdataParser.BitOr)
                        self.state = 76
                        localctx.right = self.expression(6)
                        pass

                    elif la_ == 4:
                        localctx = ZdataParser.MemberAccessExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 77
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 80 
                        self._errHandler.sync(self)
                        _alt = 1
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt == 1:
                                self.state = 78
                                self.match(ZdataParser.Dot)
                                self.state = 79
                                self.match(ZdataParser.Identifier)

                            else:
                                raise NoViableAltException(self)
                            self.state = 82 
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

                        pass

                    elif la_ == 5:
                        localctx = ZdataParser.IndexingExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        localctx.base = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 84
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 85
                        self.match(ZdataParser.OpenBracket)
                        self.state = 86
                        localctx.index = self.expression(0)
                        self.state = 87
                        self.match(ZdataParser.CloseBracket)
                        pass

                    elif la_ == 6:
                        localctx = ZdataParser.FunctionCallExpressionContext(self, ZdataParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 89
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 90
                        self.match(ZdataParser.OpenParen)
                        self.state = 92
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4768923688) != 0):
                            self.state = 91
                            self.expressionSequence()


                        self.state = 94
                        self.match(ZdataParser.CloseParen)
                        self.state = 96
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                        if la_ == 1:
                            self.state = 95
                            self.arrayLiteral()


                        pass

             
                self.state = 102
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpressionSequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(ZdataParser.Comma)
            else:
                return self.getToken(ZdataParser.Comma, i)

        def getRuleIndex(self):
            return ZdataParser.RULE_expressionSequence

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionSequence" ):
                return visitor.visitExpressionSequence(self)
            else:
                return visitor.visitChildren(self)




    def expressionSequence(self):

        localctx = ZdataParser.ExpressionSequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_expressionSequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.expression(0)
            self.state = 108
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 104
                    self.match(ZdataParser.Comma)
                    self.state = 105
                    self.expression(0) 
                self.state = 110
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 111
                self.match(ZdataParser.Comma)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arrayLiteral(self):
            return self.getTypedRuleContext(ZdataParser.ArrayLiteralContext,0)


        def String(self):
            return self.getToken(ZdataParser.String, 0)

        def RawString(self):
            return self.getToken(ZdataParser.RawString, 0)

        def Integer(self):
            return self.getToken(ZdataParser.Integer, 0)

        def Float(self):
            return self.getToken(ZdataParser.Float, 0)

        def getRuleIndex(self):
            return ZdataParser.RULE_literal

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = ZdataParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_literal)
        try:
            self.state = 119
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 114
                self.arrayLiteral()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 115
                self.match(ZdataParser.String)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 3)
                self.state = 116
                self.match(ZdataParser.RawString)
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 4)
                self.state = 117
                self.match(ZdataParser.Integer)
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 5)
                self.state = 118
                self.match(ZdataParser.Float)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OpenBrace(self):
            return self.getToken(ZdataParser.OpenBrace, 0)

        def CloseBrace(self):
            return self.getToken(ZdataParser.CloseBrace, 0)

        def arrayItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ArrayItemContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ArrayItemContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(ZdataParser.Comma)
            else:
                return self.getToken(ZdataParser.Comma, i)

        def getRuleIndex(self):
            return ZdataParser.RULE_arrayLiteral

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayLiteral" ):
                return visitor.visitArrayLiteral(self)
            else:
                return visitor.visitChildren(self)




    def arrayLiteral(self):

        localctx = ZdataParser.ArrayLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_arrayLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            self.match(ZdataParser.OpenBrace)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 5842667562) != 0):
                self.state = 122
                self.arrayItem()
                self.state = 127
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 123
                        self.match(ZdataParser.Comma)
                        self.state = 124
                        self.arrayItem() 
                    self.state = 129
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,12,self._ctx)



            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 132
                self.match(ZdataParser.Comma)


            self.state = 135
            self.match(ZdataParser.CloseBrace)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)


        def defaultPair(self):
            return self.getTypedRuleContext(ZdataParser.DefaultPairContext,0)


        def keyedPair(self):
            return self.getTypedRuleContext(ZdataParser.KeyedPairContext,0)


        def indexedPair(self):
            return self.getTypedRuleContext(ZdataParser.IndexedPairContext,0)


        def getRuleIndex(self):
            return ZdataParser.RULE_arrayItem

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayItem" ):
                return visitor.visitArrayItem(self)
            else:
                return visitor.visitChildren(self)




    def arrayItem(self):

        localctx = ZdataParser.ArrayItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_arrayItem)
        try:
            self.state = 141
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 5, 22, 26, 27, 28, 32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 137
                self.expression(0)
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 138
                self.defaultPair()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 139
                self.keyedPair()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 4)
                self.state = 140
                self.indexedPair()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IndexedPairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ExpressionContext
            self.right = None # ExpressionContext

        def OpenBracket(self):
            return self.getToken(ZdataParser.OpenBracket, 0)

        def CloseBracket(self):
            return self.getToken(ZdataParser.CloseBracket, 0)

        def Assign(self):
            return self.getToken(ZdataParser.Assign, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ZdataParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ZdataParser.ExpressionContext,i)


        def getRuleIndex(self):
            return ZdataParser.RULE_indexedPair

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexedPair" ):
                return visitor.visitIndexedPair(self)
            else:
                return visitor.visitChildren(self)




    def indexedPair(self):

        localctx = ZdataParser.IndexedPairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_indexedPair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(ZdataParser.OpenBracket)
            self.state = 144
            localctx.left = self.expression(0)
            self.state = 145
            self.match(ZdataParser.CloseBracket)
            self.state = 146
            self.match(ZdataParser.Assign)
            self.state = 147
            localctx.right = self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultPairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFAULT(self):
            return self.getToken(ZdataParser.DEFAULT, 0)

        def Assign(self):
            return self.getToken(ZdataParser.Assign, 0)

        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)


        def getRuleIndex(self):
            return ZdataParser.RULE_defaultPair

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultPair" ):
                return visitor.visitDefaultPair(self)
            else:
                return visitor.visitChildren(self)




    def defaultPair(self):

        localctx = ZdataParser.DefaultPairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_defaultPair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            self.match(ZdataParser.DEFAULT)
            self.state = 150
            self.match(ZdataParser.Assign)
            self.state = 151
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeyedPairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.key = None # Token
            self.value = None # ExpressionContext

        def Dot(self):
            return self.getToken(ZdataParser.Dot, 0)

        def Assign(self):
            return self.getToken(ZdataParser.Assign, 0)

        def expression(self):
            return self.getTypedRuleContext(ZdataParser.ExpressionContext,0)


        def Identifier(self):
            return self.getToken(ZdataParser.Identifier, 0)

        def String(self):
            return self.getToken(ZdataParser.String, 0)

        def getRuleIndex(self):
            return ZdataParser.RULE_keyedPair

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeyedPair" ):
                return visitor.visitKeyedPair(self)
            else:
                return visitor.visitChildren(self)




    def keyedPair(self):

        localctx = ZdataParser.KeyedPairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_keyedPair)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(ZdataParser.Dot)
            self.state = 154
            localctx.key = self._input.LT(1)
            _la = self._input.LA(1)
            if not(_la==22 or _la==32):
                localctx.key = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 155
            self.match(ZdataParser.Assign)
            self.state = 156
            localctx.value = self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[5] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 1)
         




