from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
from fastapi import FastAPI
import pickle
from glob import glob


app = FastAPI()

stock_files=sorted(glob('./datasets/*'))
# stock_files = sorted(glob('../input/network-dataset/*'))
stock_files
initial_data = pd.concat((pd.read_csv(file) for file in stock_files), ignore_index=True )
data_to_use = initial_data.dropna()

X = data_to_use.drop(axis=1, columns=['type']) # X is a dataframe
X = X.drop(axis=1, columns=['label','weird_name','weird_notice','weird_addl','src_ip','dst_ip','http_trans_depth','http_method',
                            'http_uri','http_version','http_request_body_len','http_response_body_len','http_status_code','http_resp_mime_types',
                            'http_orig_mime_types','ssl_issuer','ssl_subject','ssl_resumed','ssl_cipher','ssl_version','dns_query',
                            'dns_qclass','dns_qtype','dns_rcode','dns_AA','dns_RD','dns_RA','dns_rejected','http_user_agent'])



y1 = data_to_use['type'].values # y is an array
y2 = data_to_use['label'].values

X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size=0.3, random_state=1)
X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size=0.3, random_state=1)


X1_train = X_train
X1_test = X_test

numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_train.select_dtypes(include=['object']).columns

t = [('ohe', OneHotEncoder(handle_unknown = 'ignore'), categorical_cols),
    ('scale', StandardScaler(), numerical_cols)]

t1 = [('ohe', OneHotEncoder(drop='first'), categorical_cols),
    ('scale', StandardScaler(), numerical_cols)]

col_trans = ColumnTransformer(transformers=t)
col1_trans = ColumnTransformer(transformers=t1)

# fit the transformation on training data
col_trans.fit(X_train)
col1_trans.fit(X1_train)

X_train_transform = col_trans.transform(X_train)

X_test_transform = col_trans.transform(X_test)

X1_train_transform = col1_trans.transform(X1_train)

X1_test_transform = col1_trans.transform(X1_test)

@app.get("/")
def home():
    return {"text": "IOT Attacks prediction"}


@app.get("/predict")
def predict(ts: int, src_port:int, dst_port:int,proto:str, service:str, duration:float,
       src_bytes:int, dst_bytes:int,conn_state:str, missed_bytes:int, src_pkts:int,
       src_ip_bytes:int, dst_pkts:int, dst_ip_bytes:int,  
       ssl_established:str):
    X_predict =[ts, src_port, dst_port, proto, service, duration,
       src_bytes, dst_bytes, conn_state, missed_bytes, src_pkts,
       src_ip_bytes, dst_pkts, dst_ip_bytes, ssl_established]
    
    X_predict = pd.DataFrame(data=[X_predict],columns =['ts', 'src_port', 'dst_port', 'proto', 'service', 'duration',
       'src_bytes', 'dst_bytes', 'conn_state', 'missed_bytes', 'src_pkts',
       'src_ip_bytes', 'dst_pkts', 'dst_ip_bytes', 'ssl_established']) 
    
    X1_predict = X_predict.copy()
    X_predict  = col_trans.transform(X_predict)
    X1_predict = col1_trans.transform(X1_predict)

    
    model = pickle.load(open('./models/attack_or_normal_response/logisticRegression.pkl', 'rb'))
    model2 = pickle.load(open('./models/attack_type/logisticRegression.pkl', 'rb'))
   
   
    make_prediction = model.predict(X_predict)
    make_prediction_attack = model2.predict(X1_predict)
    output = make_prediction
    output2= make_prediction_attack
    return {"result":output.tolist() ,"result2": output2.tolist()}