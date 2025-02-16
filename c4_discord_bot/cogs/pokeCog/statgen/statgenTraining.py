#trains RandomForestRegressor and MultiOutputRegressor to take encoded name values and types and predict the 6 base stats


from c4_discord_bot.cogs.pokeCog.type_classifier.typeUtils import char_to_int, legal_chars


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
