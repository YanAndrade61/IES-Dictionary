import streamlit as st
import streamlit_authenticator as stauth
import yaml
import os


#----Authentication User------#
with open('credential.yaml','r') as fp:
    config = yaml.safe_load(fp)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, auth_status, username = authenticator.login('Login','sidebar')

if auth_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*')
elif auth_status == False:
    st.sidebar.error('Username/password is incorrect')

st.sidebar.write('---')

#------------APP--------------#

# Layout sidebar + main page
st.header('Dicionario engenharia de software :book:')
st.write("""
    Pagina dedicada a criação de um dicionario com os 
    principais termos sobre **Engenharia de Software**.
""")
st.write('---')

stbar = st.sidebar
stbar.header('Ferramentas do dicionário')

# Load dictionary data
with open('dictionary.yaml','r') as fp:
    data = yaml.safe_load(fp)
if data == None: data ={}

# Search for terms in data
stbar.subheader('Pesquisar termos')
sorted_terms = sorted(data.keys())
select_terms = stbar.multiselect('Termos',sorted_terms, sorted_terms)
# stbar.write('---')

# Insert a new term only for registered user
if auth_status:
    stbar.subheader('Inserir termo')
    term_name = stbar.text_input('Nome')
    term_mean = stbar.text_area('Significado')
    if stbar.button('Inserir'):
        data[term_name.lower()] = term_mean
        with open('dictionary.yaml','w') as fp:
            yaml.dump(data,fp)
        os.system('git commit -a "Update terms" | git push')

# Display selected terms
st.subheader('Significado dos termos selecionados')
for term in select_terms:
    st.write(f"* **{term.upper()}**: {data[term]}")
