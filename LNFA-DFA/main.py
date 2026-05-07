from parse import parse_input

def lambda_closure(states, transition_function):
    # ideea principala a unei inchideri e aplicarea unei operatie pe o multime pana nu mai poti
    # de ex ideea aici e ca inchiderea unei stari q sunt toate starile la care pot ajunge prin cuvantul vid adica lambda (fara sa consum altceva)
    # practic ar fi acelasi punct de plecare si echivalent dpdv al parserului meu

    stack = list(states)
    closure = set(states) # pornesc cu starile date

    while stack:

        state = stack.pop() #iau o stare

        for next_st in transition_function.get(state, {}).get('lambda', []): # pt fiecare stare vad daca are tranz lambda

            if next_st not in closure: # daca nu l am vizitat deja

                closure.add(next_st)
                stack.append(next_st) # il explorez si pe el

    return frozenset(closure) #returnez ca fronzenset deoarece trebuie sa fie hashable


def lnfa_to_dfa(states, alphabet, transition_function, init_state, final_states):
    dfa_alphabet = [s for s in alphabet if s != 'lambda']

    # starea initiala a DFA-ului
    dfa_init = lambda_closure({init_state}, transition_function)

    # BFS
    queue = [dfa_init] #starile de explorat
    dfa_states = [dfa_init] # cele pe care le am descoperit deja

    dfa_transition = {} #functia de tranzitie

    while queue:
        current = queue.pop(0)
        dfa_transition[current] = {} #aici e motivul pt care aveam nevoie de frozenset  

        for symbol in dfa_alphabet:
            # unde ajung pe symbol din toate starile din current
            next_states = set()
            for nfa_state in current:
                next_states.update(
                    transition_function.get(nfa_state, {}).get(symbol, [])
                )

            # closure pe rezultat
            dfa_state = lambda_closure(next_states, transition_function) if next_states else frozenset()

            dfa_transition[current][symbol] = dfa_state

            if dfa_state not in dfa_states:
                dfa_states.append(dfa_state)
                queue.append(dfa_state)

    # stare DFA e finala daca contine cel putin o stare finala NFA, adica tb sa fac intersectia
    dfa_final = [s for s in dfa_states if s & set(final_states)]

    return dfa_states, dfa_alphabet, dfa_transition, dfa_init, dfa_final




def minimize_dfa(dfa_states, alphabet, transition, init_state, final_states):


    # partitia initiala pe finale si nefinale si in partition bag tot

    finals = frozenset(s for s in dfa_states if s in final_states) #analog iau frozenset pt ca e hashable
    non_finals = frozenset(s for s in dfa_states if s not in final_states)
    partition = {g for g in [finals, non_finals] if g}

     
    #aici sparg pana nu mai pot sparge, adica submultimele dupa operatiile efectuate sunt identice cu cele de dinainte de a efectua ceva asupra lor
    while True:
        new_partition = set()
        for group in partition:

            #sparg grupul dupa comportament, starile cu acc signatura o sa mearga in acelasi bucket
            buckets = {}
            for state in group:

                #signatura = pe fiecare simbol, in ce grup ajung
                sig = tuple(

                    next((i for i, g in enumerate(partition) if transition[state][sym] in g), -1)
                    for sym in alphabet
                )


                #cele lfl le bag in acc bucket
                if sig not in buckets:
                    buckets[sig] = set()
                buckets[sig].add(state)

            #fiecare bucket devine grup nou in noua partitie
            for bucket in buckets.values():
                new_partition.add(frozenset(bucket))

        if new_partition == partition: #daca dupa spargere sunt echivalente am terminat
            break
        partition = new_partition

    # construiesc DFA-ul minim
    group_of = {s: g for g in partition for s in g}
    name = {g: 'M' + str(i) for i, g in enumerate(partition)} #nultime Mi

    min_trans = {}
    for g in partition:
        rep = next(iter(g))

        min_trans[name[g]] = {
            sym: name[group_of[transition[rep][sym]]]
            for sym in alphabet if transition[rep][sym] in group_of
        }


    return (
        list(name.values()),
        alphabet,
        min_trans,
        name[group_of[init_state]],
        list({name[group_of[s]] for s in final_states})
    )




def write_dfa(g, states, alphabet, transition, init_state, final_states):
    # redenumesc daca sunt frozenset-uri
    if states and isinstance(states[0], frozenset):
        name = {s: 'D' + str(i) for i, s in enumerate(states)}
        states_named = [name[s] for s in states]
        init_named = name[init_state]
        finals_named = [name[s] for s in final_states]
        trans_named = {}
        for src in states:
            for sym in transition.get(src, {}):
                dst = transition[src][sym]
                if name[src] not in trans_named:
                    trans_named[name[src]] = {}
                trans_named[name[src]][sym] = name[dst]
    else:
        states_named = states
        init_named = init_state
        finals_named = final_states
        trans_named = transition

    g.write(' '.join(states_named) + '\n')
    g.write(' '.join(alphabet) + '\n')
    count = sum(len(trans_named[s]) for s in trans_named)
    g.write(str(count) + '\n')
    for src in trans_named:
        for sym in sorted(trans_named[src]):
            g.write(f'{src} {trans_named[src][sym]} {sym}\n')
    g.write(init_named + '\n')
    g.write(' '.join(finals_named) + '\n')
    
 
if __name__ == '__main__':
    states, alphabet, tf, init, finals = parse_input('input.txt')

    dfa_states, dfa_alpha, dfa_trans, dfa_init, dfa_finals = lnfa_to_dfa(
        states, alphabet, tf, init, finals
    )

    min_states, min_alpha, min_trans, min_init, min_finals = minimize_dfa(
        dfa_states, dfa_alpha, dfa_trans, dfa_init, dfa_finals
    )

    with open('output.txt', 'w') as g:
        # DFA echivalent
        g.write("DFA echivalent:\n")
        write_dfa(g, dfa_states, dfa_alpha, dfa_trans, dfa_init, dfa_finals)
        g.write("\nDFA minim:\n")
        write_dfa(g, min_states, min_alpha, min_trans, min_init, min_finals)