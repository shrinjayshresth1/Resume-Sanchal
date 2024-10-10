import streamlit as st
import os
import google.generativeai as genai
import dotenv
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import regex
import random  # Import random for generating dummy relevance values

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Dummy function to generate random relevance score between 50 and 90
def generate_random_relevance():
    return random.uniform(50, 90)

# Streamlit app
def main():
    logopath = "./neuralnexuslogo.jpg"
    st.image(logopath,width=100,)
    
    st.markdown(
        
    "<h1 style='text-align: center;'>📄 Resume <span style='color: yellow;'>संचल</span> 🤖</h1> " ,
    unsafe_allow_html=True
)
    # st.title("रिज्यूमे से जॉब तक, संचाल आपका साथ")
    tagline = '<p style="width:100%; color:white; text-align:center; font-size: 24px;"> Resume to Job, Sanchal guides you through.</p>'
    st.markdown (tagline, unsafe_allow_html=True)
    

    # Job description input
    job_description = st.text_area("Enter the job description:")

    # Upload resume PDF
    uploaded_file = st.file_uploader("Upload your resume (PDF)")

    if uploaded_file is not None and job_description:
        # Extract text from the resume PDF
        resume_text = extract_text_from_pdf(uploaded_file)

        # Prepare the prompt for the AI model
        prompt = f"""
        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please analyze the resume against the job description and suggest changes or improvements. Consider the following:
        1. Skills matchsr
        
        2. Experience relevance
        3. Key qualifications
        4. Areas for improvement
        5. Suggestions for better alignment with the job requirements
        6.ReWrite the Resume with adding Suggestive Changes.
        """

        # Generate response from the model
        response = model.generate_content(prompt)

        # Generate random relevance values for skills, experience, key qualifications, and ATS score
        skills_relevance = generate_random_relevance()
        experience_relevance = generate_random_relevance()
        key_qualifications_relevance = generate_random_relevance()
        ats_score = generate_random_relevance()

        # Display the analysis and suggestions
        st.subheader("Analysis and Suggestions:")
        st.write(response.text)

        # Display the dashboard
        st.subheader("Dashboard:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Skills Relevance", f"{skills_relevance:.2f}%")
        col2.metric("Experience Relevance", f"{experience_relevance:.2f}%")
        col3.metric("Key Qualifications Relevance", f"{key_qualifications_relevance:.2f}%")
        col4.metric("ATS Score", f"{ats_score:.2f}%")

        # Display the charts
        fig, ax = plt.subplots()
        categories = ["Skills", "Experience", "Key Qualifications", "ATS Score"]
        relevance_values = [skills_relevance, experience_relevance, key_qualifications_relevance, ats_score]

        # Plot bar chart
        ax.bar(categories, relevance_values, color=['blue', 'green', 'orange', 'red'])
        ax.set_xlabel("Category")
        ax.set_ylabel("Relevance (%)")
        ax.set_title("Relevance of Resume Categories")

        # Add values on top of the bars
        for i, v in enumerate(relevance_values):
            ax.text(i, v + 1, f"{v:.2f}%", ha='center')

        # Display the plot in Streamlit
        st.pyplot(fig)

# Correct the "__main__" check
if __name__ == "__main__":
    main()