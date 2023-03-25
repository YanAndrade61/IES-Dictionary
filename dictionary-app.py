import streamlit as st
import yaml

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
stbar.write('---')

# Insert a new term
stbar.subheader('Inserir termo')
term_name = stbar.text_input('Nome')
term_mean = stbar.text_area('Significado')
if stbar.button('Inserir'):
    data[term_name.lower()] = term_mean
    with open('dictionary.yaml','w') as fp:
        yaml.dump(data,fp)

# Display selected terms
st.subheader('Significado dos termos selecionados')
for term in select_terms:
    st.write(f"* **{term.upper()}**: {data[term]}")
