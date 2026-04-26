from parse import parse_input
from dfa import dfa_acceptor



def nfa_acceptor(nfa):
    states, alphabet, transition_function, init_state, final_states, words = nfa #despachetez din parsare
    res = [] # de aici bag in output

    for word in words:
        current_states = {init_state}
        i = 0
    
        while i < len(word):
    
            next_states = set()
            found = False
    
            for symbol in sorted(alphabet, key=len, reverse=True):
    
                if word.startswith(symbol, i):
    
            # din starea state, pe simbolul symbol, unde pot ajunge? raspunsul e appended in next states
            # practic in acel set colectez toate ramurile nedeterminismului

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

            current_states = next_states




        res.append("DA" if current_states & set(final_states) else "NU")
    with open('nfa_output.txt', 'w') as g:

        g.write('Alfabet: ' + ' '.join(alphabet) + '\n')
        g.write('\n'.join(res))

if __name__ == "__main__":
        
    nfa_acceptor(parse_input("nfa_input.txt"))