

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