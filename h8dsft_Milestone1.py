import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from scipy import stats


st.set_page_config(
    page_title="Pascalis Farrel - Batch 008 - Milestone 1",
    page_icon= "😺",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Supermarket Sales"
    }
)

df = pd.read_csv("supermarket_sales - Sheet1.csv")

page = st.sidebar.selectbox("Select a Page: ", ['Data Visualization', 'Hypothesis Testing'])

if page == 'Data Visualization':
    st.title('Supermarket Sales')
    st.write('This is a data visualization of supermarket sales')

    #Data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)
    
    #SelectBox
    list_columns= ['Average Gross Income Per Product Line', 'Average Gross Income Per City']
    pilih = st.selectbox('Pilih kolom', list_columns)

    
    if pilih == 'Average Gross Income Per Product Line':
        st.subheader('Average Gross Income Per Product Line')
        fig1,ax1 = plt.subplots()

        df.groupby('Product line').mean()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax1)

        ax1.set_title('Average Gross Income Per Product Line') 
        ax1.set_xlabel('Product line') 
        ax1.set_ylabel('gross income') 
        st.pyplot(fig1,ax1)
    else:
        st.subheader('Average Gross Income Per City')
        fig4,ax4 = plt.subplots()

        df.groupby('City').mean()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax4)

        ax4.set_title('Average Gross Income Per City') 
        ax4.set_xlabel('City') 
        ax4.set_ylabel('gross income') 
        st.pyplot(fig4,ax4)

    #3
    

    fig2,ax2 = plt.subplots()

    df.groupby('Customer type').mean()['Quantity'].sort_values(ascending=False).plot(kind='bar',ax=ax2)

    ax2.set_title('Average Sales based on Customer type') 
    ax2.set_xlabel('Customer type') 
    ax2.set_ylabel('Quantity') 
    

    #4
    
    
    fig3,ax3 = plt.subplots()

    df.groupby('Customer type').mean()['Rating'].sort_values(ascending=False).plot(kind='bar',ax=ax3)

    ax3.set_title('Average Ratings based by Customer type') 
    ax3.set_xlabel('Customer type') 
    ax3.set_ylabel('Rating') 
    


    #RadioButton
    kolom = st.radio(
    'Pilih kolom :',
    ('Average Sales based on Customer type', 'Average Ratings based by Customer type'))
    if kolom =='Average Sales based on Customer type':
        st.subheader('Average Sales based on Customer type')
        st.pyplot(fig2,ax2)
    else:
        st.subheader('Average Ratings based by Customer type')
        st.pyplot(fig3,ax3)

    #Visualisasi 1
    branch = st.selectbox('Select a Branch', ['A','B','C'])
    st.write('Gross Income based on Payment Method')
    branch_c = alt.Chart(df.loc[df.Branch == branch].groupby(['Branch', 'Payment']). \
                        agg({'gross income': 'sum'}).reset_index()).mark_line().encode(
    x='Payment',
    y='gross income'
                        )
    st.altair_chart(branch_c, use_container_width=True)

    #Visualisasi 2
    gender = st.selectbox('Select a Gender', ['Male','Female'])
    st.write('Sales based on City')
    gender_c = alt.Chart(df.loc[df.Gender == gender].groupby(['Gender', 'City']). \
                        agg({'Quantity': 'sum'}).reset_index()).mark_line().encode(
    x='City',
    y='Quantity'
                        )
    st.altair_chart(gender_c, use_container_width=True)



else:
    st.title('Hypothesis Testing')
    st.write('Berdasarkan dataset, berikut merupakan hasil dari test hypothesis yang dilakukan')

    df = pd.read_csv('supermarket_sales - Sheet1.csv')

    st.subheader('Hypothesis Testing T-Test 2 Sample 2 Tailed')
    st.write('H0 : Fashion Accessories Sales mean == Food and beverages mean')
    st.write('H1 : Fashion Accessories Sales mean != Food and beverages mean')

    fashion = df[df['Product line'] == 'Fashion accessories']
    food = df[df['Product line'] == 'Food and beverages']

    t_stat, p_val = stats.ttest_ind(fashion['Quantity'], food['Quantity'])
    st.write('P-value:',p_val)
    st.write('t-statistics:',t_stat)

    fig_hypo = plt.figure(figsize=(10,4))

    fashion_pop = np.random.normal(fashion['Quantity'].mean(),fashion['Quantity'].std(),10000)
    food_pop = np.random.normal(food['Quantity'].mean(),food['Quantity'].std(),10000)


    ci = stats.norm.interval(0.95, fashion['Quantity'].mean(), fashion['Quantity'].std())

    sns.distplot(fashion_pop, label='Fashion Accessories Sales',color='blue')
    sns.distplot(food_pop, label='Food and beverages Sales',color='red')

    plt.axvline(fashion['Quantity'].mean(), color='blue', linewidth=2, label='Fashion Accessories Sales mean')
    plt.axvline(food['Quantity'].mean(), color='red',  linewidth=2, label='Food and beverages mean')

    plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
    plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')

    plt.axvline(fashion_pop.mean()+t_stat*food_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
    plt.axvline(fashion_pop.mean()-t_stat*food_pop.std(), color='black', linestyle='dashed', linewidth=2)

    plt.legend()
    
    st.pyplot(fig_hypo)

    st.write('Dikarenakan confidence interval pada T-Test 2 Sample 2 Tailed adalah 0.95, maka diperoleh nilai p value sebesar 0.20612360348103295 dimana nilai tersebut diatas nilai alpha. Dapat disimpulkan bahwa H0 yang diterima, bahwa nilai Average pada Fashion Accessories Sales yaitu sama dengan Average dari Food and beverages Sales.')
