from FormulaTree import AbstractArgument, Formula, AtomicArgument


def toJava(tree: AbstractArgument) -> str:
    if isinstance((arg := tree), AtomicArgument):
        return arg.value
    elif isinstance((formula := tree), Formula):
        # int
        if formula.function_name in ["+", "-", "*"]:
            return simpleBracketJoin(formula)
        # bool
        elif formula.function_name == "not":
            return bool_not(formula)
        elif formula.function_name == "and":
            return bool_and(formula)
        elif formula.function_name == "or":
            return bool_or(formula)
        elif formula.function_name == "->":
            return bool_impl(formula)
        # comparing ints
        elif formula.function_name in ["<", ">", "<=", ">=", "="]:
            return simple_inline(formula)
        # general
        elif formula.function_name == "ite":
            return ternaryOperator(formula)
        # array
        elif formula.function_name == "seq.unit":
            return seq_unit(formula)
        elif formula.function_name == "seq.++":
            return seq_concat(formula)
        elif formula.function_name == "str.len":
            return seq_len(formula)
        elif formula.function_name == "seq.nth":
            return seq_nth(formula)
        elif formula.function_name == "seq.at":
            return seq_at(formula)
        elif formula.function_name == "seqUpdate":
            return seq_update(formula)


def simpleBracketJoin(formula: Formula) -> str:
    return formula.function_name.join([f"({toJava(arg)})" for arg in formula.arguments])


def ternaryOperator(formula: Formula) -> str:
    return "({0}) ? ({1}) ! ({2})".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
        {toJava(formula.arguments[2])},
    )


def bool_not(formula: Formula) -> str:
    return "!({0})".format(
        {toJava(formula.arguments[0])},
    )


def bool_and(formula: Formula) -> str:
    return "({0}) && ({1})".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
    )


def bool_or(formula: Formula) -> str:
    return "({0}) || ({1})".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
    )


def bool_impl(formula: Formula) -> str:
    return "!({0}) || ({1})".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
    )


def simple_inline(formula: Formula) -> str:
    return "({0}) {1} ({2})".format(
        {toJava(formula.arguments[0])},
        {formula.function_name},
        {toJava(formula.arguments[1])},
    )


def seq_nth(formula: Formula) -> str:
    return "({0})[{1}]".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
    )


def seq_at(formula: Formula) -> str:
    return "new int[]{{({0})[{1}]}}".format(
        {toJava(formula.arguments[0])},
        {toJava(formula.arguments[1])},
    )


def seq_len(formula: Formula) -> str:
    return "({0}).length".format(
        {toJava(formula.arguments[0])},
    )


def seq_concat(formula: Formula) -> str:
    return (
        "ArrayUtils.addAll("
        + ", ".join([toJava(arg) for arg in formula.arguments])
        + ")"
    )


def seq_unit(formula: Formula) -> str:
    return "new int[]{{{1}}}".format(
        {toJava(formula.arguments[0])},
    )


def seq_update(formula: Formula) -> str:
    return "ArrayUtils.addAll(ArrayUtils.subarray({0}, 0, {1}), new int[]{{{2}}},ArrayUtils.subarray({0}, ({1})+1, ({0}).length))".format(
        toJava(formula.arguments[0]),
        toJava(formula.arguments[1]),
        toJava(formula.arguments[2]),
    )
