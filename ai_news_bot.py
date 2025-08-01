#!/usr/bin/env python3
"""
AI News Bot with Firecrawl Search - Daily AI News Email Automation

This script uses Firecrawl Search API to find real AI news articles and send a daily digest email.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config import EMAIL_CONFIG, SEARCH_CONFIG
from news_fetcher import FirecrawlSearchFetcher
from email_sender import EmailSender


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,  # Back to INFO level for production
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_news_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main function to run the AI news bot with Firecrawl Search."""
    logger = setup_logging()
    logger.info("Starting AI News Bot with Firecrawl Search...")
    
    try:
        # Initialize components
        news_fetcher = FirecrawlSearchFetcher()
        email_sender = EmailSender(EMAIL_CONFIG)
        
        # Search for AI news articles using Firecrawl
        logger.info("Searching for AI news articles...")
        articles = news_fetcher.fetch_all_news()
        
        if not articles:
            logger.warning("No articles found. Exiting.")
            return
        
        logger.info(f"Found {len(articles)} AI-relevant articles")
        
        # Log article titles for debugging
        for i, article in enumerate(articles[:5], 1):
            logger.info(f"  {i}. {article.get('title', 'No title')} (Score: {article.get('ai_relevance_score', 0):.2f}) - {article.get('source', 'Unknown')}")
        
        # Generate email content
        subject = f"🤖 AI News Digest - {datetime.now().strftime('%B %d, %Y')}"
        html_content = generate_email_html(articles)
        
        # Send email
        logger.info("Sending email digest...")
        email_sender.send_digest(subject, html_content)
        
        logger.info("AI News Bot with Firecrawl Search completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running AI News Bot: {str(e)}")
        # Try to send error notification email
        try:
            error_subject = f"❌ AI News Bot Error - {datetime.now().strftime('%B %d, %Y')}"
            error_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>AI News Bot Error</h2>
                <p><strong>Error:</strong> {str(e)}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Please check the logs and fix the issue.</p>
            </body>
            </html>
            """
            email_sender = EmailSender(EMAIL_CONFIG)
            email_sender.send_digest(error_subject, error_html)
        except Exception as email_error:
            logger.error(f"Failed to send error notification: {str(email_error)}")
        
        raise


def generate_email_html(articles):
    """Generate HTML content for the email digest with enhanced styling."""
    current_date = datetime.now().strftime('%B %d, %Y')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; 
                line-height: 1.6; 
                color: #333; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                background-color: #f8f9fa;
            }}
            .container {{
                background-color: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 30px 20px; 
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 16px;
            }}
            .content {{
                padding: 20px;
            }}
            .article {{ 
                background: #f8f9fa; 
                border-left: 4px solid #007bff; 
                padding: 20px; 
                margin-bottom: 20px; 
                border-radius: 0 8px 8px 0;
                transition: box-shadow 0.2s ease;
            }}
            .article:hover {{
                box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
            }}
            .article-title {{ 
                font-size: 18px; 
                font-weight: 600; 
                margin-bottom: 12px; 
                line-height: 1.4;
            }}
            .article-title a {{ 
                color: #007bff; 
                text-decoration: none; 
            }}
            .article-title a:hover {{ 
                text-decoration: underline; 
            }}
            .article-meta {{ 
                color: #666; 
                font-size: 14px; 
                margin-bottom: 12px; 
                display: flex;
                align-items: center;
                gap: 10px;
                flex-wrap: wrap;
            }}
            .article-summary {{ 
                margin-bottom: 12px; 
                color: #444;
                line-height: 1.5;
            }}
            .source {{ 
                background: #e9ecef; 
                padding: 4px 12px; 
                border-radius: 20px; 
                font-size: 12px; 
                font-weight: 500;
                color: #495057;
            }}
            .ai-score {{
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            }}
            .stats {{
                background: #e3f2fd;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                text-align: center;
            }}
            .stats h3 {{
                margin: 0 0 10px 0;
                color: #1976d2;
            }}
            .footer {{ 
                text-align: center; 
                margin-top: 30px; 
                padding: 20px;
                color: #666; 
                font-size: 14px; 
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .footer p {{
                margin: 5px 0;
            }}
            @media (max-width: 600px) {{
                body {{ padding: 10px; }}
                .header {{ padding: 20px 15px; }}
                .content {{ padding: 15px; }}
                .article {{ padding: 15px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI News Digest</h1>
                <p>{current_date}</p>
            </div>
            <div class="content">
                <div class="stats">
                    <h3>🔍 Today's AI News</h3>
                    <p><strong>{len(articles)}</strong> curated articles found using intelligent search</p>
                </div>
    """
    
    for i, article in enumerate(articles, 1):
        ai_score = article.get('ai_relevance_score', 0)
        
        html += f"""
        <div class="article">
            <div class="article-title">
                <a href="{article.get('link', '#')}" target="_blank">{article.get('title', 'No Title')}</a>
            </div>
            <div class="article-meta">
                <span class="source">{article.get('source', 'Unknown Source')}</span>
                <span class="ai-score">AI Score: {ai_score:.1f}</span>
            </div>
            <div class="article-summary">
                {article.get('summary', 'No summary available.')}
            </div>
        </div>
        """
    
    html += """
            </div>
            <div class="footer">
                <p><strong>Powered by Firecrawl Search</strong></p>
                <p>This digest was automatically generated using intelligent web search.</p>
                <p>Stay informed, stay ahead! 🚀</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    main()