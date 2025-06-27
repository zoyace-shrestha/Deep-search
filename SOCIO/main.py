#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr


load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI(api_key=api_key)

prompt = "What is the capital of France?"

def get_ai_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# Create Gradio interface
demo = gr.Interface(
    fn=get_ai_response,
    inputs=gr.Textbox(lines=4, placeholder="Ask me anything..."),
    outputs=gr.Textbox(lines=8, label="AI Response"),
    title="AI Deep Research",
    description="Ask any question and get an AI-powered response!",
    examples=[
        ["What is the capital of France?"],
        ["Explain quantum computing in simple terms"],
        ["Write a short poem about coding"]
    ],
    cache_examples=False  # Disable caching
)

if __name__ == "__main__":
    print("Starting the web interface...")
    demo.launch(share=True)