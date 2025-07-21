# type_check_visitor.py

print("[DEBUG MODULE] Loaded type_check_visitor.py")  # Verás esto al importar el módulo

from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

    # Punto de entrada: visitProg
    def visitProg(self, ctx: SimpleLangParser.ProgContext):
        print("[DEBUG] visitProg")
        return self.visitChildren(ctx)

    # MulDiv: * y /
    def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        print(f"[DEBUG] visitMulDiv: {lt} *|/ {rt}")
        if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
            return FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()
        raise TypeError(f"Unsupported operand types for * or /: {lt} and {rt}")

    # AddSub: + y -, prohibimos booleanos
    def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        op = ctx.op.text
        print(f"[DEBUG] visitAddSub: {lt} {op} {rt}")
        if isinstance(lt, BoolType) or isinstance(rt, BoolType):
            raise TypeError(f"Cannot use '{op}' with booleans: {lt}, {rt}")
        if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
            return FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()
        raise TypeError(f"Unsupported operand types for {op}: {lt} and {rt}")

    # Literales
    def visitInt(self, ctx: SimpleLangParser.IntContext):
        print(f"[DEBUG] visitInt")
        return IntType()
    def visitFloat(self, ctx: SimpleLangParser.FloatContext):
        print(f"[DEBUG] visitFloat")
        return FloatType()
    def visitString(self, ctx: SimpleLangParser.StringContext):
        print(f"[DEBUG] visitString")
        return StringType()
    def visitBool(self, ctx: SimpleLangParser.BoolContext):
        print(f"[DEBUG] visitBool")
        return BoolType()
    def visitParens(self, ctx: SimpleLangParser.ParensContext):
        print(f"[DEBUG] visitParens")
        return self.visit(ctx.expr())

    # Power: ^
    def visitPower(self, ctx: SimpleLangParser.PowerContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        print(f"[DEBUG] visitPower: {lt} ^ {rt}")
        if isinstance(lt, IntType) and isinstance(rt, IntType):
            return IntType()
        if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
            return FloatType()
        raise TypeError(f"Unsupported types for '^': {lt} and {rt}")

    # Mod: %
    def visitMod(self, ctx: SimpleLangParser.ModContext):
        lt = self.visit(ctx.expr(0))
        rt = self.visit(ctx.expr(1))
        print(f"[DEBUG] visitMod: {lt} % {rt}")
        if isinstance(lt, IntType) and isinstance(rt, IntType):
            return IntType()
        raise TypeError(f"Unsupported types for '%': {lt} and {rt}")
