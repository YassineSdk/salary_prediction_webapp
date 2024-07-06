import select
import joblib
import streamlit as st
import pandas as pd 
from sklearn.preprocessing import LabelEncoder,StandardScaler
import joblib
import time

st.set_page_config(page_title="salary predicter",
                   page_icon="💰",
                   layout='wide')


page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1511649475669-e288648b2339?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: cover;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}
[data-testid="stSidebar"]{
background-color: rgba(0,0,0,0);
}
[data-testid="element-container"]{
background-color: rgba(0,0,0,0);
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

## About the Salary Predictor App


st.title('Salary predicter 💰')
st.divider()



intro_markdown ="""

This salary predictor app is trained on a dataset sourced from the United States. It uses machine learning to predict salaries based on various input criteria such as education level, years of experience, location, job title, age, and gender.

### Features:
- **Education Level:** Choose from High School, Bachelor's, Master's, or PhD.
- **Years of Experience:** Input the number of years relevant to your job experience.
- **Location:** Select Urban, Suburban, or Rural.
- **Job Title:** Pick from Manager, Director, Analyst, or Engineer.
- **Age:** Enter your current age.
- **Gender:** Specify Male or Female.

### Dataset Information:
The model is trained on a USA dataset, ensuring relevance and accuracy for predicting salaries within the US job market.

### How to Use:
1. Fill in all required fields in the sidebar.
2. Click the **Predict** button to see your estimated salary based on the input criteria.

Feel free to explore and adjust the inputs to see how different factors can affect salary predictions.
"""

show_intro = True




model = joblib.load('predicter')

keys = [1,2]
def clear_text():
    for n in keys :
        st.session_state[n]=""





template = pd.DataFrame(columns=['Experience', 'Age', 'Education_Bachelor', 'Education_High School',
       'Education_Master','Education_PhD', 'Location_Rural','Location_Suburban','Location_Urban','Job_Title_Analyst',
       'Job_Title_Director','Job_Title_Engineer','Job_Title_Manager',
       'Gender_Female', 'Gender_Male'])





with st.sidebar:
    st.markdown('')
    st.title('insert your critirea:')
    clear = st.button('clear',on_click=clear_text,key=5)
    
    form = st.form("independante variable:")
    education_leval = form.selectbox('level of education',
                                     options=['High School','Bachelor','Master','PhD'])
    experience = form.text_input('years of experience',key=2)
    location = form.selectbox('Location',
                              options=['Urban','Suburban','Rural'])
    job_title =form.selectbox('Job title',
                              options=['Manager','Director','Analyst','Engineer'])
    age = form.text_input('age',key=1)
    Gender = form.selectbox('Gender',
                            options=['Male','Female'])
    
    
    predict = form.form_submit_button('predict')

if predict :
    if (len(age) == 0 or len(experience) == 0) :
        st.error('please Fill in all required fields')
    else :
        show_intro = False
        
        data = {
            'Education':education_leval,
            'Experience':int(experience)if experience  else None,
            'Location':location,
            'Job_Title':job_title,
            'Age':int(age) if age else None,
             'Gender':Gender,
            }
        df = pd.DataFrame([data])
        df_1 = df.copy()
        st.table(df)

        df_G = pd.get_dummies(df,dtype=int,columns=['Education','Location','Job_Title','Gender'])

        df_model= df_G.reindex(columns=template.columns, fill_value=0)
        features = df_model.values
        prediction = model.predict(features)
        st.markdown('')
        with st.spinner('wait a moment please..'):
             time.sleep(5)
             st.success('done!')

        with st.container(border=True):
             st.subheader(f"your salary expection needs to be around {round(prediction[0],2)} $")      
if show_intro :
    st.markdown(intro_markdown)

        


    
    
    



    
