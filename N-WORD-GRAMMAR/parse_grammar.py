

def parse_input(filename):


    with open(filename, 'r') as f:
        lines = f.readlines()

    non_terminals = lines[0].strip().split()
    terminals = lines[1].strip().split()
    num_productions = int(lines[2].strip())

    productions = {}

    for i in range(3, 3 + num_productions):

        parts = lines[i].strip().split()
        nt = parts[0]
        body = parts[1]  # sir de simboluri sau 'lambda'
        
        if nt not in productions:
            productions[nt] = [body]
        else:
            productions[nt].append(body)

    start_symbol = lines[3 + num_productions].strip()
    length = int(lines[4 + num_productions].strip())

    return non_terminals, terminals, productions, start_symbol, length