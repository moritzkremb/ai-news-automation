"""
Firecrawl Search News Fetcher Module

Uses Firecrawl Search API to find actual AI news articles from various sources.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from firecrawl import FirecrawlApp

from config import SEARCH_CONFIG


class FirecrawlSearchFetcher:
    """Fetches AI news using Firecrawl Search API to find real articles."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize Firecrawl with API key
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        
        self.app = FirecrawlApp(api_key=api_key)
        self.articles_cache = set()  # To avoid duplicates
    
    def fetch_all_news(self) -> List[Dict[str, Any]]:
        """Fetch news using Firecrawl search for different AI topics."""
        all_articles = []
        
        search_queries = SEARCH_CONFIG.get('search_queries', [])
        
        for query_config in search_queries:
            try:
                query = query_config['query']
                self.logger.info(f"Searching for: {query}")
                
                articles = self._search_news(query_config)
                all_articles.extend(articles)
                self.logger.info(f"Found {len(articles)} articles for '{query}'")
                
            except Exception as e:
                self.logger.error(f"Error searching for '{query_config.get('query', 'unknown')}': {str(e)}")
                continue
        
        # Remove duplicates and sort by relevance
        unique_articles = self._deduplicate_articles(all_articles)
        
        # Sort by AI relevance score or published date
        sorted_articles = sorted(
            unique_articles,
            key=lambda x: (x.get('ai_relevance_score', 0), x.get('published_date', datetime.min)),
            reverse=True
        )
        
        return sorted_articles[:SEARCH_CONFIG.get('max_articles', 15)]
    
    def _search_news(self, query_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for news articles using Firecrawl search API."""
        articles = []
        
        try:
            # Prepare search query with site filtering
            query = query_config['query']
            
            # Add site filtering to the query itself using Google search syntax
            if query_config.get('sites'):
                site_filters = ' OR '.join([f'site:{site}' for site in query_config['sites']])
                query = f"{query} ({site_filters})"
            
            # Prepare search parameters
            search_params = {
                'limit': query_config.get('limit', 5)
            }
            
            # Perform the search
            self.logger.debug(f"Searching with query: {query}")
            search_result = self.app.search(query, **search_params)
            
            if not hasattr(search_result, 'data') or not search_result.data:
                self.logger.warning(f"No search results found for: {query_config['query']}")
                return articles
            
            # Process each search result
            for result in search_result.data:
                article = self._process_search_result(result, query_config)
                if article:
                    articles.append(article)
                    
        except Exception as e:
            self.logger.error(f"Error in search: {str(e)}")
        
        return articles
    
    def _process_search_result(self, result, query_config: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single search result into an article."""
        try:
            # Extract data from search result dictionary
            title = result.get('title', 'No Title')
            url = result.get('url', '')
            description = result.get('description', 'No description available.')
            
            self.logger.debug(f"Processing: {title[:50]}...")
            
            # Calculate AI relevance score
            ai_relevance = self._calculate_ai_relevance(title, description)
            
            # Skip if not AI-related enough
            min_relevance = query_config.get('min_ai_relevance', 0.3)
            if ai_relevance < min_relevance:
                self.logger.debug(f"Article skipped - low AI relevance: {ai_relevance:.2f}")
                return None
            
            # Determine source from URL
            source = self._extract_source_from_url(url)
            
            return {
                'title': title,
                'link': url,
                'summary': description[:300] + "..." if len(description) > 300 else description,
                'source': source,
                'published': '',  # Search API doesn't provide published date
                'published_date': datetime.now(),  # Use current time as fallback
                'ai_relevance_score': ai_relevance,
                'content_type': 'search_result'
            }
            
        except Exception as e:
            self.logger.error(f"Error processing search result: {str(e)}")
            return None
    
    def _extract_source_from_url(self, url: str) -> str:
        """Extract source name from URL."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            
            # Map common domains to friendly names
            domain_mapping = {
                'techcrunch.com': 'TechCrunch',
                'www.technologyreview.com': 'MIT Technology Review',
                'openai.com': 'OpenAI',
                'blog.google': 'Google AI Blog',
                'deepmind.google': 'Google DeepMind',
                'www.theverge.com': 'The Verge',
                'arstechnica.com': 'Ars Technica',
                'venturebeat.com': 'VentureBeat',
                'artificialintelligence-news.com': 'AI News',
                'www.wired.com': 'Wired',
                'www.reuters.com': 'Reuters',
                'www.bloomberg.com': 'Bloomberg'
            }
            
            return domain_mapping.get(domain, domain.replace('www.', '').title())
            
        except Exception:
            return 'Unknown Source'
    
    def _calculate_ai_relevance(self, title: str, description: str) -> float:
        """Calculate AI relevance score for an article."""
        ai_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
            'AI', 'ML', 'GPT', 'LLM', 'transformer', 'generative AI', 'ChatGPT',
            'computer vision', 'natural language processing', 'NLP', 'robotics',
            'automation', 'algorithm', 'data science', 'OpenAI', 'Claude',
            'Google AI', 'DeepMind', 'Anthropic', 'autonomous', 'intelligent',
            'tech startup', 'AI model', 'training', 'inference', 'prediction'
        ]
        
        text = f"{title} {description}".lower()
        
        # Count keyword matches with weighted scoring
        matches = 0
        for keyword in ai_keywords:
            if keyword.lower() in text:
                # Give higher weight to AI-specific terms
                if keyword.lower() in ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'gpt', 'llm']:
                    matches += 3
                elif keyword.lower() in ['openai', 'deepmind', 'anthropic', 'chatgpt']:
                    matches += 2
                else:
                    matches += 1
        
        # Calculate score (0-1 range) - more lenient scoring
        score = min(matches / 8.0, 1.0)
        
        return score
    
    def _deduplicate_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate articles based on URL and title similarity."""
        unique_articles = []
        seen_urls = set()
        seen_titles = set()
        
        for article in articles:
            url = article.get('link', '')
            title = article.get('title', '').lower().strip()
            
            # Skip if we've seen this URL or very similar title
            if url in seen_urls or title in seen_titles:
                continue
            
            seen_urls.add(url)
            seen_titles.add(title)
            unique_articles.append(article)
        
        return unique_articles