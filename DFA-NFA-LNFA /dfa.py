import pprint
from parse import parse_input 


# states, alphabet, transition_function, initial_state, final_states = parse_input('dfa.txt')

# print("States:", states)
# print("Alphabet:", alphabet)
# print("Transition Function:")
# pprint.pprint(transition_function)

def dfa_acceptor(dfa):

    states, alphabet, transition_function, initial_state, final_states , words = dfa
    
    res = []
    

    for word in words:

        match_found = True # per word si crapa daca in punctul i nu mai poate continua 
        current_state = initial_state
        i = 0

        while i < len(word):

            found_transition = False #asta e per pas intr un punct dat

            for symbol in sorted(alphabet, key=len, reverse=True): #incerc sa abordez greedy iau cat mai mare pot
                if word.startswith(symbol, i): 

                    if current_state in transition_function and symbol in transition_function[current_state]:


                        current_state = transition_function[current_state][symbol]
                        i += len(symbol) #si sar peste simbol 
                        found_transition = True
                        break

            if not found_transition:
                match_found = False
                break

        res.append("DA" if current_state in final_states and match_found else "NU") 


    with open('dfa_output.txt','w') as g:

          g.write('Alfabet: ' + ' '.join(alphabet) + '\n')
          g.write('\n'.join(res))
 
 
if __name__ == '__main__':
    dfa_acceptor(parse_input('dfa_input.txt'))