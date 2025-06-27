import streamlit as st


class home():
    def home_page():
        custom_css = """
            <style>
                .section-container {
                    width: 100%;
                    padding: 50px;
                     background-color: #D7C3F1;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    align-items: center;
                    border-radius: 30px;
                    color: #33372C;
                }
                .main-content {
                    width: 60%;
                    display: flex;
                    flex-direction: column;
                    align-items: flex-start;
                }
                .heading1 {
                    font-size: 2.5em;
                    font-weight: 700;
                    line-height: 1.2;
                    margin-bottom: 20px;
                }
                .description {
                    font-size: 1.2em;
                    line-height: 1.5;
                    margin-bottom: 20px;
                }
                .cta-button {
                    padding: 15px 30px;
                    background: white;
                    background: #F7EFE5;
                    border-radius: 9px;
                    text-align: center;
                    cursor: pointer;
                    box-shadow: 0px 12px 14px rgba(0, 0, 0, 0.10);
                }

                .cta-button-text {
                    color: #a2d2ff;
                    font-size: 1.2em;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                }
                .image-container {
                    width: 35%;
                    box-shadow: 0px 12px 14px rgba(0, 0, 0, 0.10);
                    border-radius: 10px;
                    overflow: hidden;
                }
                .image {
                    width: 100%;
                    height: auto;
                    border-radius: 10px;
                }
                .centered-button {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }
            </style>
        """

        # Render the HTML content with custom CSS
        st.markdown(custom_css, unsafe_allow_html=True)

        # Render the HTML structure
        st.markdown(
            """
        <div class="section-container">
            <div class="main-content">
                <div class="heading1">Optimize your resume<br/>to get more interviews</div>
                <div class="description">Craftify helps you optimize your resume for any job, highlighting the key<br/>experience and skills recruiters need to see.</div>
                <div class="cta-button">
                    <a href="https://resources.workable.com/career-center/how-to-optimize-your-resume-for-an-ats/" ></i> Info </a>
                    <div></div>
                </div>
            </div>
            <div class="image-container">
             <img class="image" src="https://wpcontentpilot.com/wp-content/uploads/2023/12/support-page-illustration.svg"  alt="Resume Image"/>     
            </div>
        </div>

        <br>
        <div class="section-container">
            <div class="main-content">
            <div class="heading1">APPLICANT TRACKING SYSTEM</div>
                <div class="description">Many job seekers don’t get enough interviews even after applying for dozens of jobs. Why?<br/>Companies use <span style="font-weight: 700; color: #F05A7E">Applicant Tracking Systems (ATS)</span> to search and filter resumes by keywords. The Craftify resume scanner helps you optimize your resume keywords for each job listing so that your application gets found by recruiters.</div>
                <div class="heading3" style="font-weight: 700; color: #F05A7E; font-size: 1.2em; margin-top: 20px;">Craftify job search tools can increase your interview chances by 50%.</div>
            </div>
            <div class="image-container">
            <img class="image" src="https://img.freepik.com/free-vector/hand-drawn-flat-design-shrug-illustration_23-2149318820.jpg?t=st=1713051432~exp=1713055032~hmac=d81a3c98d855cfa33ede814835d397f530c4064e28c46cf8d3ac2c8c1622debd&w=740" style="height: 350px; width:230;" />
        </div>
        </div>    
        <br>
        <div class="section-container">
            <div class="DivTabs" style="position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <div class="heading1" style="font-weight: 700;text-transform: uppercase;  ">Features</div>
                <div class="description">
                    <div class="AtsResumeChecker" style="font-weight: 700; ; font-size: 1em;"></div>
                    <div class="OptimizeYourResumeForApplicantTrackingSystems" style="font-size: 1.2em;">1. Optimize your resume for applicant tracking systems.</div>
                </div>
                <div class="description" style="margin-top: 10px;">
                    <div class="ResumeAndCoverLetterOptimization" style=" font-size: 1.2em;">2. ATS Scanner for your Resume</div>
                </div>
                <div class="description" style="margin-top: 10px;">
                    <div class="ResumeBuilder" style=" font-size: 1.2em;">3. Semantic Analysis Keywords Extraction</div>
                </div>
                <div class="description" style="margin-top: 10px; margin-bottom: 20px;">
                    <div class="LinkedinProfileOptimization" style="font-size: 1.2em;">4. Career Gateways</div>
                </div>
            </div>
            <div>
                <img class="X34001NewPng" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0px 12px 14px rgba(0, 0, 0, 0.10);" src="https://static.jobscan.co/blog/uploads/533x340_01_new.png" />
            </div>
        </div>
        </div>

        <br>
        <div class="section-container">
        <div class="main-content">
            <div class="heading1">RESUME OPTIMIZATION</div>
            <div class="description">Show that you're the perfect match. Is your resume a good match for what a recruiter is looking for? If it's not, you might miss out on interviews for jobs you feel qualified for. </div>
        </div>
        <div class="image-container">
            <img class="image" src="https://static.jobscan.co/blog/uploads/score_fixer_2.webp" />
        </div>
        </div>
        <br>
     
        <br>
            """,
            unsafe_allow_html=True
        )

