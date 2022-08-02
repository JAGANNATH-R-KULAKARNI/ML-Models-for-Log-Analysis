from django.urls import path
from . import views

urlpatterns=[
    path('logistic_regression',views.Logistic_regression,name='Logistic_regression'),
     path('k_neighbors_classifier',views.KNeighborsClassifier,name='KNeighborsClassifier'),
      path('decision_tree_classifier',views.DecisionTreeClassifier,name='DecisionTreeClassifier'),
       path('random_forest',views.RandomForest,name='RandomForest'),
        path('knn',views.NaiveBayes,name='NaiveBayes'),
]