import streamlit as st
import streamlit_authenticator as stauth
#import appfake
import appfake1
#import appfake2
#import appfake3
#import appfake4
#import appfake5
#import appfake6
#import appfake7
#import appfake5_version2
#import appfake6_version2
from PIL import Image
import text
#import amsServices1
#import amsServices2
import appfakepred
import appfakechecker
import appfakecheckermanual
import appfakecheckertext
import appfakecheckermanualtext
import appfakenlptext
#import apptoxicity
#import appaitdetectors
#import appassociation
#import appassociation_analytics
#import appassociation_filtering
#import appassociation_advanced_filtering
# import apptest
# from multiapp import MultiApp

image1 = Image.open('starlight.png')
# image_resized = image.resize((370, 370))#, Image.ANTIALIAS)

st.set_page_config(page_title='Meta-Detection',page_icon=image1)
image = Image.open('starlight.png')
# image_resized = image.resize((370, 370))#, Image.ANTIALIAS)
st.sidebar.image(image)
# st.sidebar.image("/home/nikospps/Projects_Codes_Development/metaverification_algorithm_NEW/anal.png", use_column_width=True)

# Hide hamburger (top right corner) and “Made with Streamlit” footer
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# names = ['edaskalakis','nikospps','talexakis']
# usernames = ['edaskalakis','nikospps','talexakis']
# passwords = ['giorgis','np220287npps','t@lexakis']

# hashed_passwords = stauth.Hasher(passwords).generate()

# authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
#                                     'some_cookie_name','some_signature_key',cookie_expiry_days=30)


# hashed_passwords = stauth.Hasher(['starlight_user1', 'St@rlight!']).generate() #USED TO Generate Hashes

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#name, authentication_status, username = authenticator.login('Login', 'main')#sidebar
name, authentication_status, username = authenticator.login('main') #updated command


if authentication_status:
    st.write(f'Welcome *{name}*')
    PAGES = {
        'URL Content Insights': text,
        'URL NLP Profiler': appfake1,
        'NLP-Based Text Analysis': appfakenlptext,
        'URL Trustworthiness Checker': appfakechecker,
        'URL Trustworthiness M-Checker': appfakecheckermanual,
        'URL Trustworthiness Analysis': appfakepred,
        'Text Trustworthiness Checker': appfakecheckertext,
        'Text Trustworthiness M-Checker': appfakecheckermanualtext,
#        'Association Rule Mining': appassociation,
#        'Association Rule Mining Analytics': appassociation_analytics,
#        'Association Rule Mining Filtering': appassociation_filtering,
#        'Association Rule Mining Ad-Filtering': appassociation_advanced_filtering,
        #'ICCS Text Trustworthiness Analysis': appfakepred,
#        'AMS Analysis Services': amsServices1,
        #'AMS Sentiment Analysis': appfake2,
        #'AMS ClickBait': appfake3,
        #'AMS Spam-SMS Detection': appfake7,
        #'AMS Bot Detector': appfake4,
#        'AMS WordCloud-TextNetwork': amsServices2,
        #'AMS WordCloud': appfake5_version2,
        #'AMS TextNetwork': appfake6_version2,
#        'AIT Toxicity-Geolocation Models': apptoxicity,
#        'AIT Detection Models': appaitdetectors
    }
    # st.sidebar.title('Navigation')
    # st.write('Welcome to Metaverification API. Please Enter your Username and Password.')
    selection = st.sidebar.radio("", list(PAGES.keys()))
    page = PAGES[selection]
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    # st.image(image_resized)
    page.app()
    # st.title('Some content')
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
# name, authentication_status = authenticator.login('Metaverification API','sidebar')

# st.warning('Welcome to Metaverification API. Please Enter your Username and Password.')
# st.image(image_resized)
#
# if st.session_state['authentication_status']:
#     #logs1 = mongodb.create_coll(dbcollection='login')
#     #message = {'username': (st.session_state['name']), 'timestamp': mongodb.latesttimestasmp(), 'cet': 0}
#     #mongodb.write_mongo(logs1, message)
#     st.write('Welcome *%s*' % (st.session_state['name']))
#     PAGES = {
#         'Insert User Evaluation for a URL': app4,
#         'Topic Definition': app1b,
#         # 'Check URL for Previous Recomputation': app,
#         "Verification Services URL Evaluation": app1a,
#         'URL Evaluation History': app5,
#         # "Evaluate Test URLs": app1,
#         "Verification Services’ Weights History": app2,
#         # 'Visualization of Initial Weights': app3,
#         # 'Visualize Computed Weights': app6,
#         'Evaluate Text': app7,
#         'Text Evaluation History': app8,
#         'Login History': login,
#         'User Input Evaluation History': userinput
#     }
#     # st.sidebar.title('Navigation')
#     # st.write('Welcome to Metaverification API. Please Enter your Username and Password.')
#     selection = st.sidebar.radio("", list(PAGES.keys()))
#     page = PAGES[selection]
#     # st.image(image_resized)
#     page.app()
# elif st.session_state['authentication_status'] == False:
#     st.error('Username/password is incorrect')
#     # st.image(image)#, caption='Sunrise by the mountains')
# elif st.session_state['authentication_status'] == None:
#     st.warning('Welcome to Metaverification Toolkit. Please Enter your Username and Password.')
#     # st.image(image_resized)  # , caption='Sunrise by the mountains')

#https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4
#https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
#https://github.com/mkhorasani/Streamlit-Authenticator

## You can then use the returned name and authentication status to allow your verified user to proceed to any restricted content.
# if authentication_status:
#     st.write('Welcome *%s*' % (name))
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

## Should you require access to the persistent name and authentication status variables, you may retrieve them through
## Streamlit’s session state using st.session_state[‘name’] and st.session_state[‘authentication_status’]. This way you can
## use Streamlit-Authenticator to authenticate users across multiple pages.
# if st.session_state['authentication_status']:
#     st.write('Welcome *%s*' % (st.session_state['name']))
#     st.title('Some content')
# elif st.session_state['authentication_status'] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status'] == None:
#     st.warning('Please enter your username and password')


