#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import gradio as gr
from analyze_agent import analyze_agent
from content_extractor import ContentExtractor
from agents import trace, gen_trace_id

# Load environment variables
load_dotenv()

def process_webpage(url: str, progress=gr.Progress()) -> str:
    """
    Process flow:
    1. Take URL from Gradio interface
    2. Pass URL to ContentExtractor to get dictionary data
    3. Pass dictionary to analyze_agent
    4. Return analysis string to Gradio interface
    """
    trace_id = gen_trace_id()
    
    # Start the main trace for the entire process
    with trace("Website Analysis Process", trace_id=trace_id):
        try:
            progress(0, desc="Starting analysis...")
            print(f"Processing URL: {url}")
            
            # Extract content
            progress(0.3, desc="Extracting webpage content...")
            extractor = ContentExtractor()
            extracted_data = extractor.extract_content(url)
            print("Content extracted successfully")

            # Analyze content
            progress(0.6, desc="Analyzing content...")
            analysis_result = analyze_agent.run(extracted_data)
            print("Analysis completed")
            
            progress(1.0, desc="Done!")
            return analysis_result
        except Exception as e:
            error_msg = f"Error processing webpage: {str(e)}"
            print(error_msg)
            return error_msg

# Create Gradio interface
demo = gr.Interface(
    fn=process_webpage,
    inputs=[
        gr.Textbox(
            lines=1,
            placeholder="Enter website URL (e.g., https://www.google.com)",
            label="Website URL"
        )
    ],
    outputs=[
        gr.Textbox(
            lines=10,
            label="Website Analysis",
            show_copy_button=True
        )
    ],
    title="Website Content Analyzer",
    description="Enter a URL to get a detailed analysis of the webpage's content and structure.",
    examples=[
        ["https://www.google.com"],
        ["https://www.python.org"],
        ["https://www.github.com"]
    ],
    allow_flagging="never"
)

if __name__ == "__main__":
    print("Starting the web interface...")
    demo.launch(
        share=False,  # Set to True if you want to create a public link
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )