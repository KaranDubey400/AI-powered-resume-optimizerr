import streamlit as st
from streamlit_option_menu import option_menu
from Frontend.home_page import home as HP
from Frontend.instruction_page import Instruction as Ins
from Frontend.ats_page import Ats_page as ats
from Frontend.about import About_section as Ab_sec

# File Path
image_path = r"assets/logo/grey.png"

def main():
    # Hide the Streamlit menu and footer
    st.markdown("""
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        </style>
        """, unsafe_allow_html=True)

    # Sidebar Logo (loads only once)
    if "sidebar_image_loaded" not in st.session_state:
        st.session_state["sidebar_image_loaded"] = True
        with st.sidebar:
            st.image(image_path, use_column_width=True)

    # Navigation Menu
    selected_main = option_menu(None, ["Home", "Instruction", "ATS Analyzer", "About"],
                                icons=['house', 'folder', 'cloud', 'person'],
                                orientation="horizontal", key='menu_4')

    if selected_main == "Home":
        HP.home_page()
    elif selected_main == "Instruction":
        Ins.instruction()
    elif selected_main == "ATS Analyzer":
        ats.resume_parser()
    elif selected_main == "About":
        Ab_sec.About_Section()

    # Footer
    footer_html = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #C8A1E0;
            display:flex;
            flex-direction: column;
            align-items:center;
            padding: 10px;
        }
        .footer b {
            color: #33372C;
            font-size: 18px;
        }
    </style>
    <div class="footer">
        <b>Craftify</b>
        <p>karn</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
