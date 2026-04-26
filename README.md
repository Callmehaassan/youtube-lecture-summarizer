YouTube Lecture Summarizer + Report Generator
A personal AI-powered MCP (Model Context Protocol) tool that automatically fetches YouTube
lecture transcripts, summarizes them using AI, and generates professionally formatted Word
documents — all from Claude Desktop in under 30 seconds.
Built by Hassan — 4th Semester Data Science & AI Student
What It Does
Paste a YouTube URL into Claude Desktop. The tool:
1. Fetches the full transcript from YouTube (free, no API key needed)
2. Summarizes it using Groq AI (Llama 3.3-70B)
3. Generates a professional .docx Word file with formatted sections
4. Optionally adds a practice quiz with 10 MCQs and 5 short answer questions
5. Logs everything to a local history file
Features
Feature Description
Single Video Notes Paste any YouTube URL, get a formatted Word document
Quiz Generator Add 10 MCQs + 5 short answer questions to any document
Playlist Support Process an entire playlist — one doc per video + master combined doc
Urdu/Hindi Support Summarizes Urdu and Hindi lectures in English automatically
History Log Tracks all previously summarized videos locally
Custom Instructions Focus on specific topics, adjust depth, target audience
Demo
# Generate notes for a lecture
generate_notes url="https://youtube.com/watch?v=aircAruvnKk" video_title="Neural
Networks"
Sample Output
The generated Word document includes:
Title Page — Blue banner, video title, date, source URL
Overview — 3-5 sentence summary
Main Topics Covered — Organized sections with bullet points
Key Definitions — All important terms explained
Important Concepts — Formulas, algorithms, frameworks
Examples Discussed — Real examples from the lecture
Quick Review — 10 most important points
Practice Quiz (optional) — 10 MCQs + 5 short answer questions with answers
Tech Stack
Component Technology
MCP Framework MCP SDK (Anthropic)
AI Summarization Groq API — Llama 3.3-70B
Transcript Fetching youtube-transcript-api
Document Generation python-docx
Playlist Processing yt-dlp
Interface Claude Desktop App
Language Python 3.12
# Generate notes with practice quiz
generate_notes url="https://youtube.com/watch?v=aircAruvnKk" video_title="Neural
Networks" include_quiz=true
# Summarize entire playlist
summarize_playlist playlist_url="https://youtube.com/playlist?list=PLxxx"
max_videos=5
# View past summaries
show_history
Installation
1. Clone the repository
bash
git clone https://github.com/yourusername/youtube-mcp.git
cd youtube-mcp
2. Create virtual environment
bash
python -m venv .venv
.venv\Scripts\activate # Windows
3.Install dependencies
bash
pip install mcp anthropic youtube-transcript-api python-docx python-dotenv groq yt-d
4. Set up API keys
Create a .env file:
GROQ_API_KEY=your-groq-api-key-here
Get a free Groq API key at: https://console.groq.com
5. Configure Claude Desktop
Open %APPDATA%\Claude\claude_desktop_config.json and add:
json
{
"mcpServers": {
"youtube-summarizer": {
"command": "C:\\path\\to\\youtube-mcp\\.venv\\Scripts\\python.exe",
"args": ["C:\\path\\to\\youtube-mcp\\server.py"]
}
}
}
6. Restart Claude Desktop
The tools will appear automatically.
Project Structure
youtube-mcp/
server.py # Main MCP server — all tools registered here
tools/
transcript.py # YouTube transcript fetcher
summarize.py # Groq AI summarization + chunking
docx_gen.py # Word document generator
quiz.py # Quiz generator (MCQs + short answers)
playlist.py # Playlist batch processor
history.py # Local history log
output/ # Generated .docx files saved here
history.json # Local log of all processed videos
.env # API keys (never commit this)
.gitignore
Usage Examples
Basic lecture notes
generate_notes https://www.youtube.com/watch?v=aircAruvnKk "Neural Networks"
With custom focus
generate_notes https://www.youtube.com/watch?v=aircAruvnKk "Neural Networks"
custom_instructions="Focus only on the math and formulas"
With quiz
generate_notes https://www.youtube.com/watch?v=aircAruvnKk "Neural Networks"
include_quiz=true
Entire playlist
summarize_playlist https://www.youtube.com/playlist?
list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi max_videos=5
Cost
Item Cost
Groq API Free (generous free tier)
youtube-transcript-api Free
python-docx Free
yt-dlp Free
Claude Desktop Free
Total Rs. 0/month
Skills Demonstrated
MCP Tool Development — Built a custom MCP server from scratch
APIIntegration — Groq API + YouTube Transcript API in one pipeline
NLP / Text Processing — Chunking, summarization, language detection
Document Automation — python-docx pipeline for professional Word files
Prompt Engineering — Structured prompts for consistent AI output
Batch Processing — Playlist processor with error handling
Python — 6 modules, clean separation of concerns, error handling throughout
Limitations
Only works on videos with captions enabled (look for CC button on YouTube player)
Requires internet connection and Claude Desktop running locally
Free Groq API has rate limits for very heavy usage
Future Enhancements
Flashcard generator (Anki export)
Mind map generation
Cross-lecture search
PDF export
Notion integration
Author
Hassan — Data Science & AI Student, 4th Semester
Built as a personal portfolio project — April 20
