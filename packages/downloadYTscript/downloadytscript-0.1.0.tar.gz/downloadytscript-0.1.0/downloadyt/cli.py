#!/usr/bin/env python3
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """
    Extracts the YouTube video ID from a URL.
    Supports standard (watch?v=...) and shortened (youtu.be/...) formats.
    """
    patterns = [
        r"v=([^&]+)",         # e.g., https://www.youtube.com/watch?v=VIDEO_ID
        r"youtu\.be/([^?&]+)"  # e.g., https://youtu.be/VIDEO_ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: downloadYTscript <YouTube URL> [<Output File Name>]")
        sys.exit(1)
    
    url = sys.argv[1]
    video_id = extract_video_id(url)
    if not video_id:
        print("Error: Could not extract a valid video ID from the provided URL.")
        sys.exit(1)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript for video ID '{video_id}': {e}")
        sys.exit(1)
    
    # Combine transcript entries into a string with line breaks.
    transcript_text = "\n".join(entry["text"] for entry in transcript)
    
    # If an output file name is provided, use it. Otherwise, prompt the user.
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
    else:
        default_filename = f"{video_id}_transcript.txt"
        answer = input(f"Do you want to save the transcript in a '{default_filename}' file? (y/n): ").strip().lower()
        if answer in ['y', 'yes']:
            output_filename = default_filename
        else:
            output_filename = ""
    
    if output_filename:
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            print(f"Transcript saved to '{output_filename}'")
        except Exception as e:
            print(f"Error saving transcript to file: {e}")
            sys.exit(1)
    else:
        # Print transcript to console if no file is chosen.
        print(transcript_text)

if __name__ == "__main__":
    main()
