from pymongo import MongoClient
import pandas as pd 
import pickle

client = MongoClient('localhost', 27017)
db = client["Ipo2"]
    
with open('regression/saved_model.pkl','rb') as f:
    model = pickle.load(f)
    
def get_model():
    df = pd.DataFrame(db.inform.find({},{'_id':False}))
    print(df)


    
get_model()
    


