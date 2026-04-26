from parse import parse_input

def lnfa_to_regex(filename):
    states, alphabet, transition_function, init_state, final_states = parse_input(filename)

    # stari noi pt state elimination
    # la final ideea e sa raman cu start -> regex ul specific automatului cu toate starile eliminate -> accept
    start = 'START'
    accept = 'ACCEPT'
    all_states = [start] + states + [accept]

    # matricea de regex-uri intre fiecare pereche de stari o init vida
    regex_matrix = {}
    for s1 in all_states:
        regex_matrix[s1] = {}
        for s2 in all_states:
            regex_matrix[s1][s2] = None

    # lambda de la start la starea initiala originala
    regex_matrix[start][init_state] = 'lambda'

    # lambda de la fiecare stare finala la accept
    for final_state in final_states:
        regex_matrix[final_state][accept] = 'lambda'

    # copiez tranzitiile existente in matrice
    for src in transition_function:
        for symbol in transition_function[src]:
            for dst in transition_function[src][symbol]:
                if regex_matrix[src][dst] is None:
                    regex_matrix[src][dst] = symbol
                else:
                    regex_matrix[src][dst] = regex_matrix[src][dst] + '+' + symbol

    # elimin starile una cate una (toate in afara de start si accept)
    states_to_remove = list(states)  # doar starile originale

    for removed in states_to_remove:
        # loop pe starea eliminata
        loop = regex_matrix[removed][removed]

        for pred in all_states:
            if pred == removed:
                continue
            edge_in = regex_matrix[pred][removed]
            if edge_in is None:
                continue

            for succ in all_states:
                if succ == removed:
                    continue
                edge_out = regex_matrix[removed][succ]
                if edge_out is None:
                    continue

                # construiesc noul regex: edge_in · loop* · edge_out
                if loop is not None:
                    new_path = _concat(_concat(edge_in, _star(loop)), edge_out)
                else:
                    new_path = _concat(edge_in, edge_out)

                # reuniune cu ce era deja pe muchia pred -> succ
                if regex_matrix[pred][succ] is None:
                    regex_matrix[pred][succ] = new_path
                else:
                    regex_matrix[pred][succ] = _union(regex_matrix[pred][succ], new_path)

        # sterg starea eliminata din matrice
        all_states.remove(removed)

    result = regex_matrix[start][accept]
    if result is None:
        result = 'EMPTY'  # limbaj vid

    return result


# functiile cu _ in fata de obicei sunt functii helper 
def _concat(a, b):
    # concatenare, skip lambda
    if a == 'lambda':
        return b
    if b == 'lambda':
        return a
    # pun paranteze daca e reuniune (contine |)
    if '+' in a:
        a = '(' + a + ')'
    if '+' in b:
        b = '(' + b + ')'
    return a + '' + b

#reuniunea
def _union(a, b):
    return a + '+' + b

#stelarea klenee de 1 sau de mai multe ori elementul x se not cu x*
def _star(a):
    if len(a) == 1:
        return a + '*'
    return '(' + a + ')' + '*'


if __name__ == '__main__':
    regex = lnfa_to_regex("input.txt")
    with open("output.txt", "w") as g:
        g.write(regex)
    print(regex)