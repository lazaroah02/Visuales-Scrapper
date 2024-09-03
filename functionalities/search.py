def find_all_matches_in_dict(dictionary, key):
    """_Find all matches of a given key in dictionary_

    Args:
        dictionary (_dict_): _Dictionary where to search for matches_
        key (_string_): _Key to sarch in the dictionary_

    Returns:
        _list_: _List of matches in dictionary_
    """
    results = []
    
    def search(dictionary, key):
        for k, v in dictionary.items():
            if key in k:
                results.append(dictionary[k])
        for k, v in dictionary.items():
            if isinstance(v, dict):
                search(v, key)
    
    search(dictionary, key)
    return results