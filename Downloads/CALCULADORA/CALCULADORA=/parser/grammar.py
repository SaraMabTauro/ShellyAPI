# import re

# def evaluate_expression(expression):
#     # Validar expresión para evitar inyecciones
#     if not re.match(r'^[0-9+\-*/.() ]+$', expression):
#         raise ValueError("Expresión inválida")
#     return eval(expression)


class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

def tokenize(expression):
    tokens = []
    current_number = ''
    
    for char in expression:
        if char.isspace():
            continue
        if char.isdigit() or char == '.':
            current_number += char
        else:
            if current_number:
                tokens.append(('NUMBER', float(current_number)))
                current_number = ''
            tokens.append(('OPERATOR', char))
    
    if current_number:
        tokens.append(('NUMBER', float(current_number)))
    
    return tokens

def parse_expression(tokens):
    def parse_term(index):
        if index >= len(tokens):
            return None, index
        
        if tokens[index][0] == 'NUMBER':
            return Node('number', tokens[index][1]), index + 1
        
        return None, index

    def parse_multiplication(index):
        left, next_index = parse_term(index)
        if left is None:
            return None, index
        
        while next_index < len(tokens) and tokens[next_index][0] == 'OPERATOR' and tokens[next_index][1] in ['*', '/']:
            operator = tokens[next_index][1]
            right, new_index = parse_term(next_index + 1)
            if right is None:
                break
            left = Node('operator', operator, left, right)
            next_index = new_index
            
        return left, next_index

    def parse_addition(index):
        left, next_index = parse_multiplication(index)
        if left is None:
            return None, index
        
        while next_index < len(tokens) and tokens[next_index][0] == 'OPERATOR' and tokens[next_index][1] in ['+', '-']:
            operator = tokens[next_index][1]
            right, new_index = parse_multiplication(next_index + 1)
            if right is None:
                break
            left = Node('operator', operator, left, right)
            next_index = new_index
            
        return left, next_index

    tree, _ = parse_addition(0)
    return tree

def evaluate_tree(node):
    if node.type == 'number':
        return node.value
    
    left_val = evaluate_tree(node.left)
    right_val = evaluate_tree(node.right)
    
    if node.value == '+':
        return left_val + right_val
    elif node.value == '-':
        return left_val - right_val
    elif node.value == '*':
        return left_val * right_val
    elif node.value == '/':
        if right_val == 0:
            raise ValueError("División por cero")
        return left_val / right_val

def evaluate_expression(expression):
    tokens = tokenize(expression)
    tree = parse_expression(tokens)
    if tree is None:
        raise ValueError("Expresión inválida")
    return evaluate_tree(tree)

# Función auxiliar para obtener el árbol (será usada por tree.py)
def get_expression_tree(expression):
    tokens = tokenize(expression)
    return parse_expression(tokens)