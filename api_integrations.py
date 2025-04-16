# from typing import List, Dict
# import os
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# import requests
# import json

# load_dotenv()

# class SocialMediaIntegrator:
#     def __init__(self):
#         self._init_youtube()
#         self._init_twitter()
    
#     def _init_youtube(self):
#         try:
#             api_key = 'AIzaSyB_mPsamOWVcL1vYB7Dc39AB1mmqkrHXv4'
#             if not api_key:
#                 print("Warning: YouTube API key not found in environment variables")
#                 self.youtube = None
#                 return
                
#             self.youtube = build('youtube', 'v3', developerKey=api_key)
#             print("YouTube API initialized successfully")
#         except Exception as e:
#             print(f"Error initializing YouTube API: {e}")
#             self.youtube = None
    
#     def _init_twitter(self):
#         """Initialize Twitter API client"""
#         self.twitter_bearer_token = ('AAAAAAAAAAAAAAAAAAAAAIWdzwEAAAAATAwB8L85ZlKjTw1qI5BLPGP77cE%3DuS65JtUJ6kUDcT3PFBqBIBoFHBIxfm8fE1qFbAZQ8q8R9EK4hN')
#         if not self.twitter_bearer_token:
#             print("Warning: Twitter Bearer Token not found in environment variables")
#             self.twitter_headers = None
#         else:
#             self.twitter_headers = {
#                 'Authorization': f'Bearer {self.twitter_bearer_token}',
#                 'Content-Type': 'application/json'
#             }

#     def get_youtube_comments(self, video_id: str) -> List[Dict]:
#         comments = []
#         try:
#             if not self.youtube:
#                 raise Exception("YouTube API not initialized - missing API key")
            
#             print(f"Fetching comments for video ID: {video_id}")
            
#             # First, verify if video exists
#             try:
#                 video_response = self.youtube.videos().list(
#                     part='snippet',
#                     id=video_id
#                 ).execute()
                
#                 if not video_response.get('items'):
#                     raise Exception("Video not found or is not accessible")
#             except Exception as e:
#                 print(f"Error verifying video: {e}")
#                 raise Exception(f"Could not verify video: {str(e)}")
            
#             # Get comments
#             request = self.youtube.commentThreads().list(
#                 part='snippet',
#                 videoId=video_id,
#                 textFormat='plainText',
#                 maxResults=100
#             )
            
#             response = request.execute()
            
#             if 'items' not in response:
#                 print("No comments found in response")
#                 print(f"Response content: {json.dumps(response, indent=2)}")
#                 return comments
            
#             print(f"Found {len(response['items'])} comments")
            
#             for item in response['items']:
#                 try:
#                     comment = {
#                         'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
#                         'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
#                         'platform': 'youtube',
#                         'timestamp': item['snippet']['topLevelComment']['snippet']['publishedAt']
#                     }
#                     comments.append(comment)
#                 except KeyError as e:
#                     print(f"Error parsing comment: {e}")
#                     print(f"Comment data: {json.dumps(item, indent=2)}")
#                     continue
                    
#         except Exception as e:
#             print(f"Error fetching YouTube comments: {e}")
#             raise Exception(f"Failed to fetch YouTube comments: {str(e)}")
            
#         return comments

#     def get_twitter_comments(self, tweet_id: str) -> List[Dict]:
#         """Fetch replies to a tweet using Twitter API v2"""
#         comments = []
#         try:
#             if not self.twitter_headers:
#                 raise Exception("Twitter API not initialized - missing Bearer Token")

#             # Twitter API v2 endpoint for tweet replies
#             url = f'https://api.twitter.com/2/tweets/{tweet_id}/replies'
#             params = {
#                 'tweet.fields': 'created_at',
#                 'user.fields': 'username',
#                 'max_results': 100
#             }

#             response = requests.get(url, headers=self.twitter_headers, params=params)
#             response.raise_for_status()
#             data = response.json()

#             if 'data' in data:
#                 for item in data['data']:
#                     comment = {
#                         'text': item.get('text', ''),
#                         'author': item.get('author', {}).get('username', 'Unknown'),
#                         'platform': 'twitter',
#                         'timestamp': item.get('created_at')
#                     }
#                     comments.append(comment)

#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching Twitter replies: {e}")
#             raise Exception(f"Failed to fetch Twitter replies: {str(e)}")
#         return comments

#     def extract_video_id(self, url: str) -> str:
#         """Extract YouTube video ID from URL."""
#         try:
#             if not url:
#                 return None
            
#             print(f"Extracting video ID from URL: {url}")
            
#             if 'youtu.be' in url:
#                 video_id = url.split('/')[-1].split('?')[0]
#             elif 'youtube.com' in url:
#                 from urllib.parse import urlparse, parse_qs
#                 parsed_url = urlparse(url)
#                 video_id = parse_qs(parsed_url.query).get('v', [None])[0]
#             else:
#                 video_id = None
                
#             print(f"Extracted video ID: {video_id}")
#             return video_id
            
#         except Exception as e:
#             print(f"Error extracting video ID: {e}")
#             return None

#     def extract_tweet_id(self, url: str) -> str:
#         """Extract Twitter tweet ID from URL."""
#         try:
#             if not url:
#                 return None

#             # Handle different Twitter URL formats
#             # Format 1: https://twitter.com/username/status/1234567890
#             # Format 2: https://x.com/username/status/1234567890
#             if '/status/' in url:
#                 return url.split('/status/')[-1].split('?')[0]
#             return None
#         except Exception:
#             return None

#     # Add similar methods for other platforms 

from typing import List, Dict
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import requests
import json
from urllib.parse import urlparse, parse_qs

# Load environment variables from .env file
load_dotenv()

class SocialMediaIntegrator:
    def __init__(self):
        self._init_youtube()
        self._init_twitter()
    
    def _init_youtube(self):
        try:
            api_key = ('AIzaSyB_mPsamOWVcL1vYB7Dc39AB1mmqkrHXv4')  # Load from environment
            if not api_key:
                print("Warning: YouTube API key not found in environment variables")
                self.youtube = None
                return
                
            self.youtube = build('youtube', 'v3', developerKey=api_key)
            print("YouTube API initialized successfully")
        except Exception as e:
            print(f"Error initializing YouTube API: {e}")
            self.youtube = None
    
    def _init_twitter(self):
        """Initialize Twitter API client"""
        #self.twitter_bearer_token = ('AAAAAAAAAAAAAAAAAAAAAIWdzwEAAAAATAwB8L85ZlKjTw1qI5BLPGP77cE%3DuS65JtUJ6kUDcT3PFBqBIBoFHBIxfm8fE1qFbAZQ8q8R9EK4hN')  # Load from environment
        self.twitter_bearer_token = ('AAAAAAAAAAAAAAAAAAAAAIPJzwEAAAAAeBpS522F0%2BVdqmX3JV%2Bl%2FUKxWDA%3D7g00SpMy0BymWVWD17WH2qr0VUww8CkrYI4UFDd2GpmXXUlHEy')  # Load from environment
        #self.twitter_bearer_token = ('AAAAAAAAAAAAAAAAAAAAAOTJzwEAAAAAVM5B99MIDCLREDlN2ToZoGnwqEk%3DMbmAI9khMd7mBkJO6qCIelmDBt8V1918hq1xYDkINUu8Hg1YQt')
        if not self.twitter_bearer_token:
            print("Warning: Twitter Bearer Token not found in environment variables")
            self.twitter_headers = None
        else:
            self.twitter_headers = {
                'Authorization': f'Bearer {self.twitter_bearer_token}',
                'Content-Type': 'application/json'
            }

    def get_youtube_comments(self, video_id: str) -> List[Dict]:
        comments = []
        try:
            if not self.youtube:
                raise Exception("YouTube API not initialized - missing API key")
            
            print(f"Fetching comments for video ID: {video_id}")
            
            # First, verify if video exists
            try:
                video_response = self.youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                
                if not video_response.get('items'):
                    raise Exception("Video not found or is not accessible")
            except Exception as e:
                print(f"Error verifying video: {e}")
                raise Exception(f"Could not verify video: {str(e)}")
            
            # Get comments
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100
            )
            
            response = request.execute()
            
            if 'items' not in response:
                print("No comments found in response")
                print(f"Response content: {json.dumps(response, indent=2)}")
                return comments
            
            print(f"Found {len(response['items'])} comments")
            
            for item in response['items']:
                try:
                    comment = {
                        'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'platform': 'youtube',
                        'timestamp': item['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                    comments.append(comment)
                except KeyError as e:
                    print(f"Error parsing comment: {e}")
                    print(f"Comment data: {json.dumps(item, indent=2)}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching YouTube comments: {e}")
            raise Exception(f"Failed to fetch YouTube comments: {str(e)}")
            
        return comments

    def get_twitter_comments(self, tweet_id: str) -> List[Dict]:
        """Fetch replies to a tweet using Twitter API v2"""
        comments = []
        try:
            if not self.twitter_headers:
                raise Exception("Twitter API not initialized - missing Bearer Token")

            # Use the conversation_id for the replies (Twitter API v2)
            url = 'https://api.twitter.com/2/tweets/search/recent'
            params = {
                'query': f'conversation_id:{tweet_id}',  # Query replies using the conversation ID
                'tweet.fields': 'created_at',
                'user.fields': 'username',
                'max_results': 100
            }

            response = requests.get(url, headers=self.twitter_headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'data' in data:
                for item in data['data']:
                    comment = {
                        'text': item.get('text', ''),
                        'author': item.get('author_id', 'Unknown'),  # Author ID (you can look up usernames later)
                        'platform': 'twitter',
                        'timestamp': item.get('created_at')
                    }
                    comments.append(comment)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Twitter replies: {e}")
            raise Exception(f"Failed to fetch Twitter replies: {str(e)}")
        return comments

    def extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        try:
            if not url:
                return None
            
            print(f"Extracting video ID from URL: {url}")
            
            if 'youtu.be' in url:
                video_id = url.split('/')[-1].split('?')[0]
            elif 'youtube.com' in url:
                parsed_url = urlparse(url)
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            else:
                video_id = None
                
            print(f"Extracted video ID: {video_id}")
            return video_id
            
        except Exception as e:
            print(f"Error extracting video ID: {e}")
            return None

    def extract_tweet_id(self, url: str) -> str:
        """Extract Twitter tweet ID from URL."""
        try:
            if not url:
                return None

            # Handle different Twitter URL formats
            # Format 1: https://twitter.com/username/status/1234567890
            # Format 2: https://x.com/username/status/1234567890
            if '/status/' in url:
                return url.split('/status/')[-1].split('?')[0]
            return None
        except Exception as e:
            print(f"Error extracting tweet ID: {e}")
            return None

    # Add similar methods for other platforms
