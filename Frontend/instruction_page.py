import streamlit as st


class Instruction():
    def instruction():
        # Custom CSS styles
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
            padding: 5px 0px;
            border-radius: 9px;
            text-align: center;
             background: #F7EFE5;
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

        # Steps data
        steps_data = [
            {
                "title": "Begin with the Job Description",
                "description": "The first step in tailoring your resume is to carefully read the job description. Pay close attention to the skills, qualifications, and experiences the employer is looking for. Highlight key phrases and requirements to reference throughout your resume.",
                "example": "Job Description: \n\nSeeking a marketing specialist with experience in social media management, content creation, and data analysis.\n\nIdentified Skills:\n- Social media management\n- Content creation\n- Data analysis"
            },
            {
                "title": "Identify Relevant Experiences",
                "description": "Once you've analyzed the job description, identify experiences from your professional background that align with the requirements. Focus on highlighting achievements and responsibilities that demonstrate your ability to excel in the role.",
                "example": "\n\n- Increased brand visibility by 30% through strategic social media campaigns.\n- Analyzed data to optimize content performance and drive user engagement."
            },
            {
                "title": "Customize Resume Objective or Summary",
                "description": "Craft a tailored resume objective or summary that showcases your relevant skills and experiences. This section serves as a brief introduction to your resume and should grab the attention of the hiring manager by highlighting your suitability for the position.",
                "example": "\n\n- Results-driven marketing specialist with extensive experience in social media management, content creation, and data analysis.\n- Proven track record of driving engagement and increasing brand visibility."
            },
            # Add more steps as needed
            {
                "title": "Adjust Professional Experience Section",
                "description": "Tailor the professional experience section of your resume to emphasize the most relevant roles and accomplishments. Use action verbs and quantifiable results to showcase your achievements and demonstrate your value to potential employers.",
                "example": "Revised Professional Experience:\n\n- Social Media Manager, XYZ Company\n- Increased brand visibility by 30% through strategic social media campaigns.\n- Analyzed data to optimize content performance and drive user engagement."
            },
            {
                "title": "Highlight Relevant Skills",
                "description": "Ensure that the skills listed on your resume match those mentioned in the job description. Provide specific examples of how you've used these skills in previous roles to solve problems, achieve goals, or contribute to the success of your team or organization.",
                "example": "Highlighted Skills:\n\n- Social media management: Managed multiple social media platforms and developed content calendars to increase engagement.\n- Content creation: Produced high-quality written and visual content for social media posts, blogs, and email campaigns."
            },
            {
                "title": "Quantify Achievements",
                "description": "Wherever possible, quantify your achievements with numbers, percentages, or other measurable metrics. This helps to provide concrete evidence of your capabilities and demonstrates the impact of your work.",
                "example": "Quantified Achievements:\n\n- Increased website traffic by 40% through SEO optimization strategies.\n- Generated $100,000 in revenue through successful email marketing campaigns."
            },
            {
                "title": "Incorporate Keywords",
                "description": "To ensure your resume gets past Applicant Tracking Systems (ATS), incorporate relevant keywords from the job description. ATS software scans resumes for specific terms and phrases, so including these keywords increases the likelihood of your resume being selected for further review.",
                "example": "Keywords:\n\n- Social media management\n- Content creation\n- Data analysis"
            },
            {
                "title": "Tailor Education Section (If Applicable)",
                "description": "If your education is relevant to the position, customize the education section of your resume to highlight relevant coursework, projects, or academic achievements. This provides additional context for your qualifications and demonstrates your commitment to continuous learning and skill development.",
                "example": "Tailored Education:\n\n- Bachelor of Business Administration, Marketing\n- Relevant coursework: Social Media Marketing Strategies, Data Analysis for Marketing, Digital Content Creation."
            },
            {
                "title": "Formatting and Style",
                "description": "Pay attention to the formatting and style of your resume to ensure it is professional and easy to read. Use a clean layout, consistent font styles and sizes, and plenty of white space to enhance readability and visual appeal.",
                "example": "Professional Formatting:\n\n- Use a clean, easy-to-read font such as Arial or Calibri.\n- Maintain consistent spacing and alignment throughout the document."
            },
            {
                "title": "Provide Examples and References",
                "description": "Seek out examples and references to help guide you through the resume tailoring process. Online resources, including resume templates, guides, and articles, can provide valuable insights and inspiration for crafting a standout resume.",
                "example": "Online Resources:\n\n- Resume templates and guides from reputable websites such as Indeed, Monster, and LinkedIn.\n- Articles and blog posts offering tips and best practices for resume writing and tailoring."
            },
            {
                "title": "Review and Revise",
                "description": "Before submitting your tailored resume, review it carefully for errors, inconsistencies, and areas for improvement. Consider seeking feedback from trusted colleagues, mentors, or professional resume writers to ensure your resume is polished and ready for submission.",
                "example": "Revision Process:\n\n- Review each section of your resume for accuracy and completeness.\n- Proofread carefully for spelling, grammar, and punctuation errors."
            }
        ]

        # Render steps
        for step in steps_data:
            st.markdown(f"""
            <div class="section-container">
                <div class="main-content">
                    <div class="heading1">{step['title']}</div>
                    <div class="description">{step['description']}</div>
                    <div class="cta-button">
                        <span class="cta-button-text">Example</span>
                    </div>
                    <div class="example">{step['example']}</div>
                </div>
                <div class="image-container">
                    <img class="image" src="https://img.freepik.com/free-vector/instruction-manual-smart-man-with-laptop-studying-handbook-reading-guidebook-cartoon-character-use-terms-tutorial-guide-digital-documentation_335657-1600.jpg" alt="Resume Image"/>
                </div>
            </div>
            <br>
            """, unsafe_allow_html=True)