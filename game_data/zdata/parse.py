import os
import re
import sys
from typing import override
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from collections import OrderedDict
from .generated.ZdataLexer import ZdataLexer
from .generated.ZdataParser import ZdataParser
from .generated.ZdataParserVisitor import ZdataParserVisitor

"""
Expression to extract a string like @"MODS(stuff)MODS"
"""
HERE_STRING = re.compile(r'@"(?P<marker>[A-Za-z]+)\((?P<content>.*)\)(?P=marker)"')

NUMBER_SUFFIX = re.compile(r"(uu|u8|ul|i8|il|i|u)$")


class WrappedValue:
    def __init__(self, value, *, key=None, type=None):
        self.key = key
        self.value = value
        self.type = type
        self.num_errors = 0


def parse_int(s: str):
    return int(NUMBER_SUFFIX.sub("", s))


def parse_float(s: str):
    return float(s.removesuffix("f"))


class ParsedZdataFile:
    def __init__(self, *, exports: dict, schema: str):
        self.exports = exports
        self.schema = schema


class ZdataVisitor(ZdataParserVisitor):
    def __init__(self):
        super().__init__()
        self.variables = {}
        self.exports = OrderedDict()
        self.schema = None

    @override
    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        return ParsedZdataFile(exports=self.exports, schema=self.schema)

    @override
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    @override
    def visitSchemaStatement(self, ctx):
        self.schema = ctx.Identifier().getText()

    @override
    def visitExportStatement(self, ctx):
        wrapped_value = self.visit(ctx.assignmentStatement())
        self.exports[wrapped_value.key] = wrapped_value.value

    @override
    def visitAssignmentStatement(self, ctx):
        type_name = ctx.type_.text
        variable_name = ctx.variableName.text
        value = self.visit(ctx.right)

        if isinstance(value, dict):
            value.update({"_type": type_name})

        self.variables[variable_name] = value
        return WrappedValue(value, key=variable_name)

    @override
    def visitCastExpression(self, ctx):
        return self.visit(ctx.expression())

    @override
    def visitLiteralExpression(self, ctx):
        return self.visitChildren(ctx)

    @override
    def visitGroupingExpression(self, ctx):
        return self.visit(ctx.expression())

    @override
    def visitUnionExpression(self, ctx):
        items = []

        expressions = ctx.getTypedRuleContexts(ZdataParser.ExpressionContext)
        for expression in expressions:
            if isinstance(expression, ZdataParser.UnionExpressionContext):
                items.extend(self.visit(expression))
            else:
                items.append(self.visit(expression))

        return items

    @override
    def visitExpressionSequence(self, ctx):
        return self.visitChildren(ctx)

    @override
    def visitAdditiveExpression(self, ctx):
        op = ctx.op.text
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        if isinstance(left, int) and isinstance(right, int):
            if op == "+":
                return left + right
            else:
                return left - right

        return ctx.getText()

    @override
    def visitMultiplicativeExpression(self, ctx):
        op = ctx.op.text
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        if isinstance(left, int) and isinstance(right, int):
            if op == "*":
                return left * right
            else:
                return left / right

        return ctx.getText()

    @override
    def visitLiteral(self, ctx):
        if ctx.String():
            return ctx.String().getText().strip('"')
        elif ctx.Integer():
            return parse_int(ctx.Integer().getText())
        elif ctx.Float():
            return parse_float(ctx.Float().getText())
        elif ctx.RawString():
            return HERE_STRING.sub(r"\g<content>", ctx.RawString().getText())
        else:
            return self.visitChildren(ctx)

    @override
    def visitVariableAccessExpression(self, ctx):
        name = ctx.Identifier().getText()

        if name in self.variables:
            return self.variables[name]

        return self.visitChildren(ctx)

    @override
    def visitMemberAccessExpression(self, ctx):
        return ctx.getText()

    @override
    def visitArrayLiteral(self, ctx):
        items = []

        for child in ctx.getTypedRuleContexts(ZdataParser.ArrayItemContext):
            item = self.visit(child)
            items.append(item)

        if len(items) > 0 and all(
            isinstance(child, WrappedValue) and child.key for child in items
        ):
            return dict((entry.key, entry.value) for entry in items)
        else:
            return items

    @override
    def visitArrayItem(self, ctx):
        return self.visitChildren(ctx)

    @override
    def visitIndexedPair(self, ctx):
        key = ctx.left.getText()
        value = self.visit(ctx.right)

        return WrappedValue(value, key=key)

    @override
    def visitDefaultPair(self, ctx):
        value = self.visit(ctx.expression())
        return WrappedValue(value, key="default")

    @override
    def visitKeyedPair(self, ctx):
        key = (
            ctx.String().getText().strip('"')
            if ctx.String()
            else ctx.Identifier().getText()
        )
        value = self.visit(ctx.value)

        return WrappedValue(value, key=key)

    @override
    def visitFunctionCallExpression(self, ctx):
        name = ctx.expression().getText()

        args = []
        if ctx.expressionSequence():
            args.extend(
                self.visit(arg)
                for arg in ctx.expressionSequence().getTypedRuleContexts(
                    ZdataParser.ExpressionContext
                )
            )

        if ctx.arrayLiteral():
            args.append(self.visit(ctx.arrayLiteral()))

        match name:
            case "int" | "float":
                return args[0]
            case "int2" | "float2" | "uint2" | "uint4":
                return args

        return {
            "_type": "functionCall",
            "name": name,
            "args": args,
        }


class ParseErrorListener(ErrorListener):
    def __init__(self, filename="<string>"):
        super().__init__()
        self.filename = filename

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"file {self.filename} line {line}:{column:d} {msg}", file=sys.stderr)


def parse_zdata_stream(stream, filename=None) -> ParsedZdataFile:
    error_listener = ParseErrorListener(filename)

    lexer = ZdataLexer(stream, sys.stderr)
    stream = CommonTokenStream(lexer)
    parser = ZdataParser(stream, sys.stderr)

    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()
    output = ZdataVisitor().visit(tree)

    output.num_errors = parser.getNumberOfSyntaxErrors()

    return output


def parse_zdata_file(path) -> ParsedZdataFile:
    try:
        output = parse_zdata_stream(
            FileStream(path, encoding="utf-8"), filename=os.path.basename(path)
        )
    except Exception as e:
        raise Exception(f"error parsing file {path}") from e

    return output
