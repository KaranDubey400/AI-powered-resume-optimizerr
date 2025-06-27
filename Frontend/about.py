import streamlit as st



class About_section():
    def About_Section():
        
        st.markdown("<h1 style='color:  #F05A7E;'>About Craftify</h1>", unsafe_allow_html=True)
        st.write("It is an AI-powered platform designed to assist job seekers in optimizing their resumes for Applicant Tracking Systems (ATS) and tailoring them for specific job descriptions. It also includes features for job searching and provides personalized job suggestions.")

        # Key Features
        st.markdown("<h2 style='color:  #F05A7E;'>Key Features:</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:  #F05A7E;'> Resume Analyzer (Resume Parser):</h3>", unsafe_allow_html=True)
        st.write("ATS Optimization: Users can scan their resumes against ATS systems to receive feedback and improve their chances of getting noticed by recruiters.")
        st.write("Resume Analysis: The platform provides semantic analysis and keyword extraction to ensure resumes highlight key skills and experiences.")
        st.write("Output Styling: Utilizes HTML and CSS to present extracted information in a user-friendly format.Includes tooltips and explanations for better user guidance.")
        st.markdown("---")
        st.markdown("<h3 style='color:  #F05A7E;'> Resume Optimization with Keyword Integration: </h3>", unsafe_allow_html=True)
        st.write("Craftify provides strategic guidance on incorporating essential keywords into resumes. These recommendations are tailored to align with industry trends and job-specific requirements, ensuring users create highly optimized profiles that capture recruiters' attention. Future updates will introduce step-by-step keyword integration tools, making the optimization process even more seamless and user-friendly.")
         
        st.markdown("---")
        # How It Works
        st.markdown("<h2 style='color:  #F05A7E;'>How It Works:</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:  #F05A7E;'>1. Upload Resume & Job Description:</h3>", unsafe_allow_html=True)
        st.write("   Users seamlessly upload their resumes and target job descriptions to Craftify. ")
        st.markdown("<h3 style='color:  #F05A7E;'>2. ATS Analysis:</h3>", unsafe_allow_html=True)
        st.write("Craftify scans the resume for ATS compliance, analyzing keywords, formatting, and structure.")
        st.markdown("<h3 style='color:  #F05A7E;'>3. Keyword Suggestions:</h3>", unsafe_allow_html=True)
        st.write("It identifies missing keywords and skills from the job description and provides actionable recommendations.")
        st.markdown("<h3 style='color:  #F05A7E;'>4. Optimization Feedback:</h3>", unsafe_allow_html=True)
        st.write("Users get a detailed report with visual insights to align their resume with recruiter expectations.")
       
        st.write("Future updates will guide users in integrating recommended changes seamlessly. there will be job searching integration as well ")
        st.markdown("---")
        # Mission statement
      