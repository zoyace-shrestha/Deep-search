from typing import List, Callable
import openai
import os
from functools import wraps
import time
import asyncio

class TraceContextManager:
    def __init__(self, name: str, trace_id: str = None):
        self.name = name
        self.trace_id = trace_id
        self.start_time = None

    def __enter__(self):
        print(f"Starting {self.name}...")
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"Completed {self.name} in {end_time - self.start_time:.2f}s")
        return False  # Don't suppress exceptions

def trace(name: str, trace_id: str = None):
    return TraceContextManager(name, trace_id)

def gen_trace_id() -> str:
    return f"trace_{int(time.time())}"

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        tools: List[Callable] = None
    ):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, input_data):
        """Run the agent with the given input"""
        try:
            # Use the first tool (analyze_function) to format the data
            if self.tools and len(self.tools) > 0:
                formatted_data = self.tools[0](input_data)
            else:
                formatted_data = str(input_data)

            # Get AI response
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": formatted_data}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in agent execution: {str(e)}" 