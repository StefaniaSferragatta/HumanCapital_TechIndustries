# utility libraries
import pandas as pd
from tqdm import tqdm
import math 
import regex as re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import boxplot as bp

#ML libraries 
from scipy import stats
from scipy.stats import randint
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder

# Causal Inference libraries
from pgmpy.estimators import HillClimbSearch, MaximumLikelihoodEstimator, BicScore, K2Score
from pgmpy.inference.CausalInference import CausalInference
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
#import econml
import networkx as nx
import pylab as plt
from IPython.display import Image, display
import dowhy
import graphviz
from dowhy import CausalModel

def corr_matrix(df_company):
    ord_enc = OrdinalEncoder()
    df_company["Job_code"]=ord_enc.fit_transform(df_company[["job-title"]])
    df_company['Locations_code']=ord_enc.fit_transform(df_company[["location"]])

    #delete the categorical&useless columns
    df_company = df_company.drop(['company'], axis= 1)
    df_company = df_company.drop(['location'], axis= 1)
    df_company = df_company.drop(['job-title'], axis= 1)
    df_company = df_company.drop(['year'], axis= 1)

    #Normalize the values
    scaler = MinMaxScaler() 
    df_company_norm= scaler.fit_transform(df_company)
    df_company_new=pd.DataFrame(df_company_norm,columns=['overall_ratings','work_balance_stars','culture_values_stars','carrer_opportunities_stars','comp_benefit_stars','senior_mangemnet_stars',"helpful_count","Job_code","Locations_code"])
    #compute the correlation matrix
    corr_df_company = df_company_new.corr()
    return (corr_df_company)














def refutel(mode):
    refutel = model_fb.refute_estimate(estimands,estimate, mode)
    print(refutel)
