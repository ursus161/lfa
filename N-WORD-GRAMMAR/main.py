from parse_grammar import parse_input


def generate_words(filename):

    non_terminals, terminals, productions, start_symbol, length = parse_input(filename)

    results = set() # set ca sa nu am duplicate

    def derive(current, depth):
        # daca am depasit lungimea taiata nu mai  continui
        if len(current) > length:
            return

        # caut primul neterminal din stringul curent
        nt_index = -1
        for i, ch in enumerate(current):
            if ch in non_terminals:
                nt_index = i
                break

        # nu mai am neterminale, verific daca e solutie
        if nt_index == -1:
            if len(current) == length:
                results.add(current)
            return

        # inlocuiesc neterminalul cu fiecare productie posibila (ramurile DFS-ului)
        nt = current[nt_index]
        for prod in productions.get(nt, []):
            if prod == 'lambda':
                # lambda = sterg neterminalul
                new = current[:nt_index] + current[nt_index + 1:]
            else:
                # inlocuiesc neterminalul cu corpul productiei
                new = current[:nt_index] + prod + current[nt_index + 1:]
            derive(new, depth + 1)



    derive(start_symbol, 0)

    return sorted(results)


if __name__ == '__main__':
    words = generate_words('input.txt')
    with open('output.txt', 'w') as g:
        if words:
            g.write('\n'.join(words))
        else:
            g.write('NU EXISTA')