# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title("🥤 Customise Your Smoothie 🥤")
st.write(
  """Choose the fruits you want in you custom Smoothie.
  """)

import streamlit as st

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on the smoothie will be", name_on_order)

import streamlit as st

# option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#    )

#st.write("Your favorite fruit is:", option)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    "Choose up to 5 ingredients"
    ,my_dataframe
    ,max_selections=5
)

if ingredients_List:
    #st.write(ingredients_List)
    #st.text(ingredients_List)
    ingredients_string=''

    for fruit_chosen in ingredients_List:
        ingredients_string+=fruit_chosen+' '

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

   #st.write(my_insert_stmt)
   #st.stop()

    time_to_insert = st.button("Submit Order")

    #st.write(my_insert_stmt)

    if time_to_insert:
       session.sql(my_insert_stmt).collect()

       st.success('Your Smoothie is ordered!', icon="✅")

    






