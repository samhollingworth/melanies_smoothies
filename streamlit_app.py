# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")

# Get secrets from Streamlit Cloud Secrets
conn_info = st.secrets["connections"]["snowflake"]

# Establish Snowpark Session
session = Session.builder.configs(conn_info).create()

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
fruit_options = my_dataframe['FRUIT_NAME'].tolist()  # Convert to a list

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Display fruit options for selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    fruit_options, 
    max_selections=5
)

if ingredients_list:
    st.write("Ingredients Selected:", ingredients_list)

    # Convert selected ingredients to a comma-separated string
    ingredients_string = ', '.join(ingredients_list)

    # Prepare the SQL Insert Statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Failed to insert order: {e}")

# Close Snowflake session
session.close()
