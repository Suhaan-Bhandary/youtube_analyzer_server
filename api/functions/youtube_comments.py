from itertools import islice
from api.functions.text_analyzer import analyzeText
from api.functions.spam_detecter import isTextSpam
from youtube_comment_downloader import *

def fetchPostComments(youtube_video_url, total_comment_count, sort_by_most_popular=False):
    downloader = YoutubeCommentDownloader()

    # Whether to download popular (0) or recent comments (1). Defaults to 1
    sort_by = 0 if sort_by_most_popular else 1

    # Fetch the comments
    comments_iterator = downloader.get_comments_from_url(youtube_video_url, sort_by=sort_by)

    # Comments array
    comments = []

    # Show the comments
    for comment in islice(comments_iterator, total_comment_count):
        comments.append(comment)

    return comments

def getCommentsFiltered(youtube_video_url, count, sort_by_most_popular):
    comments = fetchPostComments(youtube_video_url, count, sort_by_most_popular)

    spam_comments = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in comments:
        comment_text = comment["text"]
        comment_analyze_data = analyzeText(comment_text)

        if isTextSpam(comment_text):
            spam_comments.append({
                "comment": comment,
                "analytics": comment_analyze_data
            })
            continue

        if comment_analyze_data["sentiment"] > 0:
            positive_comments.append({
                "comment": comment,
                "analytics": comment_analyze_data
            })

        elif comment_analyze_data["sentiment"] < 0:
            negative_comments.append({
                "comment": comment,
                "analytics": comment_analyze_data
            })
        else:
            neutral_comments.append({
                "comment": comment,
                "analytics": comment_analyze_data
            })

    return {
        "spam_comments": spam_comments,
        "positive_comments": positive_comments,
        "negative_comments": negative_comments,
        "neutral_comments": neutral_comments,
    }

