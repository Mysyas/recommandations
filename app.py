import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def getRecommandation(name,gender,aim,medical):
    list_=pickle.load(open('user_dataset.pkl','rb'))
    lr=pd.DataFrame(columns=['Gender','Fitness Goal','Medical History'],data=[[gender,aim,medical]])
    list_=pd.concat([list_,lr],axis=0,ignore_index=True)
    vectorizer=TfidfVectorizer()
    combined_features=vectorizer.fit_transform(list_['Gender']+" "+list_['Fitness Goal']+" "+list_['Medical History'])
    similarity=cosine_similarity(combined_features)
    st.session_state.name=name
    foods=[]
    recommanded=[]
    
    plats=pickle.load(open('plats.pkl','rb'))
    
    index=list_.index[(list_['Gender']==gender)&(list_['Fitness Goal']==aim)&(list_['Medical History']==medical)]
    for i,_ in sorted(list(enumerate(similarity[index[0]])), reverse=True,key=lambda v: v[1])[0:5]:
        foods.extend(plats[plats['id']== list_.iloc[i,5]]['Recipe_name'])
        recommanded.append(list_.iloc[i,4])
    return list(set(recommanded)),list(set(foods))
        
    
if 'name' not in st.session_state:
    st.session_state.name=""
if 'diet_recommended' not in st.session_state:
    st.session_state.diet_recommended=""
if 'result' not in st.session_state:
    st.session_state.result=""

st.set_page_config(layout="wide")
st.header('Recommandation de plats')
st.markdown('<p id="info"><strong>Remplissez dument les informations</strong></p>',unsafe_allow_html=True)
with st.form('diet'):
    st.write("<strong>Nom d'utilisateur</strong>",unsafe_allow_html=True)
    user=st.text_input('')
    col1,col2 = st.columns([1,2],gap='medium')
    with col1:
        st.write('<strong>Genre <i style="color: red">*</i></strong>',unsafe_allow_html=True)
        gender=st.selectbox('Genre',options=['Masculin','Féminin'])
    with col2:
        st.write('<strong>Objectif <i style="color: red">*</i></strong>',unsafe_allow_html=True)
        aim=st.selectbox('Objectif',options=['Perte de poids','Prise de poids','Prise de masse'])
    
    st.write('<strong>Antécédent médical <i style="color: red">*</i></strong>',unsafe_allow_html=True)
    medical=st.selectbox('Antécédent médical',options=['Aucun','Diabétique','Gout'])
    
    btn=st.form_submit_button('Recommander')
    if btn:
        gender_val='M' if gender=="Masculin" else 'F'
        aim_val='weight gain' if aim=='Prise de poids' else 'weight loss' if aim=='Perte de poids' else 'muscle building'
        medical_val= 'None' if medical=='Aucun' else 'Diabetes' if medical=='Diabétique' else 'Gout'
        st.session_state.diet_recommended, st.session_state.result= getRecommandation(user,gender_val,aim_val,medical_val)
if 'name' in st.session_state:
    st.write(f'Salut, nous proposons à  {st.session_state.name} :')

col1,col2= st.columns([1,1])
with col1:
    st.write('Régimes recommandés')
    for diet in st.session_state.diet_recommended:
        st.write(f'<li>{diet}</li>',unsafe_allow_html=True)
    if len(st.session_state.diet_recommended)==0:
        st.write("Aucune proposition de régime n'est actuellement disponible")

with col2:
    st.write('Plats recommandés')
    for res in st.session_state.result:
        st.write(f'<li>{res}</li>',unsafe_allow_html=True)
    if len(st.session_state.diet_recommended)==0:
        st.write("Aucune proposition de régime n'est actuellement disponible")
    
        
