#!/usr/bin/env python3

from sys import stdin
from functools import reduce
from enum import Enum
from collections import defaultdict


class ExprType(Enum):
    PRINT = 0
    INPUT = 1
    ASSIGNMENT = 2


def is_valid_id(string):
    return len(string) and reduce(
        lambda x, y: x and y,
        [("a" <= letter <= "z") or ("A" <= letter <= "Z") or ("0" <= letter <= "9") for letter in string],
    ) and not ("0" <= string[0] <= "9")


def is_valid_const(string):
    return len(string) and reduce(
        lambda x, y: x and y,
        [("0" <= letter <= "9") for letter in string],
    )


def is_valid_operator(string):
    return string in ["+", "-"]


def is_valid_operand(string):
    return is_valid_id(string) or is_valid_const(string)


def is_valid_statement(stmt):
    return len(stmt) and (len(stmt) % 2) and is_valid_operand(stmt[0]) and reduce(
        lambda x, y: x and y,
        [is_valid_operator(stmt[2 * i + 1]) and is_valid_operand(stmt[2 * i + 2]) for i in range(len(stmt) // 2)],
        True,
    )


def eval_operand(operand, vals):
    return int(operand) if is_valid_const(operand) else vals[operand] if is_valid_id(operand) else None


def eval_stmt(stmt, vals):
    ret = eval_operand(stmt[0], vals)
    for i in range(len(stmt) // 2):
        ret = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
        }[stmt[2 * i + 1]](ret, eval_operand(stmt[2 * i + 2], vals))
    return ret


def run_print(expr, vals):
    print(vals[expr[1]])


def run_input(expr, vals, user_input):
    vals[expr[1]] = user_input.pop()


def run_assignment(expr, vals):
    vals[expr[1]] = eval_stmt(expr[2], vals)


def run(program, user_input):
    vals = defaultdict(int)
    for expr in program:
        # print(expr, vals)
        if expr[0] == ExprType.PRINT:
            run_print(expr, vals)
        elif expr[0] == ExprType.INPUT:
            run_input(expr, vals, user_input)
        elif expr[0] == ExprType.ASSIGNMENT:
            run_assignment(expr, vals)


def parse_print(line):
    if len(line) != 2 or line[0] != "!" or not is_valid_id(line[1]):
        raise ValueError
    return ExprType.PRINT, line[1]


def parse_input(line):
    if len(line) != 2 or line[0] != "?" or not is_valid_id(line[1]):
        raise ValueError
    return ExprType.INPUT, line[1]


def parse_assignment(line):
    if len(line) <= 2 or line[1] != "=" or not is_valid_id(line[0]):
        raise ValueError
    stmt = line[2:]
    if not is_valid_statement(stmt):
        raise ValueError
    return ExprType.ASSIGNMENT, line[0], stmt


def parse_line(line):
    if len(line) >= 1 and line[0] == "!":
        return parse_print(line)
    elif len(line) >= 1 and line[0] == "?":
        return parse_input(line)
    elif len(line) >= 2 and is_valid_id(line[0]) and line[1] == "=":
        return parse_assignment(line)
    else:
        raise ValueError()


def parse_program(program):
    res = []
    for i in range(len(program)):
        try:
            line = program[i]
            if len(line):
                res.append(parse_line(line))
        except ValueError:
            # print(program[i])
            raise ValueError({'line': i + 1})
    return res


def tokenize_line_by_delim(line, delim):
    res = reduce(
        lambda x, y: x + y,
        [("\n" + delim + "\n").join(map(lambda x: x.strip(), part.split(delim))).split("\n") for part in line],
        [],
    )
    res = [token for token in res if token]
    return res


def tokenize_line(line):
    line = [line]
    for delim in "!?=+-":
        line = tokenize_line_by_delim(line, delim)
    return line


def tokenize(program):
    if type(program) == list:
        return [tokenize(line) for line in program]
    else:
        return tokenize_line(program)


def get_input(input_stream=stdin):
    lines = [line.strip() for line in input_stream]
    try:
        run_index = lines.index("run")
    except ValueError:
        return lines, None
    program = lines[:run_index]
    user_input = lines[run_index + 1:] if run_index < len(lines) else []
    return program, user_input


def main():
    program, user_input = get_input(stdin)
    if user_input is None:
        exit()
    program = tokenize(program)
    try:
        program = parse_program(program)
    except ValueError as e:
        print("Syntax error at line %d" % e.args[0]['line'])
        exit()
    user_input = [int(val) for val in user_input]
    user_input.reverse()
    # print(program, list(reversed(user_input)))
    try:
        run(program, user_input)
    except IndexError:
        print("Unexpected end of input")


if __name__ == '__main__':
    main()
