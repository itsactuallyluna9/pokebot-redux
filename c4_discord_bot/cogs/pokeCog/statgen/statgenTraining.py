#trains RandomForestRegressor and MultiOutputRegressor to take encoded name values and types and predict the 6 base stats

from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
import joblib

#all characters legally generated by base model
legal_chars = ['\n', ' ', '-', '.', '2', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#functions to encode and decode list[char]
char_to_int = dict((c, i) for i, c in enumerate(legal_chars))
int_to_char = dict((i, c) for c, i in char_to_int.items())

def encodeName(name):
    
    try: 
        name = name.lower()
    except AttributeError:
        return [0] #handle NaN
    chars = [char_to_int[char] for char in list(name) if char in legal_chars]
        
    name = chars
        
    while len(name) < 12:
        name.append(int(0)) 
    
    return name

def encodeType(type_str):
        # takes str containing a valid type / nan (case-insensitive) and returns the int representation (between 0 and 18)
        
        try: 
            type_str = type_str.lower()
        except AttributeError:
            return 18 #handle NaN
        type_int = None
        
        match type_str:
            case 'fire': type_int = 0
            case 'water': type_int = 1
            case 'grass': type_int = 2
            case 'electric': type_int = 3
            case 'ice': type_int = 4
            case 'fighting': type_int = 5
            case 'poison': type_int = 6
            case 'ground': type_int = 7
            case 'flying': type_int = 8
            case 'psychic': type_int = 9
            case 'bug': type_int = 10
            case 'rock': type_int = 11
            case 'ghost': type_int = 12
            case 'dark': type_int = 13
            case 'dragon': type_int = 14
            case 'steel': type_int = 15
            case 'fairy': type_int = 16
            case 'normal': type_int = 17
            case 'nan': type_int = 18
            case _: raise ValueError('Invalid type entered')
            
        return type_int
