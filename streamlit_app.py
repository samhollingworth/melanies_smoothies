# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")

# Get secrets from Streamlit Cloud Secrets
try:
    conn_info = st.secrets["connections"]["snowflake"]
except Exception as e:
    st.error("Failed to load connection information from secrets. Please check your Streamlit Cloud secrets configuration.")
    st.stop()

# Establish Snowpark Session
try:
    session = Session.builder.configs(conn_info).create()
    st.success("✅ Successfully connected to Snowflake.")
except Exception as e:
    st.error(f"❌ Failed to connect to Snowflake: {e}")
    st.stop()

# Load fruit options from Snowflake
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
    fruit_options = my_dataframe['FRUIT_NAME'].tolist()  # Convert to a list
except Exception as e:
    st.error(f"❌ Failed to load fruit options from Snowflake: {e}")
    session.close()
    st.stop()

# Display text input for name
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

    # Prepare the SQL Insert Statement
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if not name_on_order.strip():
            st.error("Please enter a name for your order before submitting.")
        else:
            try:
                # Use parameterized query to prevent SQL injection
                session.table("smoothies.public.orders").insert([{"ingredients": ', '.join(ingredients_list), "name_on_order": name_on_order}])
                st.success('✅ Your Smoothie is ordered!', icon="✅")
            except Exception as e:
                st.error(f"❌ Failed to insert order: {e}")

# Close Snowflake session gracefully
session.close()
