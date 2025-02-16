import pandas as pd
import joblib

from c4_discord_bot.cogs.pokeCog.type_classifier.typeUtils import encodeType, decodeType, encodeName

data_path = 'c4_discord_bot/cogs/pokeCog/type_classifier/data/type_syllable.csv'
data = pd.read_csv(data_path)
 #write to file

def load_forest(filename):
    # take a filename, load and return the RandomForestClassifier from type_classifier/models/[filename]
    filename = 'c4_discord_bot/cogs/pokeCog/type_classifier/models/' + filename
    forest = joblib.load(filename)
    return forest

def classifyType1(forest, name, silent=True):
    # take a pokemon name and a fitted RandomForestClassifier, predict the type and return as str
    
    if not silent: print(name)
    
    if len(name) > 12:
        name = ''.join(name[0:12])
    
    name = pd.DataFrame([encodeName(name)], columns=['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11'])
    
    if not silent: print(name.head())
    
    pred = forest.predict(name)
    
    if not silent: print(decodeType(pred[0]))
    
    return decodeType(pred[0])

def classifyType2(forest, name, type1, silent=True):
    
    if not silent: print(name)
    
    if len(name) > 12:
        name = ''.join(name[0:12])
        
    name = pd.DataFrame([encodeName(name)], columns=['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11'])
    
    name = name.join(pd.DataFrame([[encodeType(type1)]], columns=['type_0']))
    
    if not silent: print(name.head())
    
    pred = forest.predict(name)
    
    if not silent: print(decodeType(pred[0]))
    
    return decodeType(pred[0])
    
    
def classifyTypes(type1_forest, type2_forest, name):
    # take a pokemon name and a fitted RandomForestClassifier for each type, predict both types and return as Tuple(str, str)
    type1 = classifyType1(type1_forest, name)
    type2 = classifyType2(type2_forest, name, type1)
    return type1, type2


# train_fit_forest(data, 1)
