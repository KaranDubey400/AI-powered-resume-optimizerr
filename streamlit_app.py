# Frontend Framework
import streamlit as st
from streamlit_option_menu import option_menu

# From files
from Frontend.home_page import home as HP 
from Frontend.instruction_page import Instruction as Ins
from Frontend.ats_page import Ats_page as ats

from Frontend.about import About_section as Ab_sec

# File Path
image_path = r"assets/logo/grey.png"

def main():
    
    hide_menu = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        </style>
        """
    st.markdown(hide_menu, unsafe_allow_html=True)
    
    if st.session_state.get('switch_button', False):
        st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 5
        manual_select = st.session_state['menu_option']
    else:
        manual_select = None
    
    selected_main = option_menu( None , ["Home","Instruction","ATS Analyzer","About"],
        icons=[ 'house','folder','cloud', 'person','gear'], 
        orientation="horizontal", manual_select=manual_select, key='menu_4')

    with st.sidebar:
        st.image(image_path) 

    if selected_main == "Home":
        HP.home_page()
    if selected_main == "Instruction":
        Ins.instruction()
    elif selected_main == "ATS Analyzer":
        ats.resume_parser()
   
    elif selected_main == "About":
        Ab_sec.About_Section()

    # Create an empty space to center the button horizontally
    col1, col2, col3 = st.columns([7, 5, 5])

    # Place the button inside the middle column
    with col2:
        st.button(f"Next Page", key='switch_button')
    # Footer note
    footer_html = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: -9px;
            width: 100%;
            background-color: #C8A1E0;
            display:flex;
            flex-direction: column;
            align-items:center;
        }
        .footer b{
            color: #33372C;
            font-size: 20px;
        }
    </style>
    <div class="footer">
        <b>Craftify</b>
        <p>karn </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
