import streamlit as st
import pandas as pd
import paper_extraction as pe
from itertools import chain

@st.cache(allow_output_mutation=True)

def upload_data():
    df = pd.read_excel("scopus_its_2.xls")
    df = df.applymap(str)
    return df

def tkd(df):
    with st.spinner('Wait for it...'):
        df['TKD'] = df.Title.apply(lambda x: pe.paper().tkd_judul(x))
    return df

def term(df):
    with st.spinner('Wait for it...'):
        df['Term'] = df.Title.apply(lambda x: pe.paper().nphrase(x))
    return df

def dept(df):
    with st.spinner('Wait for it...'):
        df['Department'] = df.Affiliations.apply(lambda x: pe.paper().dept(x))
    return df

def pie_chart(df,col):
    df_dt = pd.DataFrame(df[col].value_counts())
    df_dt['index1'] = df_dt.index
    df_dt.columns = ['Number', col]
    import plotly.express as px
    fig = px.pie(df_dt, values='Number', names=col, color_discrete_sequence=px.colors.sequential.Burg, width=500, height=500)
    return fig

def bar_chart(df,col):
    df_dt = pd.DataFrame(df[col].value_counts())
    df_dt['index1'] = df_dt.index
    df_dt.columns = ['Total Term', col]
    import plotly.express as px
    fig = px.bar(df_dt, y='Total Term', x=col, color_discrete_sequence=px.colors.sequential.Burg)
    return fig

def tkd_term_freq(df,tkd=None):
    df_tkd_term = df[['TKD','Term']]
    if tkd != None: df_tkd_term = df_tkd_term.loc[df_tkd_term['TKD'] == tkd].reset_index(drop=True)
    df_tkd_term = list(chain.from_iterable(df_tkd_term.Term.tolist()))
    df_tkd_term = pd.DataFrame(pd.Series(df_tkd_term).value_counts())
    df_tkd_term['index1'] = df_tkd_term.index
    df_tkd_term.columns = ['Frequency', 'Term']
    df_tkd_term = df_tkd_term[['Term', 'Frequency']]
    df_tkd_term = df_tkd_term.reset_index(drop=True)
    return df_tkd_term

def term_years(df):
    df_term_years=pd.DataFrame()
    df_term_year_sel=pd.DataFrame()
    df_year = df[['Term','Year']]
    years = list(set(df.Year.to_list()))
    for y in years:
        df_year_sel = df_year.loc[df_year['Year'] == y]
        list_term = list(chain.from_iterable(df_year_sel.Term.tolist()))
        df_term_sel = pd.DataFrame(pd.Series(list_term))
        year=[]
        for a in range(len(list_term)):
            year.append(y)
        year = pd.DataFrame(pd.Series(year))
        df_term_year_sel = pd.concat([year,df_term_sel],axis=1)
        df_term_year_sel.columns = ['Year','Term']
        df_term_years = pd.concat([df_term_year_sel,df_term_years])
    df_term_years = df_term_years.drop_duplicates(subset='Term',keep='first')
    return df_term_years

def visual_df(df_dept,term_selected=False):

    if term_selected == False:
        st.subheader("All Research Term")
        df_all = tkd_term_freq(df_dept)
        st.dataframe(df_all)
        st.info('Total Term : ' + str(len(df_all.index)))
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("All Research Term")
            df_all = tkd_term_freq(df_dept)
            df_all = df_all[["Term","Frequency"]]
            st.dataframe(df_all)
            st.info('Total Term : ' + str(len(df_all.index)))
        with col2:
            st.subheader("Contain selected Term")
            df_term_selected = search_term_df(df_all,term_selected)
            df_term_selected = df_term_selected[["Term","Frequency"]]
            st.dataframe(df_term_selected)
            st.info('Total Selected Term : ' + str(len(df_term_selected.index)))       

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("TKD Category")
        st.plotly_chart(pie_chart(df_dept,'TKD'))
    with col2:
        st.subheader("Document Type")
        st.plotly_chart(pie_chart(df_dept,'Document Type'))
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Basic TKD Category")
        df_basic = tkd_term_freq(df_dept,'Basic')
        st.dataframe(df_basic)
        st.info('Total Basic Term : ' + str(len(df_basic.index)))
    with col2:
        st.subheader("Implementation TKD Category")
        df_im = tkd_term_freq(df_dept,'Implementation')
        st.dataframe(df_im)
        st.info('Total Implementation Term : ' + str(len(df_im.index)))

# search Term in title
def search_term(title,term):
    title = str(title).replace("[",'').replace("]",'').replace('"','')
    term = term.rstrip().strip()
    if term in title:
        a=1
    else: a=0
    return a

# dataframe search by Term
def search_term_df(df,term):
    df['search'] = df.Term.apply(lambda x: search_term(x,term))
    df = df.loc[df.search == 1].reset_index(drop=True)
    return df



st.set_page_config(page_title='ITS SCOPUS', layout="wide")
st.title("ITS SCOPUS")
if 'data' not in st.session_state:
    df = upload_data()
    # df = df[['Authors','Year','Affiliations','Document Type','Abstract','Title','Link']]
    st.session_state.data = df
df_data = st.session_state.data
df_data = df_data[['Authors','Year','Affiliations','Document Type','Abstract','Title','Link']]
st.dataframe(df)
st.info('Total Artitle ' + str(len(df.index)))



if "button" not in st.session_state:
    st.session_state.button = False
    st.session_state.tkdbutton = False
    st.session_state.termbutton = False
    st.session_state.deptbutton = False
    st.session_state.visbutton = False

#___figure out tkd category--------------------
st.subheader("Artitle TKD Category")

if st.button('Run TKD Category') or st.session_state.tkdbutton:
    if "tkd" not in st.session_state:
        # st.session_state.tkd = tkd(df)
        st.session_state.tkd = st.session_state.data
    df_tkd = st.session_state.tkd
    df_tkd = df_tkd[['TKD','Authors','Year','Affiliations','Document Type','Abstract','Title','Link']]
    st.dataframe(df_tkd)
    st.session_state.tkdbutton = True

#___Extract Research Terms-----------------------   
if st.session_state.tkdbutton:
    st.subheader("Research Terms")

    if st.button('Extract Research Terms') or st.session_state.termbutton:
        if "term" not in st.session_state:
            # st.session_state.term = term(st.session_state.tkd)
            st.session_state.term = st.session_state.data
        df_term = st.session_state.term
        df_term = df_term[['TKD','Authors','Year','Affiliations','Document Type','Abstract','Title','Term','Link']]
        st.dataframe(df_term)
        st.session_state.termbutton = True

#___Department------------------------------------ 
if st.session_state.termbutton:
    st.subheader("Department")

    if st.button('Run') or st.session_state.deptbutton:
        if "dept" not in st.session_state:
            # st.session_state.dept = dept(st.session_state.term)
            st.session_state.dept = st.session_state.data
        df_dept = st.session_state.dept
        df_dept = df_dept[['TKD','Authors','Year','Affiliations','Document Type','Abstract','Title','Term','Department','Link']]
        st.dataframe(df_dept)
        st.session_state.deptbutton = True
        df_dept['Term'] = df_dept.Term.apply(lambda x: x.replace("[","").replace("]","").replace("'","").split(","))

if st.session_state.deptbutton:

    st.title("")
    st.title("ITS SCOPUS VISUALIZATION")

    selected = st.selectbox(
     'Please select how do you want to visualize data:',
     ('','Main Visualize','By Department','By Research Term'))

    if selected == 'Main Visualize':
        visual_df(df_dept)

    if selected == 'By Department':
        dept_sel = ['']+str(set(df_dept.Department.tolist())).replace("{","").replace("}","").replace("'","").strip().rstrip().split(',')
        dept_sel = tuple(dept_sel) #tuple selection
        selected_dept = st.selectbox(
        'Please select Department:',
        dept_sel)
        selected_dept = str(selected_dept)
        selected_dept = selected_dept.strip().rstrip()
        df_dept_sel = df_dept
        df_dept_sel = df_dept_sel.loc[df_dept_sel.Department == selected_dept].reset_index(drop=True)
        df_dept_sel = df_dept_sel[['TKD','Authors','Year','Affiliations','Document Type','Abstract','Title','Term','Department','Link']]
        
        df_term_years = term_years(df_dept_sel)

        if selected_dept: 
            st.subheader(str(selected_dept)+' Department Scopus') 
            st.dataframe(df_dept_sel)
            st.info('Total Artitle ' + str(len(df_dept_sel.index)))

            col1, col2 = st.columns([3,2])
            with col1:
                st.plotly_chart(bar_chart(df_term_years,'Year'))
            with col2:
                st.header("")
                st.header("")
                st.dataframe(df_term_years)
                st.info('Total Term ' + str(len(df_term_years.index)))
                
            visual_df(df_dept_sel)
        else: st.warning("Please select Department")
            

    if selected == 'By Research Term':
        df_re = list(chain.from_iterable(df_dept.Term.tolist()))
        re_sel = ['']+str(set(df_re)).replace("{","").replace("}","").replace("'","").replace('"',"").strip().rstrip().split(',')
        re_sel = tuple(re_sel)
        selected_re = st.selectbox(
        'Please select Term:',
        re_sel)
        df_search = search_term_df(df_dept,selected_re)
        df_search = df_search[['TKD','Authors','Year','Affiliations','Document Type','Abstract','Title','Term','Department','Link']]
        
        if selected_re:
            st.subheader(str(selected_re)+' Term Selected')
            st.dataframe(df_search)
            st.info('Total Artitle ' + str(len(df_search.index)))
            visual_df(df_search,selected_re)
        else: st.warning("Please select Term")