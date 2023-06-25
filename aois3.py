def generate_truth_table_variables(num_variables):
    truth_table = []
    num_rows = 2 ** num_variables

    for i in range(num_rows):
        row = []
        for j in range(num_variables - 1, -1, -1):
            row.append((i >> j) & 1)
        truth_table.append(row)

    return truth_table


def read_func(expression, variable_set):
    stack = []
    for ch in expression:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            sub_exp = ''
            while stack and stack[-1] != '(':
                sub_exp += stack.pop()
            stack.pop()  # Remove '(' from stack
            sub_exp = sub_exp[::-1]  # Reverse sub-expression
            result = read_func(sub_exp, variable_set)  # Evaluate sub-expression
            stack.append('1' if result else '0')  # Push the result back to stack
        elif ch.isalpha():
            value = variable_set[ch]
            stack.append('1' if value else '0')
        else:
            stack.append(ch)
    result_exp = ''.join(stack)
    return result_exp == '1'

def get_sdnf_from_minterms(minterms, truth_table):
    sdnf_terms = []
    num_variables = len(truth_table[0])
    
    for minterm in minterms:
        term = []
        for i in range(num_variables):
            if truth_table[minterm][i] == 1:
                term.append(f"A{i+1}")
            else:
                term.append(f"!A{i+1}")
        sdnf_terms.append(" & ".join(term))
    
    sdnf = " | ".join(f"({term})" for term in sdnf_terms)
    return sdnf

def minimize_calculative(expression):
    variables = list(set([ch for ch in expression if ch.isalpha()]))
    num_variables = len(variables)
    truth_table = generate_truth_table_variables(num_variables)
    variable_set = {ch: 1 for ch in variables}

    minterms = []
    for i, row in enumerate(truth_table):
        variable_set.update({variables[j]: row[j] for j in range(num_variables)})
        result = int(read_func(expression, variable_set))
        if result == 1:
            minterms.append(i)

    sdnf = get_sdnf_from_minterms(minterms, truth_table)
    sknf = get_sknf_from_maxterms(list(set(range(2 ** num_variables)) - set(minterms)), truth_table)

    return sdnf, sknf


def minimize_calculative_tabular(expression):
    variables = list(set([ch for ch in expression if ch.isalpha()]))
    num_variables = len(variables)
    truth_table = generate_truth_table_variables(num_variables)
    variable_set = {ch: 1 for ch in variables}

    minterms = []
    for i, row in enumerate(truth_table):
        variable_set.update({variables[j]: row[j] for j in range(num_variables)})
        result = int(read_func(expression, variable_set))
        if result == 1:
            minterms.append(i)

    sdnf = get_sdnf_from_minterms(minterms, truth_table)
    sknf = get_sknf_from_maxterms(list(set(range(2 ** num_variables)) - set(minterms)), truth_table)

    return sdnf, sknf


def minimize_tabular(expression):
    variables = list(set([ch for ch in expression if ch.isalpha()]))
    num_variables = len(variables)
    truth_table = generate_truth_table_variables(num_variables)
    variable_set = {ch: 1 for ch in variables}

    minterms = []
    for i, row in enumerate(truth_table):
        variable_set.update({variables[j]: row[j] for j in range(num_variables)})
        result = int(read_func(expression, variable_set))
        if result == 1:
            minterms.append(i)

    sdnf = get_sdnf_from_minterms(minterms, truth_table)
    sknf = get_sknf_from_maxterms(list(set(range(2 ** num_variables)) - set(minterms)), truth_table)

    return sdnf, sknf


def get_sknf_from_maxterms(maxterms, truth_table):
    sknf_terms = []
    for maxterm in maxterms:
        term = []
        for i, value in enumerate(truth_table[maxterm]):
            if value == 0:
                term.append(f"A{i + 1}")
            elif value == 1:
                term.append(f"!A{i + 1}")
        sknf_terms.append(term)
    return sknf_terms


def start():
    expression = "!(A+!B)*(!(!A*!B))"
    print("Expression:", expression)
    print()

    print("Calculative Method:")
    sdnf, sknf = minimize_calculative(expression)
    print("Minimized:", get_sknf_expression(sknf))
    print()

    print("Calculative-Tabular Method:")
    sdnf, sknf = minimize_calculative_tabular(expression)
    print("Minimized:", get_sknf_expression(sknf))
    print()

    print("Tabular Method:")
    sdnf, sknf = minimize_tabular(expression)
    print("Minimized:", get_sknf_expression(sknf))
    print()


def get_sdnf_expression(sdnf_terms):
    sdnf = ""
    for term in sdnf_terms:
        if len(term) > 1:
            sdnf += "(" + " & ".join(term) + ")"
        else:
            sdnf += term[0]
        sdnf += " | "
    return sdnf[:-3]


def get_sknf_expression(sknf_terms):
    sknf = ""
    for term in sknf_terms:
        if len(term) > 1:
            sknf += "(" + " | ".join(term) + ")"
        else:
            sknf += term[0]
        sknf += " & "
    return sknf[:-3]


start()

