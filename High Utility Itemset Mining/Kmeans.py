#Simple Linear Regression

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#import dataset
dataset=pd.read_csv("C:\\Users\Aman\Desktop\Final Final Project\inputC.csv")
X = dataset.iloc[:,1:-1].values
Y = dataset.iloc[:,2].values
K = dataset.iloc[:,[1,2]].values

#Splitting the dataset into the training set and test set
from sklearn.cross_validation import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 1/5,random_state = 0)

#Fitting Simple Linear Regression to the training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train,Y_train)

#Predicting the test set results
Y_pred = regressor.predict(X_test)

"""#detect outliers
lower_bound = 0.1
upper_bound = 0.95
res = Y.quantile([lower_bound,upper_bound])
print("Outliers are ")
print(res)"""

#coorelation matrix
print("The correlation matrix is ")
correl = np.corrcoef(Y)
print(coorel)

#visualising the training set results
plt.scatter(X_train,Y_train,color='RED')
plt.plot(X_train, regressor.predict(X_train))
plt.title("Utility Vs Support")
plt.ylabel("Utility")
plt.xlabel("Support")
plt.show()

#using the elbow method to find optimal number of cluster
from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
    kmeans.fit(K)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1,11),wcss)
plt.title('The elbow method')
plt.xlabel('No of clusters')
plt.ylabel('WCSS')
plt.show()

#applying kmeans to the mall dataset
kmeans = KMeans(n_clusters=2,init='k-means++',random_state=0)
ykmeans = kmeans.fit_predict(K)

#Visualising the clusters
plt.scatter(K[ykmeans==0,0],K[ykmeans==0,1],s = 100,c = 'red',label ='Cluster 1')
plt.scatter(K[ykmeans==1,0],K[ykmeans==1,1],s = 100,c = 'blue',label ='Cluster 2')
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=300,c='yellow',label='centroid')
plt.title('Clusters of itemsets')
plt.xlabel('XX')
plt.ylabel('YY')
plt.legend()
plt.show()
    


 
