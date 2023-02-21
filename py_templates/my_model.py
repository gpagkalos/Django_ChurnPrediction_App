import os 
import pandas as pd
import torch 
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import StandardScaler


class Network(nn.Module):
    
    def __init__(self, num_input_features):
        super(Network, self).__init__()
        self.linear1 = nn.Linear(num_input_features, 15)
        self.linear2 = nn.Linear(15, 8)
        self.linear3 = nn.Linear(8, 1)
    
    def forward(self, xb):
        prediction = torch.sigmoid(input=self.linear1(xb))
        prediction = torch.sigmoid(input=self.linear2(prediction))
        prediction = torch.sigmoid(input=self.linear3(prediction))
        return prediction


def ModelPredict(df):

	model_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'py_templates\model_torch.pth')


	scaler_params = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)),
	'media\X_train.csv'))
	print('\n\n'+model_path,'\n\n')
	ids_df = df.CustomerId 
	df.drop(labels=['RowNumber', 'CustomerId', 'Surname','Exited'], axis=1, inplace=True)
	df = pd.get_dummies(data=df, drop_first=True)
	model = Network(len(df.columns))
	# Feature scaling
	sc = StandardScaler()

	scaler_params = sc.fit(scaler_params)
	df = sc.transform(df)

	df = torch.from_numpy(df.astype(np.float32))
	model = torch.load(model_path)
	predictions = model(df).reshape((-1,)).cpu().detach().numpy()*100
	return(sorted(list(zip(ids_df.tolist(),(list(np.around(predictions,4))))), key = lambda x: x[1]))