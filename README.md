# Website Content Analyzer

A powerful tool that analyzes websites and provides detailed insights about their content, structure, and design using AI-powered analysis.

## Features

- **Content Extraction**: Automatically extracts and processes webpage content including:
  - Text content (paragraphs, headings)
  - Media elements (images with alt text)
  - Metadata (title, URL, timestamp)
  - Theme information (colors, fonts, layout)

- **AI Analysis**: Provides comprehensive analysis of:
  - Overall webpage structure and organization
  - Content quality and relevance
  - Visual design and user experience
  - Technical implementation observations
  - Recommendations for improvement

- **User Interface**: 
  - Clean and intuitive Gradio web interface
  - Progress tracking during analysis
  - Copy-to-clipboard functionality
  - Example URLs for quick testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Deep-search
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the web interface:
```bash
python SOCIO/main.py
```

2. Open your browser and navigate to `http://127.0.0.1:7860`

3. Enter a website URL in the input field and click "Submit"

4. Wait for the analysis to complete (this may take a few seconds depending on the website size)

5. Review the detailed analysis provided in the output field

## Project Structure

```
Deep-search/
├── SOCIO/
│   ├── agents.py           # Agent definitions and tracing functionality
│   ├── analyze_agent.py    # AI analysis implementation
│   ├── content_extractor.py# Website content extraction logic
│   └── main.py            # Main application and Gradio interface
├── README.md
└── requirements.txt
```

## Dependencies

- `gradio`: Web interface framework
- `openai`: AI analysis capabilities
- `beautifulsoup4`: Web scraping and content extraction
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests handling

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

## Acknowledgments

- Built with OpenAI's GPT-3.5 for intelligent content analysis
- Uses Gradio for the user interface
- BeautifulSoup4 for reliable web scraping

## Note
 
Make sure you have a valid OpenAI API key and sufficient credits for the AI analysis functionality to work properly.
