
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

    return closure


def lnfa_acceptor(lnfa):
    states, alphabet, transition_function, init_state, final_states, words = lnfa
    res = []

    for word in words:

        current_states = lambda_closure({init_state}, transition_function)
        # ma duc peste tot pe lambda din start
        # incep din starea initiala dar daca am lambda tranzitii pot sa fiu in orice stare practic 
        i = 0

        while i < len(word):
            next_states = set()
            found = False

            for symbol in sorted(alphabet, key=len, reverse=True):
                if symbol == 'lambda': # nu e simbol real, skip 
                    continue

                # de aici in jos e ca la nfa ul fara lambda tranzitii
                if word.startswith(symbol, i):


                    for state in current_states:
                        next_states.update(

                            transition_function.get(state, {}).get(symbol, [])
                        )


                    i += len(symbol)
                    found = True
                    break

            if not found or not next_states:
                current_states = set()
                break

            current_states = lambda_closure(next_states, transition_function) # ma duc pe lambda dupa fiecare pas

        res.append("DA" if current_states & set(final_states) else "NU")

    with open('lnfa_output.txt', 'w') as g:

        g.write('Alfabet: ' + ' '.join(set( el for el in alphabet if el!= "lambda")) + '\n')
        g.write('\n'.join(res))


lnfa_acceptor(parse_input("lnfa_input.txt"))