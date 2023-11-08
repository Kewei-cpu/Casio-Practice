import random


class Equation:
    op_priority = {"+": 1, "-": 1, "*": 2, "/": 3}
    op_latex = {"+": "+", "-": "-", "*": "\\times", "/": "\\div"}

    def __init__(self, father=None, position=0):
        self.left = None
        self.operator = None
        self.right = None

        self.father = father
        self.position = position

    def min_python_format(self):
        if self.father and self.op_priority[self.operator] < self.op_priority[self.father.operator]:
            return "(" + (self.left.min_python_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.operator + (
                       self.right.min_python_format() if isinstance(self.right, Equation) else str(self.right)) + ")"

        elif self.position == 1 and self.father.operator in ("/", "-") and self.operator in ("+", "-"):
            return "(" + (self.left.min_python_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.operator + (
                       self.right.min_python_format() if isinstance(self.right, Equation) else str(self.right)) + ")"

        else:
            return (self.left.min_python_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.operator + (
                       self.right.min_python_format() if isinstance(self.right, Equation) else str(self.right))

    def python_format(self):
        return "(" + (self.left.python_format() if isinstance(self.left, Equation) else str(self.left)) + \
               self.operator + (
                   self.right.python_format() if isinstance(self.right, Equation) else str(self.right)) + ")"

    def latex_frac_format(self):
        if self.operator == "/":
            return "\\frac{" + (
                self.left.latex_frac_format() if isinstance(self.left, Equation) else str(self.left)) + "}{" + \
                   (self.right.latex_frac_format() if isinstance(self.right, Equation) else str(self.right)) + "}"
        if self.father and self.father.operator == "/":
            return (self.left.latex_frac_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_frac_format() if isinstance(self.right, Equation) else str(self.right))
        elif self.father and self.op_priority[self.operator] < self.op_priority[
            self.father.operator]:
            return "(" + (self.left.latex_frac_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_frac_format() if isinstance(self.right, Equation) else str(self.right)) + ")"
        elif self.position == 1 and self.father.operator in ("/", "-") and self.operator in ("+", "-"):
            return "(" + (self.left.latex_frac_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_frac_format() if isinstance(self.right, Equation) else str(self.right)) + ")"
        else:
            return (self.left.latex_frac_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_frac_format() if isinstance(self.right, Equation) else str(self.right))

    def latex_format(self):
        if self.father and self.op_priority[self.operator] < self.op_priority[self.father.operator]:
            return "(" + (self.left.latex_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_format() if isinstance(self.right, Equation) else str(self.right)) + ")"
        elif self.position == 1 and self.father.operator in ("/", "-") and self.operator in ("+", "-"):
            return "(" + (self.left.latex_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_format() if isinstance(self.right, Equation) else str(self.right)) + ")"
        else:
            return (self.left.latex_format() if isinstance(self.left, Equation) else str(self.left)) + \
                   self.op_latex[self.operator] + (
                       self.right.latex_format() if isinstance(self.right, Equation) else str(self.right))

    def random_gen(self, depth=5, maxnum=100, float=True):  # length = depth + 2
        depth_left = random.randint(0, depth)
        depth_right = depth - depth_left

        if depth_left == 0:
            self.left = random.randint(1, maxnum) if not float else round(random.randint(1, maxnum) - random.random(),
                                                                          4)
        else:
            self.left = Equation(self, -1)
            self.left.random_gen(depth_left - 1, maxnum, float)

        if depth_right == 0:
            self.right = random.randint(1, maxnum) if not float else round(random.randint(1, maxnum) - random.random(),
                                                                           4)
        else:
            self.right = Equation(self, 1)
            self.right.random_gen(depth_right - 1, maxnum, float)

        self.operator = random.choice(["+", "*", "-", "/"])

    def random_gen_with_x(self, depth=5, maxnum=100, float=True, xrate=0.2, inputx=None):  # length = depth + 2
        if not inputx:
            x = random.randint(1, maxnum) if not float else round(random.randint(1, maxnum) - random.random(), 4)
        else:
            x = inputx

        depth_left = random.randint(0, depth)
        depth_right = depth - depth_left

        if depth_left == 0:
            self.left = (random.randint(1, maxnum) if not float else round(
                random.randint(1, maxnum) - random.random(), 4)) if random.random() > xrate else x
        else:
            self.left = Equation(self, -1)
            self.left.random_gen_with_x(depth_left - 1, maxnum, float, xrate, x)

        if depth_right == 0:
            self.right = (random.randint(1, maxnum) if not float else round(
                random.randint(1, maxnum) - random.random(), 4)) if random.random() > xrate else x
        else:
            self.right = Equation(self, 1)
            self.right.random_gen_with_x(depth_right - 1, maxnum, float, xrate, x)

        self.operator = random.choice(["+", "*", "-", "/"])
        return x


for i in range(10):
    a = Equation()
    x = a.random_gen_with_x(13, 100, True, 0.2)
    print("\section{}")
    try:
        print("$" + a.latex_frac_format().replace(str(x), " x ") + "=" + str(round(eval(a.min_python_format()), 4)) + "$")
        print(f"$$x={x}$$")
    except ZeroDivisionError:
        pass
