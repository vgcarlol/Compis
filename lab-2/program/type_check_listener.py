from SimpleLangListener import SimpleLangListener
from SimpleLangParser   import SimpleLangParser
from custom_types       import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):
    def __init__(self):
        self.errors = []
        self.types  = {}   # ctx -> Type

    # MulDiv
    def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        if not (isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType))):
            self.errors.append(f"Unsupported operand types for * or /: {lt} and {rt}")
            self.types[ctx] = IntType()
        else:
            self.types[ctx] = FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()

    # AddSub
    def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        op = ctx.op.text
        # ❌ Prohibimos operar con booleanos
        if isinstance(lt, BoolType) or isinstance(rt, BoolType):
            self.errors.append(f"Cannot use '{op}' with booleans: {lt} and {rt}")
            self.types[ctx] = IntType()
        # numérico
        elif isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
            self.types[ctx] = FloatType() if isinstance(lt, FloatType) or isinstance(rt, FloatType) else IntType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {lt} and {rt}")
            self.types[ctx] = IntType()

    # Literales
    def exitInt(self, ctx: SimpleLangParser.IntContext):
        self.types[ctx] = IntType()
    def exitFloat(self, ctx: SimpleLangParser.FloatContext):
        self.types[ctx] = FloatType()
    def exitString(self, ctx: SimpleLangParser.StringContext):
        self.types[ctx] = StringType()
    def exitBool(self, ctx: SimpleLangParser.BoolContext):
        self.types[ctx] = BoolType()
    def exitParens(self, ctx: SimpleLangParser.ParensContext):
        self.types[ctx] = self.types[ctx.expr()]

    # Power
    def exitPower(self, ctx: SimpleLangParser.PowerContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        if isinstance(lt, IntType) and isinstance(rt, IntType):
            self.types[ctx] = IntType()
        elif isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
            self.types[ctx] = FloatType()
        else:
            self.errors.append(f"Unsupported types for ^: {lt} and {rt}")
            self.types[ctx] = IntType()

    # Mod
    def exitMod(self, ctx: SimpleLangParser.ModContext):
        lt = self.types[ctx.expr(0)]
        rt = self.types[ctx.expr(1)]
        if isinstance(lt, IntType) and isinstance(rt, IntType):
            self.types[ctx] = IntType()
        else:
            self.errors.append(f"Unsupported types for %: {lt} and {rt}")
            self.types[ctx] = IntType()
