import streamlit as st
from streamlit_option_menu import option_menu
# NLP Library
import spacy
import pandas as pd
from backend.resumeAanalyzer import ResumeAnalyzer as RA
#Visualization
import plotly.express as px

import time
from collections import Counter
# NLP Eng language Model
nlp = spacy.load("en_core_web_lg")
# File Path
image_path = r"assets/logo/Colorlogo.png"
skill_pattern_path = r"assets/data/jz_complete_patterns.jsonl"

# Add entity ruler for skill patterns
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)


class Ats_page():

    def resume_parser():
    # Resume Title
        try:
            st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Resume Analysis</font></h1>", unsafe_allow_html=True)
            # Upload resume file
            user_resume = st.file_uploader("📄 Upload Your Resume (in .docx format)", type=["docx"])
            # If resume is uploaded, convert content to text
            if user_resume is not None:
                try:
                    user_resume = RA.extract_text_from_word_document(user_resume) if user_resume.name.endswith('.docx') else None
                    # Display success or error message based on file upload
                    if user_resume is not None:
                        st.success("🎉 Resume uploaded successfully!")
                    else:
                        st.error("❌ Please upload a .docx file.")
                    if st.button("Show Resume"):
                        if user_resume is not None:
                            st.subheader("Resume Text:")
                            st.text(user_resume)
                except Exception as e:
                    st.error(f"Error processing resume: {str(e)}")
                    user_resume = None
            st.markdown("<br>", unsafe_allow_html=True)
            # Checkbox to let the user choose the input method for Job Description
            use_file_for_job_description = st.checkbox("📄 Upload Job Description from file")

            if use_file_for_job_description:
                job_description = st.file_uploader("Upload job description file (in .docx format)", type=["docx"])
                if job_description is not None:
                    try:
                        job_description = RA.extract_text_from_word_document(job_description) if job_description.name.endswith('.docx') else None
                        if job_description is not None:
                            st.success("🎉 job_description uploaded successfully!")
                        else:
                            st.error("❌ Please upload a .docx file.")
                        if st.button("Show Job"):
                            if job_description is not None:
                                st.subheader("Job Description:")
                                st.text(job_description)
                    except Exception as e:
                        st.error(f"Error processing job description: {str(e)}")
                        job_description = None
            else:
                job_description = st.text_area("✍️ Paste job description here ⬇️")
                if job_description:
                    st.subheader("Job Description:")
                    st.text(job_description.replace('\n', ' '))
                        
            st.markdown("<hr>", unsafe_allow_html=True)
            #  Scan Buttons
            job_match = False
            if st.button("Scan Resume"):
                # Extract named entities from the provided resume
                sent1 = nlp(RA.clean_text(user_resume))
                entities = {label: [] for label in ["Job-Category","PERSON", "SKILL", "ORG","EDU","GPE","PK_ORG","SOFT_SKILL"]}
                for ent in sent1.ents:
                    if ent.label_ in entities:
                        entities[ent.label_].append(ent.text)
                        
                # Access the PERSON entity if available
                if "PERSON" in entities:
                    name = entities["PERSON"][0]  # Assuming there's only one person's name detected
                    name = name.upper() 
                    st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Name:</font></h1>", unsafe_allow_html=True)
                    # Define CSS style for highlighting
                    highlight_style = "font-size: 16px; padding: 8px; background-color: white ; color: black; border-radius: 5px; text-align: center; line-height: 2.5;"
                    # Generate HTML for displaying skills with highlighting
                    html_name = "".join(f"<span style='{highlight_style}'>{name}</span>")
                    styled_skills_paragraph = f"<p>{html_name}</p>"
                    st.markdown(styled_skills_paragraph, unsafe_allow_html=True)
                else:
                    st.subheader("Name")
                    st.write("Name not detected")
                    
                # Access the contact information
                contact_number = RA.extract_contact_number(user_resume)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Contact No:</font></h1>", unsafe_allow_html=True)
                # Define CSS style for highlighting
                highlight_style = "font-size: 16px; padding: 8px; background-color: white ; color: black; border-radius: 5px; text-align: center; line-height: 2.5;"
                # Generate HTML for displaying skills with highlighting
                html_name = "".join(f"<span style='{highlight_style}'>{contact_number}</span>")
                styled_skills_paragraph = f"<p>{html_name}</p>"
                st.markdown(styled_skills_paragraph, unsafe_allow_html=True)
                
                # Access the email information
                email = RA.extract_email(user_resume)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Email:</font></h1>", unsafe_allow_html=True)
                # Define CSS style for highlighting
                highlight_style = "font-size: 16px; padding: 8px; background-color: white ; color: black; border-radius: 5px; text-align: center; line-height: 2.5;"
                # Generate HTML for displaying skills with highlighting
                html_name = "".join(f"<span style='{highlight_style}'>{email}</span>")
                styled_skills_paragraph = f"<p>{html_name}</p>"
                st.markdown(styled_skills_paragraph, unsafe_allow_html=True)
                
                # Add Match Rate Analysis here
                if job_match:
                    try:
                        # Get the matching percentage first
                        match_percentage = RA.job_matching_algorithm(resume_text, job_description_text)
                        
                        if match_percentage is not None:
                            # Show progress bar animation
                            progress_bar = st.progress(0)
                            for percent_complete in range(100):
                                time.sleep(0.04)
                                progress_bar.progress(percent_complete + 1)
                            
                            # Determine the feedback based on the match percentage
                            feedback = RA.job_matching_feedback(match_percentage)
                            
                            # Display the actual circular progress bar with the match percentage
                            st.markdown("<h1 style='color: #FF4B4B; text-align: center; margin-bottom: 20px;'>Match Rate Analysis</h1>", unsafe_allow_html=True)
                            progress_bar_html = f"""
                            <div style="display: flex; justify-content: center; width: 100%;">
                                <div class="result-container">
                                    <div class="percentage-container">
                                        <div class="percentage-circle"></div>
                                        <span>{match_percentage}%</span>
                                    </div>
                                    <div class="highlighted-text">
                                        <div class="match-percentage">{match_percentage}%</div>
                                        <div class="feedback">{feedback}</div>
                                    </div>
                                </div>
                            </div>
                            <style>
                                .result-container {{
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    justify-content: center;
                                    text-align: center;
                                    width: fit-content;
                                    padding: 20px;
                                    margin: 0 auto;
                                }}
                                .percentage-container {{
                                    height: 180px;
                                    width: 180px;
                                    background-color: #0E1117;
                                    color: #FF4B4B;
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    position: relative;
                                    margin: 0 auto 20px auto;
                                }}
                                .percentage-circle {{
                                    position: absolute;
                                    width: 100%;
                                    height: 100%;
                                    border: 4px solid #FF4B4B;
                                    border-radius: 50%;
                                }}
                                .percentage-container span {{
                                    font-size: 36px;
                                    font-weight: 600;
                                    z-index: 1;
                                }}
                                .highlighted-text {{
                                    background-color: rgba(61, 157, 243, 0.2);
                                    padding: 15px;
                                    border-radius: 8px;
                                    width: 180px;
                                    margin: 0 auto;
                                }}
                                .match-percentage {{
                                    font-weight: bold;
                                    color: #0aa859;
                                    font-size: 24px;
                                    margin-bottom: 5px;
                                }}
                                .feedback {{
                                    font-size: 18px;
                                    color: rgb(199, 235, 255);
                                    margin-top: 5px;
                                }}
                            </style>
                            """
                            st.markdown(progress_bar_html, unsafe_allow_html=True)
                        else:
                            st.warning("Could not calculate match percentage. Please check if both resume and job description contain sufficient text.")
                    except Exception as e:
                        st.error(f"Error calculating match percentage: {str(e)}")
                        st.error("Please make sure both resume and job description are properly uploaded and contain text content.")
                
                # Extract skills from user resume
                user_skills = RA.unique_skills(RA.extract_skills(RA.clean_text(user_resume),nlp))
                # Display user skills
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>User Unique Skills:</font></h1>", unsafe_allow_html=True)
                # Define CSS style for highlighting
                highlight_style = "font-size: 16px;text-transform: uppercase; padding: 8px; background-color: #1F79C9 ; font-weight: bold; color: white; border-radius: 5px; text-align: center; line-height: 2.5;"
                # Generate HTML for displaying skills with highlighting
                html_skills = " ".join(f"<span style='{highlight_style}'>{skill}</span>" for skill in user_skills)
                styled_skills_paragraph = f"<p>{html_skills}</p>"
                st.markdown(styled_skills_paragraph, unsafe_allow_html=True)
                
                # Generate 'skills' column dynamically
                df = pd.DataFrame({"Clean_Resume": [RA.clean_text(user_resume)]})
                df["skills"] = df["Clean_Resume"].str.lower().apply(RA.extract_skills, nlp=nlp)
                # Display distribution of skills
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Distribution of Skills:</font></h1>", unsafe_allow_html=True)
                # Add a tooltip or popup message
                st.markdown("The skill distribution graph displays the frequency of skills mentioned in your resume. It shows which skills are mentioned most frequently, helping you identify your strengths at a glance. Use it to emphasize relevant skills, tailor your resume to specific job requirements, and highlight your qualifications effectively. If you have any questions, refer to the tool's documentation or contact support for assistance.")
                # Display the histogram
                fig = px.histogram(x=df["skills"].explode(), labels={"x": "Skills"})
                st.plotly_chart(fig, use_container_width=True) 
                ################################################################################################################################
                # Assuming get_skills() returns a list of skills and clean_text() processes the resume text
                skills_resume = Counter(RA.extract_skills(RA.clean_text(user_resume),nlp))
                skills_job_description= Counter(RA.extract_skills(RA.clean_text(job_description),nlp))
                
                # If you still need the skills and counts as lists, you can convert them like this
                skills_job_description_list = list(skills_job_description.keys())
                count_job_description = [skills_job_description[skill] for skill in skills_job_description_list]
                # Create a dictionary with the data
                data = {
                    "Skill": skills_job_description_list,
                    "Count in Resume": [skills_resume.get(skill, 0) for skill in skills_job_description_list],
                    "Count in Job Description": count_job_description
                }

                # Create a DataFrame from the data
                df = pd.DataFrame(data)
                # Display the table
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Hard Skills:</font></h1>", unsafe_allow_html=True)
                st.markdown("Hard skills enable you to perform job-specific duties and responsibilities. You can learn hard skills in the classroom, training courses, and on the job. These skills are typically focused on teachable tasks and measurable abilities such as the use of tools, equipment, or software. Hard skills have a high impact on your match score.")
                st.markdown("<strong>Tip: </strong>Match the skills in your resume to the exact spelling in the job description. Prioritize skills that appear most frequently in the job description.",unsafe_allow_html=True)
                # Apply center alignment to all columns
                html = df.to_html(classes='data', header="true", index=False)
                # Apply CSS to center-align text in the table
                html = f'<style> .data {{text-align: center; width: 100%;}} .data th {{text-align: center;background-color:#FF4B4B}} </style>' + html
                # Render the HTML table using markdown
                st.markdown(html, unsafe_allow_html=True)            
                ################################################################################################################################

                # Assuming get_soft_skills() returns a list of skills and clean_text() processes the resume text
                soft_skills_resume = Counter(RA.extract_soft_skills(RA.clean_text(user_resume),nlp))
                soft_skills_job_description= Counter(RA.extract_soft_skills(RA.clean_text(job_description),nlp))
                # If you still need the skills and counts as lists, you can convert them like this
                skills_job_description_list = list(soft_skills_job_description.keys())
                count_job_description = [soft_skills_job_description[skill] for skill in skills_job_description_list]
                # Create a dictionary with the data
                data = {
                    "Skill": skills_job_description_list,
                    "Count in Resume": [soft_skills_resume.get(skill, 0) for skill in skills_job_description_list],
                    "Count in Job Description": count_job_description
                }
                # Create a DataFrame from the data
                df = pd.DataFrame(data)
                # Display the table
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Soft Skills:</font></h1>", unsafe_allow_html=True)
                st.markdown("Soft skills are your traits and abilities that are not unique to any job. Your soft skills are part of your personality, and can be learned also. These skills are the traits that typically make you a good employee for any company such as time management and communication. Soft skills have a medium impact on your match score.")
                st.markdown("<strong>Tip: </strong>Prioritize hard skills in your resume to get interviews, and then showcase your soft skills in the interview to get jobs. ",unsafe_allow_html=True)
                # Apply center alignment to all columns
                html = df.to_html(classes='data', header="true", index=False)
                # Apply CSS to center-align text in the table
                html = f'<style> .data {{text-align: center; width: 100%;}} .data th {{text-align: center;background-color:#FF4B4B}} </style>' + html
                # Render the HTML table using markdown
                st.markdown(html, unsafe_allow_html=True)
                
                ################################################################################################################################
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>ATS Checker & Tips:</font></h1>", unsafe_allow_html=True)
                st.markdown("Applicant Tracking Systems (ATS) are computers that process your resume to understand your work history and relevance to the job description. These findings typically include your work history, job titles, relevant skills and education, as well as contact information like your name, phone number, and email address.")
                st.markdown("<strong>Tip: </strong>Complete all checks below to ensure your resume is easily searchable by recruiters and ATS.",unsafe_allow_html=True)        
                
                job_entities = RA.extract_entities(job_description,nlp=nlp)
                resume_entities = RA.extract_entities(user_resume,nlp=nlp)
                # Define entity labels to compare
                entity_labels = ["Job-Category", "ORG", "EDU", "GPE", "PK_ORG"]

                
                matched_data = {}
                # Define feedback messages
                feedback_messages = {
                    "Job-Category": {
                        "found": "We found relevant keywords related to job categories in your resume.",
                        "not_found": "We did not find any keywords related to job categories in your resume. Please consider adding relevant keywords."
                    },
                    "EDU": {
                        "found": "We found relevant keywords related to education in your resume.",
                        "not_found": "We did not find any keywords related to education in your resume. Please consider adding relevant keywords."
                    },
                    "PK_ORG": {
                        "found": "We found relevant keywords related to organizations/projects in your resume.",
                        "not_found": "We did not find any keywords related to organizations/projects in your resume. Please consider adding relevant keywords."
                    },
                    "ORG": {
                        "found": "We found relevant keywords related to organizations/projects in your resume.",
                        "not_found": "We did not find any keywords related to organizations/projects in your resume. Please consider adding relevant keywords."
                        },
                    "GPE": {
                        "found": "We found relevant keywords related to locations in your resume.",
                        "not_found": "We did not find any keywords related to locations in your resume. Please consider adding relevant keywords."
                    }
                }
                # Compare entities between job description and resume
                for label in entity_labels:
                    # Find the intersection of entities between job description and resume
                    matched_data[label] = [entity for entity in resume_entities[label] if entity in job_entities[label]]

                # Display matched data
                for label, data in matched_data.items():
                    st.write(f"Label: {label}")
                    if label in feedback_messages:
                        feedback = feedback_messages[label]
                        keywords = ", ".join(RA.unique_skills(data))  # Convert the list to a comma-separated string
                        if any(entity in job_entities[label] for entity in data):
                            st.success("Keywords: " + keywords + ". Feedback: " + feedback["found"])
                        else:    
                            st.error("Feedback: " + feedback["not_found"])
                ################################################################################################################################
                job_match = True 
        #####################################Job Matching Algorithm#####################################################################
            with st.sidebar:
                progress_bar_html = """
                <style>
                    .sidebar-result-container {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        width: 100%;
                        padding: 20px;
                        margin: 20px 0;
                    }
                    .sidebar-percentage-container {
                        height: 180px;
                        width: 180px;
                        background-color: #0E1117;
                        color: #FF4B4B;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                        margin: 0 auto 20px auto;
                    }
                    .sidebar-percentage-circle {
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        border: 4px solid #FF4B4B;
                        border-radius: 50%;
                    }
                    .sidebar-percentage-container span {
                        font-size: 36px;
                        font-weight: 600;
                        z-index: 1;
                    }
                    .sidebar-highlighted-text {
                        background-color: rgba(61, 157, 243, 0.2);
                        padding: 15px;
                        border-radius: 8px;
                        width: 180px;
                        margin: 0 auto;
                    }
                    .sidebar-match-percentage {
                        font-weight: bold;
                        color: #0aa859;
                        font-size: 24px;
                        margin-bottom: 5px;
                    }
                    .sidebar-feedback {
                        font-size: 18px;
                        color: rgb(199, 235, 255);
                        margin-top: 5px;
                    }
                </style>
                """
                st.markdown(progress_bar_html, unsafe_allow_html=True)

                if user_resume and job_description:
                    # Convert the file content to text
                    resume_text = RA.clean_text(user_resume)
                    job_description_text = RA.clean_text(job_description)
                    if not job_match:
                        pass
                    if job_match:
                        try:
                            # Get the matching percentage first
                            match_percentage = RA.job_matching_algorithm(resume_text, job_description_text)
                            
                            if match_percentage is not None:
                                # Show progress bar animation
                                progress_bar = st.progress(0)
                                for percent_complete in range(100):
                                    time.sleep(0.04)
                                    progress_bar.progress(percent_complete + 1)
                                
                                # Determine the feedback based on the match percentage
                                feedback = RA.job_matching_feedback(match_percentage)
                                
                                # Display the actual circular progress bar with the match percentage
                                st.markdown("<h1 style='color: #FF4B4B; text-align: center; margin-bottom: 20px;'>Match Rate Analysis</h1>", unsafe_allow_html=True)
                                progress_bar_html = f"""
                                <div class="sidebar-result-container">
                                    <div class="sidebar-percentage-container">
                                        <div class="sidebar-percentage-circle"></div>
                                        <span>{match_percentage}%</span>
                                    </div>
                                    <div class="sidebar-highlighted-text">
                                        <div class="sidebar-match-percentage">{match_percentage}%</div>
                                        <div class="sidebar-feedback">{feedback}</div>
                                    </div>
                                </div>
                                """
                                st.markdown(progress_bar_html, unsafe_allow_html=True)
                            else:
                                st.warning("Could not calculate match percentage. Please check if both resume and job description contain sufficient text.")
                        except Exception as e:
                            st.error(f"Error calculating match percentage: {str(e)}")
                            st.error("Please make sure both resume and job description are properly uploaded and contain text content.")
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
            st.error("Please check if the files are in correct format and try again.")
