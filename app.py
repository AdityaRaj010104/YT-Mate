import streamlit as st
from dotenv import load_dotenv
import os
import streamlit as st
from dotenv import load_dotenv
import os

from transcript_extraction import fetch_transcript, get_available_languages, get_video_id
from text_splitter import split_text
from embedding_generation import generate_and_store_embeddings
from retriever import retrieve_from_vectorstore
from augumentation import build_augmented_prompt
from generation_answer import generate_answer_from_prompt
from summarize import generate_video_summary  # Import the new function

load_dotenv()
st.set_page_config(page_title="YT-Mate", layout="wide")

st.title("🎬 YT-Mate: Chat with YouTube Videos")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "video_summary" not in st.session_state:
    st.session_state.video_summary = None
if "vectorstore_path" not in st.session_state:
    st.session_state.vectorstore_path = None
if "current_video_lang" not in st.session_state:
    st.session_state.current_video_lang = None

@st.cache_resource(show_spinner=True)
def prepare_vectorstore(video_id, lang_code):
    """Prepare FAISS vectorstore for a given video_id + language."""
    tlist = fetch_transcript(video_id, lang_code)
    joined_text = " ".join(entry.text for entry in tlist)
    chunks = split_text(joined_text)
    path = f"faiss_index/{video_id}_{lang_code}"
    generate_and_store_embeddings(chunks, vectorstore_path=path)
    return path, tlist  # Return transcript list for summary generation

# Step 1: Input YouTube URL
url = st.text_input("Enter YouTube Video URL")

if url:
    video_id, langs = get_available_languages(url)

    # Show dropdown with available languages
    lang_display = [f"{name} ({code})" for name, code in langs]
    choice = st.selectbox("Choose Transcript Language", lang_display)

    if choice:
        lang_code = choice.split("(")[-1].strip(")")
        
        # Create a unique identifier for this video + language combination
        current_combo = f"{video_id}_{lang_code}"
        
        # Only process if it's a new video/language combination
        if st.session_state.current_video_lang != current_combo:
            # Reset chat history for new video/language
            st.session_state.chat_history = []
            
            # Prepare vectorstore and get transcript
            with st.spinner("Processing transcript and generating summary..."):
                path, transcript_list = prepare_vectorstore(video_id, lang_code)
                
                # Generate video summary
                summary = generate_video_summary(transcript_list)
                
                # Update session state
                st.session_state.video_summary = summary
                st.session_state.vectorstore_path = path
                st.session_state.current_video_lang = current_combo
        
        st.success(f"Transcript prepared in {choice} ✅")
        
        # Display video summary
        st.subheader("📝 Video Summary")
        st.info(st.session_state.video_summary)

        # Step 2: Chat
        st.subheader("💬 Chat with the Video")
        question = st.text_input("Ask a question:")

        if st.button("Ask") and question:
            with st.spinner("Processing.."):
                docs = retrieve_from_vectorstore(question, vectorstore_path=st.session_state.vectorstore_path)
                final_prompt = build_augmented_prompt(question, docs)
                answer = generate_answer_from_prompt(final_prompt)
                st.session_state.chat_history.append((question, answer))

        # Display chat history
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)


# import streamlit as st
# from dotenv import load_dotenv
# import os

# from transcript_extraction import fetch_transcript,get_available_languages, get_video_id
# from text_splitter import split_text
# from embedding_generation import generate_and_store_embeddings
# from retriever import retrieve_from_vectorstore
# from augumentation import build_augmented_prompt
# from generation_answer import generate_answer_from_prompt

# load_dotenv()
# st.set_page_config(page_title="YT-Mate", layout="wide")

# st.title("🎬 YT-Mate: Chat with YouTube Videos")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "video_id" not in st.session_state:
#     st.session_state.video_id = None

# @st.cache_resource(show_spinner=True)
# def prepare_vectorstore(video_id, lang_code):
#     """Prepare FAISS vectorstore for a given video_id + language."""
#     tlist = fetch_transcript(video_id, lang_code)
#     joined_text = " ".join(entry.text for entry in tlist)
#     chunks = split_text(joined_text)
#     path = f"faiss_index/{video_id}_{lang_code}"
#     generate_and_store_embeddings(chunks, vectorstore_path=path)
#     return path

# # Step 1: Input YouTube URL
# url = st.text_input("Enter YouTube Video URL")

# if url:
#     video_id, langs = get_available_languages(url)

#     # Show dropdown with available languages
#     lang_display = [f"{name} ({code})" for name, code in langs]
#     choice = st.selectbox("Choose Transcript Language", lang_display)

#     if choice:
#         lang_code = choice.split("(")[-1].strip(")")
#         path = prepare_vectorstore(video_id, lang_code)
#         st.success(f"Transcript prepared in {choice} ✅")

#         # Step 2: Chat
#         st.subheader("💬 Chat with the Video")
#         question = st.text_input("Ask a question:")

#         if st.button("Ask") and question:
#             docs = retrieve_from_vectorstore(question, vectorstore_path=path)
#             final_prompt = build_augmented_prompt(question, docs)
#             answer = generate_answer_from_prompt(final_prompt)
#             st.session_state.chat_history.append((question, answer))

#         # Display chat history
#         for q, a in st.session_state.chat_history:
#             with st.chat_message("user"):
#                 st.write(q)
#             with st.chat_message("assistant"):
#                 st.write(a)
