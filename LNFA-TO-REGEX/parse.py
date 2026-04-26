

def parse_input(filename):

    transition_function = {}

    with open(filename, 'r') as f:
        
        lines = f.readlines()
    

    states = lines[0].strip().split()
    alphabet = lines[1].strip().split()

    i=2
    while i<len(lines):

        parts = lines[i].strip().split()
        if len(parts) == 3:
            leaving_state, arriving_state ,symbol = parts
            if leaving_state not in transition_function:

                transition_function[leaving_state] = {symbol: [arriving_state]}

            #adica era deja adaugata starea de plecare    
            else:
                
                if symbol not in transition_function[leaving_state]:
                    transition_function[leaving_state][symbol] = [arriving_state]

                else :
                    transition_function[leaving_state][symbol].append(arriving_state)
            
            i+=1

        else:
            break # am terminat tranzitiile si ne ducem pe starea initiala si starile finale

    init_state = lines[i].strip()
    final_states = lines[i+1].strip().split()
    
    return states, alphabet, transition_function, init_state, final_states