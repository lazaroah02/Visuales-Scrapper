def find_all_matches_in_dict(dictionary, key):
    """_Find all matches of a given key in dictionary_

    Args:
        dictionary (_dict_): _Dictionary where to search for matches_
        key (_string_): _Key to search in the dictionary_

    Returns:
        _list_: _List of matches in dictionary_
    """
    results = {}
    
    def search(dictionary, key):
        for k, v in dictionary.items():
            if key in k:
                results[k] = v
        for k, v in dictionary.items():
            if isinstance(v, dict):
                search(v, key)
    
    search(dictionary, key)
    return clean_results(results)

def clean_results(results):
    existing_keys = []
    cleaned_result = {}
        
    def clean_repeated_keys(dictionary, parent_dict):
        for k, v in dictionary.items():
            #if the key is already stored don't add it to the new result
            if k in existing_keys:
                continue
            else:
                #if the key is not stored, add it
                existing_keys.append(k)    
                if isinstance(v, dict):
                    parent_dict[k] = clean_repeated_keys(v, v)
                else: 
                    parent_dict[k] = v    
        return parent_dict            
    
    clean_repeated_keys(results, cleaned_result) 
    return cleaned_result
       