"""
Configuration file for AI News Bot

Contains search queries, email settings, and other configuration options.
"""

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    # Email credentials are loaded from environment variables:
    # SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL
}

# Firecrawl Search Configuration (better for finding actual articles)
SEARCH_CONFIG = {
    'max_articles': 15,
    'search_queries': [
        {
            'query': 'artificial intelligence news',
            'limit': 4,
            'min_ai_relevance': 0.4,
            'sites': ['techcrunch.com', 'www.technologyreview.com', 'www.theverge.com']
        },
        {
            'query': 'OpenAI ChatGPT GPT news',
            'limit': 3,
            'min_ai_relevance': 0.5,
            'sites': ['techcrunch.com', 'www.reuters.com', 'www.bloomberg.com']
        },
        {
            'query': 'Google AI Gemini DeepMind',
            'limit': 3,
            'min_ai_relevance': 0.4,
            'sites': ['blog.google', 'techcrunch.com', 'www.theverge.com']
        },
        {
            'query': 'machine learning AI startups funding',
            'limit': 2,
            'min_ai_relevance': 0.3,
            'sites': ['techcrunch.com', 'venturebeat.com']
        },
        {
            'query': 'AI regulation policy government',
            'limit': 2,
            'min_ai_relevance': 0.3,
            'sites': ['www.reuters.com', 'www.technologyreview.com']
        },
        {
            'query': 'AI research breakthrough science',
            'limit': 2,
            'min_ai_relevance': 0.4,
            'sites': ['www.technologyreview.com', 'arstechnica.com']
        }
    ]
}