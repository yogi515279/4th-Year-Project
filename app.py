from flask import Flask, render_template, request, jsonify
from model_service import CyberBullyingDetector
from api_integrations import SocialMediaIntegrator
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
detector = CyberBullyingDetector()
social_media = SocialMediaIntegrator()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/analyze_youtube', methods=['POST'])
def analyze_youtube():
    try:
        video_url = request.form.get('video_url')
        print(f"Received URL: {video_url}")
        
        if not video_url:
            return render_template('report.html', 
                                error="Please provide a YouTube URL",
                                active_tab='youtube')
        
        video_id = social_media.extract_video_id(video_url)
        print(f"Extracted video ID: {video_id}")
        
        if not video_id:
            return render_template('report.html', 
                                error="Could not extract video ID from URL. Please make sure it's a valid YouTube URL.",
                                active_tab='youtube')
        
        try:
            print("Fetching comments...")
            comments = social_media.get_youtube_comments(video_id)
            print(f"Fetched {len(comments)} comments")
            
            if not comments:
                return render_template('report.html',
                                    error="No comments found for this video. The video might have comments disabled.",
                                    active_tab='youtube')
            
            results = []
            print("Analyzing comments...")
            
            for comment in comments:
                try:
                    analysis = detector.analyze_text(comment['text'])
                    result = {
                        'text': comment['text'],
                        'author': comment['author'],
                        'analysis': analysis,
                        'timestamp': comment['timestamp']
                    }
                    results.append(result)
                except Exception as e:
                    print(f"Error analyzing comment: {e}")
                    continue
            
            print(f"Analysis complete. Found {len(results)} results")
            
            return render_template('report.html', 
                                youtube_results=results, 
                                video_url=video_url,
                                active_tab='youtube')
                                
        except Exception as e:
            print(f"Error in comment analysis: {e}")
            return render_template('report.html', 
                                error=f"Error analyzing comments: {str(e)}",
                                active_tab='youtube')
                                
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('report.html', 
                            error=f"An unexpected error occurred: {str(e)}",
                            active_tab='youtube')

@app.route('/analyze_twitter', methods=['POST'])
def analyze_twitter():
    tweet_url = request.form.get('tweet_url')
    tweet_id = social_media.extract_tweet_id(tweet_url)
    
    if not tweet_id:
        return render_template('report.html', 
                             error="Invalid Twitter URL format. Please provide a valid tweet URL.",
                             active_tab='twitter')
    
    try:
        comments = social_media.get_twitter_comments(tweet_id)
        results = []
        
        for comment in comments:
            analysis = detector.analyze_text(comment['text'])
            results.append({
                'text': comment['text'],
                'author': comment['author'],
                'analysis': analysis,
                'timestamp': comment['timestamp']
            })
        
        return render_template('report.html', 
                             twitter_results=results, 
                             tweet_url=tweet_url,
                             active_tab='twitter')
    except Exception as e:
        return render_template('report.html', 
                             error=f"Error analyzing Twitter replies: {str(e)}",
                             active_tab='twitter')

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    text = request.form.get('text')
    
    if not text:
        return render_template('report.html', 
                             error="Please enter some text",
                             active_tab='manual')
     
    try:
        analysis = detector.analyze_text(text)
        return render_template('report.html', 
                             manual_result=analysis, 
                             analyzed_text=text,
                             active_tab='manual')
    except Exception as e:
        return render_template('report.html', 
                             error=f"Error analyzing text: {str(e)}",
                             active_tab='manual')

if __name__ == '__main__':
    app.run(debug=False) 