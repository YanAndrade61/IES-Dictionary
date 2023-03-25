import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import ssl

#-----Connection to google sheet------#

# Disable certificate verification (Not necessary always)
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets.gcp_service_account, scopes = scope)

client = Client(scope=scope,creds=credentials)
spreadsheetname = "IES-Dictionary"
spread = Spread(spreadsheetname,client = client)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Functions 
@st.cache_data()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['termo','significado']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)

#------Authentication User------#
credentials = {
    "usernames": st.secrets.config.credentials.usernames
}
authenticator = stauth.Authenticate(
    credentials,
    st.secrets.config.cookie.name,
    st.secrets.config.cookie.key,
    st.secrets.config.cookie.expiry_days,
    st.secrets.config.preauthorized
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
data = load_the_spreadsheet('Dictionary')

# Search for terms in data
stbar.subheader('Pesquisar termos')
sorted_terms = sorted(list(data['termo']))
select_terms = stbar.multiselect('Termos',sorted_terms, sorted_terms)
# stbar.write('---')

# Insert a new term only for registered user
if auth_status:
    stbar.subheader('Inserir termo')
    term_name = stbar.text_input('Nome')
    term_mean = stbar.text_area('Significado')
    if stbar.button('Inserir'):
        term_df = pd.DataFrame({
            'termo': [term_name],
            'significado' :  [term_mean]}
        ) 
        new_df = data.append(term_df,ignore_index=True)
        update_the_spreadsheet('Dictionary',new_df)

# Display selected terms
st.subheader('Significado dos termos selecionados')
for term, mean in data[data['termo'].isin(select_terms)].values:
    st.write(f"* **{term.upper()}**: {mean}")
