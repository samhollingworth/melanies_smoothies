# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customise your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake connection parameters
connection_parameters = {
    "account": "EODBGZC-KRB90497",
    "user": "hollingworthsam2000",
    "password": "Westend11Danielle30",  # Consider using Streamlit secrets management for sensitive info
    "role": "PUBLIC",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

# Establishing Snowpark session
session = Session.builder.configs(connection_parameters).create()

# Fetching available fruits
my_dataframe = session.table("fruit_options").select(col('FRUIT_NAME')).to_pandas()
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ", ".join(ingredients_list)

    # Display the insert statement for debugging purposes
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, customer_name)
                         VALUES ('{ingredients_string}', '{name_on_order}');"""
    
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()  # Execute the SQL statement using Snowpark session
        st.success('Your Smoothie is ordered!', icon="✅")

# Close the session when done
session.close()
