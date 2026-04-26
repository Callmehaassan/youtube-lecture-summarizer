import os
import re
import subprocess
import json
from tools.transcript import fetch_transcript
from tools.summarize import summarize_transcript
from tools.docx_gen import create_document
from tools.history import log_video


def extract_playlist_id(url: str) -> str | None:
    patterns = [
        r"youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)",
        r"youtube\.com/watch\?.*list=([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_playlist_videos(playlist_id: str) -> list:
    try:
        yt_dlp_path = r"C:\Users\hp\Desktop\youtube-mcp\.venv\Scripts\yt-dlp.exe"
        
        result = subprocess.run(
            [
                yt_dlp_path,
                "--flat-playlist",
                "--dump-json",
                f"https://www.youtube.com/playlist?list={playlist_id}"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Log output for debugging
        with open("playlist_debug.txt", "w") as f:
            f.write("STDOUT:\n" + result.stdout[:2000])
            f.write("\nSTDERR:\n" + result.stderr[:2000])
            f.write("\nRETURNCODE: " + str(result.returncode))

        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    videos.append({
                        "video_id": data.get("id", ""),
                        "title": data.get("title", "Unknown Title"),
                        "url": f"https://www.youtube.com/watch?v={data.get('id', '')}"
                    })
                except Exception:
                    continue
        return videos

    except Exception as e:
        with open("playlist_debug.txt", "w") as f:
            f.write("EXCEPTION: " + str(e))
        return []


def process_playlist(playlist_url: str, max_videos: int = 10) -> dict:
    # Write debug log
    with open("playlist_debug.txt", "w") as f:
        f.write(f"URL received: {playlist_url}\n")
    
    playlist_id = extract_playlist_id(playlist_url)
    
    with open("playlist_debug.txt", "a") as f:
        f.write(f"Playlist ID extracted: {playlist_id}\n")
    
    if not playlist_id:
        return {
            "success": False,
            "error": "Invalid playlist URL. Please provide a valid YouTube playlist link."
        }

    videos = videos[:max_videos]

    results = []
    all_summaries = []
    failed = []

    for i, video in enumerate(videos):
        try:
            transcript_result = fetch_transcript(video["url"])
            if not transcript_result["success"]:
                failed.append(f"Video {i+1} ({video['title']}): {transcript_result['error']}")
                continue

            summary_result = summarize_transcript(
                transcript_result["transcript"],
                transcript_result["word_count"]
            )
            if not summary_result["success"]:
                failed.append(f"Video {i+1} ({video['title']}): Summarization failed")
                continue

            doc_result = create_document(
                summary_result["summary"],
                video["url"],
                video["title"]
            )

            if doc_result["success"]:
                log_video(
                    video["video_id"],
                    video["title"],
                    video["url"],
                    doc_result["filepath"]
                )
                results.append({
                    "title": video["title"],
                    "filepath": doc_result["filepath"],
                    "filename": doc_result["filename"]
                })
                all_summaries.append({
                    "title": video["title"],
                    "summary": summary_result["summary"],
                    "url": video["url"]
                })

        except Exception as e:
            failed.append(f"Video {i+1} ({video['title']}): {str(e)}")
            continue

    if not results:
        return {
            "success": False,
            "error": "No videos could be processed successfully."
        }

    master_summary = ""
    for item in all_summaries:
        master_summary += f"## {item['title']}\n\n"
        master_summary += item["summary"]
        master_summary += "\n\n---\n\n"

    master_doc = create_document(
        master_summary,
        playlist_url,
        "Complete Course Notes"
    )

    return {
        "success": True,
        "processed": len(results),
        "failed": len(failed),
        "failed_details": failed,
        "individual_files": results,
        "master_file": master_doc.get("filepath", ""),
        "master_filename": master_doc.get("filename", "")
    }