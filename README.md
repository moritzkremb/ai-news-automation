# AI News Email Automation

A Python-based automation that intelligently searches for the latest AI news articles and sends you a daily email digest.

## Features

- 🔍 **Smart Search**: Uses Firecrawl Search API to find real AI news articles
- 📰 **Quality Sources**: Searches TechCrunch, MIT Tech Review, Reuters, Bloomberg, and more
- 🤖 **AI Relevance Scoring**: Filters articles by AI relevance to ensure quality content
- 📧 **Beautiful Email Digests**: Sends professionally formatted HTML emails
- 🔄 **Automated Daily Scheduling**: Set-and-forget automation via GitHub Actions
- 🚫 **Duplicate Detection**: Smart deduplication by URL and title
- 🔒 **Secure**: Environment-based credential management

## Quick Setup

### 1. Clone and Install

```bash
cd ai-news-automation
pip install -r requirements.txt
```

### 2. Get API Keys

1. **Firecrawl API Key** (for news search):
   - Sign up at [firecrawl.dev](https://firecrawl.dev/)
   - Get your free API key (starts with `fc-`)

2. **Gmail App Password** (for email sending):
   - Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
   - Enable 2-factor authentication first
   - Generate a 16-character app password

### 3. Configure Environment

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your details:
   ```env
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-16-character-app-password
   RECIPIENT_EMAIL=recipient@example.com
   FIRECRAWL_API_KEY=fc-your-api-key-here
   ```

### 4. Test the Setup

```bash
python ai_news_bot.py
```

You should see output like:
```
Found 12 AI-relevant articles
  1. OpenAI announces new GPT model (Score: 0.9) - TechCrunch
  2. Google's latest AI breakthrough (Score: 0.8) - MIT Technology Review
  ...
Sending email digest...
AI News Bot completed successfully!
```

## Automated Daily Emails

### Option 1: GitHub Actions (Recommended)

1. Push this code to a GitHub repository
2. Add these secrets in GitHub Settings → Secrets and variables → Actions:
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD` 
   - `RECIPIENT_EMAIL`
   - `FIRECRAWL_API_KEY`
3. The workflow runs daily at 8 AM UTC automatically!

### Option 2: Local Cron Job

Add to your crontab (`crontab -e`):
```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/ai-news-automation && python ai_news_bot.py
```

## Customization

### Adding Search Queries

Edit `config.py` to add more search queries:

```python
SEARCH_CONFIG['search_queries'].append({
    'query': 'AI robotics automation',
    'limit': 3,
    'min_ai_relevance': 0.4,
    'sites': ['techcrunch.com', 'www.theverge.com']
})
```

### Adjusting Settings

In `config.py`:
- `max_articles`: Number of articles in digest (default: 15)
- `min_ai_relevance`: AI relevance threshold (0.0-1.0)
- `limit`: Results per search query

### Changing Schedule

Edit `.github/workflows/daily-news.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC
```

## Troubleshooting

### Common Issues

- **No articles found**: Check Firecrawl API key and account limits
- **Email authentication failed**: Use Gmail App Password, enable 2FA first
- **API rate limits**: Firecrawl free tier has daily limits
- **Low relevance scores**: Adjust `min_ai_relevance` in search queries

### Logs
Check `ai_news_bot.log` for detailed error information.

### Testing
Run with debug logging: Change `logging.INFO` to `logging.DEBUG` in `ai_news_bot.py`

## File Structure

```
ai-news-automation/
├── ai_news_bot.py          # Main application
├── config.py               # Search queries and settings
├── email_sender.py         # Email functionality  
├── news_fetcher.py         # Firecrawl search integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .github/workflows/
│   └── daily-news.yml     # GitHub Actions automation
└── README.md              # This file
```

## Search Sources

The bot intelligently searches these trusted sources:
- **TechCrunch** - AI startup news and funding
- **MIT Technology Review** - In-depth AI research and analysis
- **Reuters** - Breaking AI news and policy updates
- **Bloomberg** - AI business and market news
- **Google AI Blog** - Official Google AI updates
- **The Verge** - Consumer AI technology news
- **Ars Technica** - Technical AI developments

## Requirements

- Python 3.8+
- Firecrawl API account (free tier available)
- Gmail account with App Password enabled
- Internet connection

## License

This project is for personal/educational use. Please respect the terms of service of Firecrawl, news sources, and email providers.