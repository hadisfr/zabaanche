#!/usr/bin/env python3


from random import randint


all_ops = ['-', '+']
all_vars = ["PhilipMortimer", "FrancisBlake", "Olrik", "AhmedNasir", "SarahSummertown"]


def get_random_var():
    return all_vars[randint(0, len(all_vars) - 1)]


def get_random_op():
    return all_ops[randint(0, len(all_ops) - 1)]


for var in all_vars:
    print("? %s" % var)

for i in range(10):
    for j in range(6):
        var = get_random_var()
        stmt = get_random_var()
        for k in range(randint(0, 10)):
            stmt += " " + get_random_op() + " " + get_random_var()
        print("%s = %s" % (var, stmt))
    for var in all_vars:
        print("! %s" % var)

print("run")

for var in all_vars:
    print(randint(0, 10))
