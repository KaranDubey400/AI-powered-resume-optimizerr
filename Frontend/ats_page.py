import streamlit as st
from streamlit_option_menu import option_menu
# NLP Library
import spacy
import pandas as pd
from backend.resumeAanalyzer import ResumeAnalyzer as RA
# Visualization
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
        try:
            st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Resume Analysis</font></h1>", unsafe_allow_html=True)
            
            # Upload resume file
            user_resume = st.file_uploader("📄 Upload Your Resume (in .docx format)", type=["docx"])
            
            # If resume is uploaded, convert content to text
            if user_resume is not None:
                try:
                    user_resume = RA.extract_text_from_word_document(user_resume) if user_resume.name.endswith('.docx') else None
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
            
            # Job Description Input
            use_file_for_job_description = st.checkbox("📄 Upload Job Description from file")
            job_description = None
            
            if use_file_for_job_description:
                job_description = st.file_uploader("Upload job description file (in .docx format)", type=["docx"])
                if job_description is not None:
                    try:
                        job_description = RA.extract_text_from_word_document(job_description) if job_description.name.endswith('.docx') else None
                        if job_description is not None:
                            st.success("🎉 Job description uploaded successfully!")
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
            
            # Scan Button - Now using this as our job_match flag
            scan_clicked = st.button("Scan Resume")
            
            if scan_clicked and user_resume and job_description:
                # Extract named entities from the provided resume
                sent1 = nlp(RA.clean_text(user_resume))
                entities = {label: [] for label in ["Job-Category","PERSON", "SKILL", "ORG","EDU","GPE","PK_ORG","SOFT_SKILL"]}
                for ent in sent1.ents:
                    if ent.label_ in entities:
                        entities[ent.label_].append(ent.text)
                
                # Display Personal Information
                if "PERSON" in entities:
                    name = entities["PERSON"][0].upper()
                    st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Name:</font></h1>", unsafe_allow_html=True)
                    highlight_style = "font-size: 16px; padding: 8px; background-color: white; color: black; border-radius: 5px; text-align: center; line-height: 2.5;"
                    st.markdown(f"<p><span style='{highlight_style}'>{name}</span></p>", unsafe_allow_html=True)
                else:
                    st.subheader("Name")
                    st.write("Name not detected")
                
                # Contact Information
                contact_number = RA.extract_contact_number(user_resume)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Contact No:</font></h1>", unsafe_allow_html=True)
                st.markdown(f"<p><span style='{highlight_style}'>{contact_number}</span></p>", unsafe_allow_html=True)
                
                # Email Information
                email = RA.extract_email(user_resume)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Email:</font></h1>", unsafe_allow_html=True)
                st.markdown(f"<p><span style='{highlight_style}'>{email}</span></p>", unsafe_allow_html=True)
                
                # Skills Analysis
                user_skills = RA.unique_skills(RA.extract_skills(RA.clean_text(user_resume), nlp)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>User Unique Skills:</font></h1>", unsafe_allow_html=True)
                skill_style = "font-size: 16px; text-transform: uppercase; padding: 8px; background-color: #1F79C9; font-weight: bold; color: white; border-radius: 5px; text-align: center; line-height: 2.5;"
                html_skills = " ".join(f"<span style='{skill_style}'>{skill}</span>" for skill in user_skills)
                st.markdown(f"<p>{html_skills}</p>", unsafe_allow_html=True)
                
                # Skills Distribution
                df = pd.DataFrame({"Clean_Resume": [RA.clean_text(user_resume)]})
                df["skills"] = df["Clean_Resume"].str.lower().apply(RA.extract_skills, nlp=nlp)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Distribution of Skills:</font></h1>", unsafe_allow_html=True)
                st.markdown("The skill distribution graph displays the frequency of skills mentioned in your resume...")
                fig = px.histogram(x=df["skills"].explode(), labels={"x": "Skills"})
                st.plotly_chart(fig, use_container_width=True)
                
                # Hard Skills Comparison
                skills_resume = Counter(RA.extract_skills(RA.clean_text(user_resume), nlp)
                skills_job_description = Counter(RA.extract_skills(RA.clean_text(job_description), nlp)
                skills_job_description_list = list(skills_job_description.keys())
                count_job_description = [skills_job_description[skill] for skill in skills_job_description_list]
                
                data = {
                    "Skill": skills_job_description_list,
                    "Count in Resume": [skills_resume.get(skill, 0) for skill in skills_job_description_list],
                    "Count in Job Description": count_job_description
                }
                
                df = pd.DataFrame(data)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Hard Skills:</font></h1>", unsafe_allow_html=True)
                st.markdown("Hard skills enable you to perform job-specific duties...")
                html = df.to_html(classes='data', header="true", index=False)
                html = f'<style> .data {{text-align: center; width: 100%;}} .data th {{text-align: center;background-color:#FF4B4B}} </style>' + html
                st.markdown(html, unsafe_allow_html=True)
                
                # Soft Skills Comparison
                soft_skills_resume = Counter(RA.extract_soft_skills(RA.clean_text(user_resume), nlp))
                soft_skills_job_description = Counter(RA.extract_soft_skills(RA.clean_text(job_description), nlp))
                skills_job_description_list = list(soft_skills_job_description.keys())
                count_job_description = [soft_skills_job_description[skill] for skill in skills_job_description_list]
                
                data = {
                    "Skill": skills_job_description_list,
                    "Count in Resume": [soft_skills_resume.get(skill, 0) for skill in skills_job_description_list],
                    "Count in Job Description": count_job_description
                }
                
                df = pd.DataFrame(data)
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>Soft Skills:</font></h1>", unsafe_allow_html=True)
                st.markdown("Soft skills are your traits and abilities that are not unique to any job...")
                html = df.to_html(classes='data', header="true", index=False)
                html = f'<style> .data {{text-align: center; width: 100%;}} .data th {{text-align: center;background-color:#FF4B4B}} </style>' + html
                st.markdown(html, unsafe_allow_html=True)
                
                # ATS Checker
                st.markdown("<h1 style='color: #FF4B4B;'> <font size='6'>ATS Checker & Tips:</font></h1>", unsafe_allow_html=True)
                st.markdown("Applicant Tracking Systems (ATS) are computers that process your resume...")
                
                job_entities = RA.extract_entities(job_description, nlp=nlp)
                resume_entities = RA.extract_entities(user_resume, nlp=nlp)
                entity_labels = ["Job-Category", "ORG", "EDU", "GPE", "PK_ORG"]
                
                feedback_messages = {
                    "Job-Category": {
                        "found": "We found relevant keywords related to job categories in your resume.",
                        "not_found": "We did not find any keywords related to job categories in your resume."
                    },
                    # ... other feedback messages ...
                }
                
                for label in entity_labels:
                    matched_entities = [entity for entity in resume_entities[label] if entity in job_entities[label]]
                    st.write(f"Label: {label}")
                    if label in feedback_messages:
                        feedback = feedback_messages[label]
                        keywords = ", ".join(RA.unique_skills(matched_entities))
                        if matched_entities:
                            st.success("Keywords: " + keywords + ". Feedback: " + feedback["found"])
                        else:    
                            st.error("Feedback: " + feedback["not_found"])
            
            # Sidebar Match Rate Analysis
            with st.sidebar:
                if scan_clicked and user_resume and job_description:
                    try:
                        resume_text = RA.clean_text(user_resume)
                        job_description_text = RA.clean_text(job_description)
                        match_percentage = RA.job_matching_algorithm(resume_text, job_description_text)
                        
                        if match_percentage is not None:
                            # Progress bar animation
                            progress_bar = st.progress(0)
                            for percent_complete in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(percent_complete + 1)
                            
                            feedback = RA.job_matching_feedback(match_percentage)
                            
                            # Match Rate Display
                            st.markdown("""
                            <style>
                                .match-rate-container {
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    padding: 20px;
                                }
                                .percentage-circle {
                                    height: 180px;
                                    width: 180px;
                                    background-color: #0E1117;
                                    color: #FF4B4B;
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    position: relative;
                                    margin: 0 auto 20px;
                                    border: 4px solid #FF4B4B;
                                }
                                .percentage-text {
                                    font-size: 36px;
                                    font-weight: 600;
                                }
                                .feedback-box {
                                    background-color: rgba(61, 157, 243, 0.2);
                                    padding: 15px;
                                    border-radius: 8px;
                                    width: 100%;
                                    max-width: 200px;
                                    margin: 0 auto;
                                    text-align: center;
                                }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="match-rate-container">
                                <h1 style='color: #FF4B4B; margin-bottom: 20px; text-align: center;'>Match Rate Analysis</h1>
                                <div class="percentage-circle">
                                    <span class="percentage-text">{match_percentage}%</span>
                                </div>
                                <div class="feedback-box">
                                    <div style="font-weight: bold; color: #0aa859; font-size: 24px; margin-bottom: 5px;">
                                        {match_percentage}% match
                                    </div>
                                    <div style="font-size: 18px; color: rgb(199, 235, 255);">
                                        {feedback}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning("Could not calculate match percentage.")
                    except Exception as e:
                        st.error(f"Error calculating match percentage: {str(e)}")
        
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
