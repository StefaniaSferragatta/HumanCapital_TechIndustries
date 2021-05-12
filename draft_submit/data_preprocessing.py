data = pd.read_csv('datasets/employee_reviews_sub.csv')

#delete the useless columns
data = data.drop(['Unnamed: 0'], axis= 1)
data = data.drop(['link'], axis= 1)

#Average ratings for different feature (by company). We use these information to fill the missing values in the rating fields.
ratings_comp = data[["company", 'overall-ratings', "work-balance-stars", "culture-values-stars", "carrer-opportunities-stars", "comp-benefit-stars", "senior-mangemnet-stars"]].copy()
ratings_comp.set_index(["company"], inplace=True)
ratings_comp = ratings_comp[~(ratings_comp[['overall-ratings',"work-balance-stars", "culture-values-stars", "carrer-opportunities-stars", "comp-benefit-stars", "senior-mangemnet-stars"]] == "none").any(axis=1)]
ratings_comp[['overall-ratings',"work-balance-stars", "culture-values-stars", "carrer-opportunities-stars", "comp-benefit-stars", "senior-mangemnet-stars"]] = ratings_comp[['overall-ratings',"work-balance-stars", "culture-values-stars", "carrer-opportunities-stars", "comp-benefit-stars", "senior-mangemnet-stars"]].apply(pd.to_numeric)
avg_company = ratings_comp.groupby("company")['overall-ratings',"work-balance-stars", "culture-values-stars", "carrer-opportunities-stars", "comp-benefit-stars", "senior-mangemnet-stars"].mean()
avg_company.columns = ['Overall Ratings',"Work Balance", "Culture Values", "Career Opportunities", "Company Benefits", "Senior Management"]
avg_company = avg_company.transpose()


companies=pd.unique(data['company'])
#in the following dict are stored the mean values for each comapany and each attribute using the previous dataframe avg_company
ratings_per_company={company: avg_company.loc[:,company].values for company in companies}  #companies are keys whereas values are the different ratings

for index,row in tqdm(data.iterrows()):  #for each row in the dataset  
    company=data.iloc[index,0]  #company name
    for index_y in range(4,10):  #for each column from overall ratings to helpful-count       
        if data.iloc[index,index_y]=='none':
            data.iloc[index,index_y]=round(ratings_per_company.get(company)[index_y-4],1)
            
            
#converting dtypes
data['culture-values-stars']=pd.to_numeric(data['culture-values-stars'])
data['work-balance-stars']=pd.to_numeric(data['work-balance-stars'])
data['carrer-opportunities-stars']=pd.to_numeric(data['carrer-opportunities-stars'])
data['comp-benefit-stars']=pd.to_numeric(data['comp-benefit-stars'])
data['senior-mangemnet-stars']=pd.to_numeric(data['senior-mangemnet-stars'])


#get rid of the row without location
data= data[data['location']!='none']
# add a column with the year only
data['year'] = pd.to_datetime(data['dates'], errors='coerce').dt.year
#delete the column with the dates
del data['dates']

#Use the data only with location in California
data_CA=data['location'].filter(regex='CA$',axis=0)
california_loc=pd.unique(list(filter(lambda loc:re.findall(r'CA$',loc),data['location'])))
data_CA=data[data['location'].isin(california_loc)]


#Save the processed dataframe into a file
data_CA.to_csv('processed_employee_reviews.csv')