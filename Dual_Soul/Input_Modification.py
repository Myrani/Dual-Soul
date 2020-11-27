def extract_Translation_Table(content):
    
    cpt = len(content)/2
    i = 0
    preference_dictionary = {}
   
    while i <= cpt+2 :
        preference_dictionary[content[i]] = content[i+1]
        i+=2
    
    return preference_dictionary

