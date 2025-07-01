# SOCIO/analyze_agent.py
from typing import Dict
from agents import Agent, trace, gen_trace_id

def analyze_function(extracted_data: Dict) -> str:
    """
    Analyze the extracted data from a webpage and generate an AI response
    Args:
        extracted_data: Dictionary containing webpage data from ContentExtractor
    Returns:
        str: AI analysis of the webpage content
    """
    metadata = extracted_data['metadata']
    content = extracted_data['content']
    media = extracted_data['media']
    theme = extracted_data['theme']

    return f"""
    Analyze this webpage with the following components:

    1. Metadata Analysis:
    - URL: {metadata['url']}
    - Title: {metadata['title']}
    - Timestamp: {metadata['timestamp']}

    2. Content Analysis:
    - Paragraph Count: {content['statistics']['paragraph_count']}
    - Heading Count: {content['statistics']['heading_count']}
    - Text Content Sample: {content['text_content']['paragraphs'][:2] if content['text_content']['paragraphs'] else 'No paragraphs found'}

    3. Media Analysis:
    - Total Images: {len(media['images'])}
    - Image Details: {[img['alt'] for img in media['images'][:3]] if media['images'] else 'No images found'}

    4. Theme Analysis:
    - Color Scheme: {theme['colors']}
    - Font Families: {theme['fonts']['families']}
    - Layout Structure: {theme['layout']}
    - UI Elements: {theme['style_elements']}

    Please provide a comprehensive analysis addressing each component above, including:
    1. Overall webpage structure and organization
    2. Content quality and relevance
    3. Visual design and user experience
    4. Technical implementation observations
    5. Recommendations for improvement
    """

# Define the agent
analyze_agent = Agent(
    name='WebpageAnalyzer',
    instructions="""You will get the data from using the analyze_tool and get the extracted data from the webpage and analyze the webpage and give the analysis in the language of the webpage""",
    tools=[analyze_function]
)