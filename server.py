#!/usr/bin/env python3
"""Simple Flask web interface for YouTube downloads."""

import os
from flask import Flask, render_template_string, request, send_file, redirect, url_for

try:
    from pytubefix import Search
except ImportError:
    Search = None

from download import YouTubeDownloader

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <title>YouTube Downloader</title>
</head>
<body class="p-4">
  <form method="get" class="mb-4">
    <input class="border p-2 rounded" type="text" name="q" placeholder="Search" value="{{ query or '' }}">
    <button class="ml-2 bg-blue-500 text-white px-4 py-2 rounded" type="submit">Search</button>
  </form>
  {% if results %}
  <ul>
    {% for r in results %}
    <li class="mb-4 flex">
      <img src="{{ r['thumbnail'] }}" class="w-32 h-24 mr-4" />
      <div>
        <p class="font-semibold">{{ r['title'] }}</p>
        <a class="text-blue-500" href="/download?video_id={{ r['id'] }}&type=audio">Audio</a>
        <span class="mx-2">|</span>
        <a class="text-blue-500" href="/download?video_id={{ r['id'] }}&type=video">Video</a>
      </div>
    </li>
    {% endfor %}
  </ul>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    results = []
    if query and Search:
        try:
            search = Search(query)
            videos = search.results[:10]
            for v in videos:
                results.append({
                    "id": v.video_id,
                    "title": v.title,
                    "thumbnail": v.thumbnail_url,
                })
        except Exception as e:
            print(f"Search error: {e}")
    return render_template_string(TEMPLATE, results=results, query=query)

@app.route("/download")
def download_route():
    video_id = request.args.get("video_id")
    media_type = request.args.get("type", "audio")
    if not video_id:
        return redirect(url_for("index"))
    url = f"https://www.youtube.com/watch?v={video_id}"
    downloader = YouTubeDownloader(url=url, media_type=media_type)
    downloader.download()
    filename = f"{downloader.title}.mp3" if media_type == "audio" else f"{downloader.title}.mp4"
    filepath = os.path.join("outputs", media_type, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
