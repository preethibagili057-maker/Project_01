import streamlit as st
import ollama
from docx import Document

st.markdown("""
<style>
.stApp{
background-color : #FFB6C1;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Job Description Decoder... ",page_icon = "🤖",layout = "wide")
st.title("Job Description Decoder..🆔")

@st.cache_resource
def load_resources():
    model_name = "llama3.2"
    return model_name
model = load_resources()

st.write("Paste a complicated job description...🔎 and AI convert it into simple useful information....☸️")


st.subheader("Step 1: Job Description")
job_description = st.text_area("📄Paste Job Description...",height = 400, placeholder = "Paste here complete job description....🅾")
st.subheader("Step2: Upload Resume..")

resume_file = st.file_uploader(
    "Upload your Resume in word format", type = ["docx"]
)

resume_text = ""

if resume_file is not None:
    try:
        document = Document(resume_file)
        for paragraph in document.paragraphs:
            # if paragraph.text.strip():
                resume_text += paragraph.text + "\n"
        # for table in document.tables:
            # for row in table.rows:
                #  for cell in row.cells:
                    # if cell.text.strip():
                        # resume_text += cell.text + "\n"
        st.success("✅ Resume uploaded successfully!")
        st.text_area(
            "Extracted Resume",resume_text,height=300
        )
        # with st.expander("👀 View Extracted Resume"):
            # st.text(resume_text)
    except Exception as e:
        st.error("❌ Unable to read the Word document.")
        st.write(e)

if st.button(" Analyze Job & Resume"):
#if st.button("Job Description Decoder..")
    if job_description.strip() == "":
        st.warning("⚠️ Please Attach your job description first....🙃 ")
    elif resume_file is None:
        st.warning("⚠️ please upload your resume..")
    elif resume_text.strip() == "":
        st.warning("⚠️ Could not extract any text from the resume..")
    else:

        
            prompt = f"""
Analyze this Job Description:{job_description}
Return the result using these headings:
ROLE SUMMARY
TECHNICAL SKILLS
SOFT SKILLS
MUST-HAVE SKILLS
RESPONSIBILITIES
EXPERIENCE
EDUCATION
INTERVIEW TOPICS
HR QUESTIONS
TOOLS AND TECHNOLOGIES
TECHNICAL QUESTIONS

Use simple English and bullet points."""


    

with st.sidebar:
    st.header("⚙️ Settings")
    st.write("AI Model:")
    st.info(model)
    st.write("✅Skills Extraction")
    st.write("✅Responsibilities")
    st.write("✅Must-Have skills")
    st.write("✅Interview Topics")
    st.write("✅Interview Questions")

    try:
        with st.spinner("Analyzing....🤖 And it may take few seconds...🤧"):
            response = ollama.chat(
                model = "llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        
            result = response["message"]["content"]
            st.success("Job Description Decoded Successfully!")
            st.markdown("AI Analysis")
            st.markdown(result)
            st.download_button(
                label="Download Analysis..",data = result, file_name = "Job_Description_Analysis.txt",mime="text/plain"
            )
    except Exception as e:
        st.error("Ollama connection error..")
        st.code(str(e))

