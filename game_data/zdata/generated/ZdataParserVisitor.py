from antlr4 import *
if "." in __name__:
    from .ZdataParser import ZdataParser
else:
    from ZdataParser import ZdataParser

# This class defines a complete generic visitor for a parse tree produced by ZdataParser.

class ZdataParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ZdataParser#program.
    def visitProgram(self, ctx:ZdataParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#statement.
    def visitStatement(self, ctx:ZdataParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#schemaStatement.
    def visitSchemaStatement(self, ctx:ZdataParser.SchemaStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#exportStatement.
    def visitExportStatement(self, ctx:ZdataParser.ExportStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:ZdataParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#literalExpression.
    def visitLiteralExpression(self, ctx:ZdataParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#variableAccessExpression.
    def visitVariableAccessExpression(self, ctx:ZdataParser.VariableAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#castExpression.
    def visitCastExpression(self, ctx:ZdataParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#groupingExpression.
    def visitGroupingExpression(self, ctx:ZdataParser.GroupingExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:ZdataParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:ZdataParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#unionExpression.
    def visitUnionExpression(self, ctx:ZdataParser.UnionExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#memberAccessExpression.
    def visitMemberAccessExpression(self, ctx:ZdataParser.MemberAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#indexingExpression.
    def visitIndexingExpression(self, ctx:ZdataParser.IndexingExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#functionCallExpression.
    def visitFunctionCallExpression(self, ctx:ZdataParser.FunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#expressionSequence.
    def visitExpressionSequence(self, ctx:ZdataParser.ExpressionSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#literal.
    def visitLiteral(self, ctx:ZdataParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#arrayLiteral.
    def visitArrayLiteral(self, ctx:ZdataParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#arrayItem.
    def visitArrayItem(self, ctx:ZdataParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#indexedPair.
    def visitIndexedPair(self, ctx:ZdataParser.IndexedPairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#defaultPair.
    def visitDefaultPair(self, ctx:ZdataParser.DefaultPairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZdataParser#keyedPair.
    def visitKeyedPair(self, ctx:ZdataParser.KeyedPairContext):
        return self.visitChildren(ctx)



del ZdataParser