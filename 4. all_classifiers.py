from __future__ import division 
import numpy as np
import pandas as pd
import math

from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix, classification_report


from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


models = []
models.append(('KNN (K=3)', KNeighborsClassifier(n_neighbors = 3, weights='uniform')))
models.append(('RFC', RandomForestClassifier(n_estimators=50, criterion='entropy')))
models.append(('SVM', SVC(kernel='linear' )))
models.append(('ANN', MLPClassifier(hidden_layer_sizes=(100,100))))


# # Preparing data

# In[44]:


all_data = pd.read_csv("<path of the file that contains the expression valuesof the selected genes>", sep="\t", header=None)
X_train = all_data.T.iloc[:,:].values
print len(X_train[:, 0])


# # True labels

# In[45]:


positive_labels = np.zeros(40)		#number will be changed according to each datasets
negative_labels = np.ones(157)		#number will be changed according to each datasets		
true_labels = np.append(positive_labels, negative_labels)

print true_labels


scoring = {'accuracy' : make_scorer(accuracy_score), 
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score),
           'f1' : make_scorer(f1_score)}


kfold = KFold(n_splits=10)
for name, model in models:
    print name, "\n----------------------------------"
    for i in scoring.keys():
        results = cross_val_score(estimator=model, 
                                  X=X_train, 
                                  y=true_labels, 
                                  cv=kfold, 
                                  scoring=i)
        print "Average_"+str(i),": ", np.mean(results)
    y_pred = cross_val_predict(model, X_train, true_labels , cv=kfold)
    #print y_pred
    a= confusion_matrix(true_labels, y_pred)
    TP= a[0][0]
    TN= a[1][1]
    FP= a[0][1]
    FN = a[1][0]
    specificity = TN/(TN+FP)
    print "Specificity : ",  specificity
    MCC = ((TP*TN)-(FP*FN))/ math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    print "MCC : ",  MCC
    print a
    print "\n\n"

