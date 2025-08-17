from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def generate_video_summary(transcript_entries, video_title=None):
    """
    Enhanced version that can include video title in the summary if available.
    
    Args:
        transcript_entries (list): List of transcript entries
        video_title (str, optional): Title of the video if available
    
    Returns:
        str: A brief summary with optional title context
    """
    try:
        # Join all transcript chunks into one complete string
        full_transcript = " ".join(entry.text for entry in transcript_entries)
        
        # Adjust prompt based on whether we have title
        if video_title:
            template = """
            You are an expert at creating concise and informative video summaries.
            
            Video Title: {title}
            
            Please provide a brief summary of the following YouTube video transcript.
            The summary should be:
            - 3-5 sentences long
            - Capture the main topic and key points
            - Be informative and engaging
            - Written in a clear, easy-to-understand manner
            - Consider the video title for context
            
            Transcript:
            {transcript}
            
            Brief Summary:
            """
            input_vars = ["title", "transcript"]
        else:
            template = """
            You are an expert at creating concise and informative video summaries.
            
            Please provide a brief summary of the following YouTube video transcript.
            The summary should be:
            - 3-5 sentences long
            - Capture the main topic and key points
            - Be informative and engaging
            - Written in a clear, easy-to-understand manner
            
            Transcript:
            {transcript}
            
            Brief Summary:
            """
            input_vars = ["transcript"]
        
        summary_prompt = PromptTemplate(
            template=template,
            input_variables=input_vars
        )
        
        # Format the prompt
        if video_title:
            formatted_prompt = summary_prompt.format(title=video_title, transcript=full_transcript)
        else:
            formatted_prompt = summary_prompt.format(transcript=full_transcript)
        
        # Initialize Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Generate summary
        response = llm.invoke(formatted_prompt)
        
        return response.content.strip()
        
    except Exception as e:
        print(f"❌ Error generating video summary: {e}")
        return "Unable to generate summary at this time."