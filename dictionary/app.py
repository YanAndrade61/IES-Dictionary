from authentication import authenticate_user
from googleSheet import get_google_client, get_spreadsheet
import streamlit as st
import pandas as pd


stbar = st.sidebar
# -----Connection to google sheet------#
spreadsheet = {"name": "IES-Dictionary", "page": "Dictionary"}
client = get_google_client(gcp_account=st.secrets.gcp_service_account)
spread = get_spreadsheet(spreadsheetname=spreadsheet["name"], client=client)
data_df = spread.sheet_to_df(index=0, sheet=spreadsheet["page"])
data_dict = data_df.set_index("termo").to_dict("index")

# ------Authentication User------#
credentials = {"usernames": st.secrets.config.credentials.usernames}

name, auth_stats = authenticate_user(
    credentials,
    st.secrets.config.cookie,
    st.secrets.config.preauthorized,
    "sidebar",
)
if auth_stats:
    stbar.write(f"Welcome *{name}*")
elif auth_stats is False:
    stbar.error("Username/password is incorrect")

st.sidebar.write("---")

# ------------APP--------------#
st.header("Dicionario engenharia de software :book:")
st.write(
    """
    Pagina dedicada a criação de um dicionario com os 
    principais termos sobre **Engenharia de Software**.
    """
)
st.write("---")

# Search for terms in data
sorted_terms = sorted(list(data_dict.keys()))
select_terms = st.multiselect("Termos", sorted_terms, sorted_terms)

# Insert a new term only for registered user
if auth_stats:
    stbar.header("Ferramentas do usuário")
    stbar.subheader("Inserir termo")
    term_name = stbar.text_input("Nome")
    term_mean = stbar.text_area("Significado")
    if stbar.button("Inserir"):
        term_df = pd.DataFrame(
            {"termo": [term_name.lower()], "significado": [term_mean]}
        )
        if term_name.lower() in data_dict.keys():
            data_df = data_df[data_df["termo"] != term_name.lower()]

        data_df = data_df.append(term_df, ignore_index=True).sort_values(by="termo")
        spread.df_to_sheet(data_df, sheet=spreadsheet["page"], index=False)

# Display selected terms
st.subheader("Significado dos termos selecionados")
for term in select_terms:
    st.write(f"* **{term.upper()}**: {data_dict[term]['significado']}")
