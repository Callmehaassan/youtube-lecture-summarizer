from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from tools.transcript import fetch_transcript
from tools.summarize import summarize_transcript
from tools.docx_gen import create_document, add_quiz_to_document
from tools.history import log_video, format_history_list, find_by_video_id
from tools.quiz import generate_quiz
from tools.playlist import process_playlist
import re

load_dotenv()

mcp = FastMCP("youtube-summarizer")


def extract_video_id(url: str) -> str:
    patterns = [
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return "unknown"


@mcp.tool()
def echo(message: str) -> str:
    """Echo back a message to test the MCP connection."""
    return f"MCP server is working! You said: {message}"


@mcp.tool()
def get_transcript(url: str) -> str:
    """Fetch the full transcript of a YouTube video."""
    result = fetch_transcript(url)
    if not result["success"]:
        return f"Error: {result['error']}"
    return (
        f"Transcript fetched successfully!\n"
        f"Video ID: {result['video_id']}\n"
        f"Language: {result['language']}\n"
        f"Word count: {result['word_count']}"
    )


@mcp.tool()
def generate_notes(url: str, video_title: str = "YouTube Lecture", custom_instructions: str = "", include_quiz: bool = False) -> str:
    """
    Fetch, summarize, and save a YouTube lecture as a Word document.
    Set include_quiz=true to add practice questions at the end.
    Example: generate_notes url="https://youtube.com/watch?v=xxx" video_title="My Lecture" include_quiz=true
    """
    video_id = extract_video_id(url)
    existing = find_by_video_id(video_id)
    if existing:
        notice = f"Note: I already summarized this on {existing['date']}. Generating fresh copy.\n\n"
    else:
        notice = ""

    transcript_result = fetch_transcript(url)
    if not transcript_result["success"]:
        return f"Error fetching transcript: {transcript_result['error']}"

    summary_result = summarize_transcript(
        transcript_result["transcript"],
        transcript_result["word_count"],
        custom_instructions
    )
    if not summary_result["success"]:
        return f"Error summarizing: {summary_result['error']}"

    doc_result = create_document(
        summary_result["summary"],
        url,
        video_title
    )
    if not doc_result["success"]:
        return f"Error creating document: {doc_result['error']}"

    quiz_status = ""
    if include_quiz:
        quiz_result = generate_quiz(summary_result["summary"])
        if quiz_result["success"]:
            add_quiz_to_document(doc_result["filepath"], quiz_result["quiz"])
            quiz_status = "\nQuiz with 10 MCQs and 5 short answer questions added to document."
        else:
            quiz_status = f"\nQuiz generation failed: {quiz_result['error']}"

    log_video(video_id, video_title, url, doc_result["filepath"])

    return (
        f"{notice}"
        f"Done! Your lecture notes have been saved.\n\n"
        f"File: {doc_result['filename']}\n"
        f"Location: {doc_result['filepath']}"
        f"{quiz_status}\n\n"
        f"Here is the summary:\n\n{summary_result['summary']}"
    )


@mcp.tool()
def show_history() -> str:
    """Show all previously summarized lectures."""
    return format_history_list()


@mcp.tool()
def summarize_playlist(playlist_url: str, max_videos: int = 5) -> str:
    """
    Summarize an entire YouTube playlist.
    Creates one Word document per video plus one master combined document.
    Example: summarize_playlist playlist_url="https://youtube.com/playlist?list=xxx" max_videos=5
    """
    result = process_playlist(playlist_url, max_videos)

    if not result["success"]:
        return f"Error: {result['error']}"

    output = "Playlist processing complete!\n\n"
    output += f"Successfully processed: {result['processed']} videos\n"

    if result["failed"] > 0:
        output += f"Failed: {result['failed']} videos\n"
        for detail in result["failed_details"]:
            output += f"  - {detail}\n"

    output += "\nIndividual files:\n"
    for i, f in enumerate(result["individual_files"], 1):
        output += f"  {i}. {f['title']}\n"
        output += f"     {f['filepath']}\n"

    output += "\nMaster combined file:\n"
    output += f"  {result['master_file']}\n"

    return output


if __name__ == "__main__":
    mcp.run()