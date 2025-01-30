<div align="center">

# LinkedIn Influencer MCP 🚀
<p align="center">
  <img src="https://img.shields.io/badge/FastMCP-Powered-blue?style=for-the-badge&logo=data:image/png;base64,..." alt="FastMCP"/>
  <img src="https://img.shields.io/badge/LinkedIn-Automation-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"/>
  <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License"/>
</p>

<strong>🎯 A powerful MCP server for automating LinkedIn interactions and content analysis</strong>

## 🏗️ Architecture
![LinkedIn Influencer MCP Architecture](https://github.com/shahshrey/linkedin_influencer_mcp/blob/main/src/linkedin_influencer_mcp/assets/flow.png)

</div>

## 📖 Overview

This Model Context Protocol (MCP) server provides tools and resources for automating sending linkedin connection requests, analyzing profiles, and scraping content and posting content. Built with FastMCP, it enables Claude to perform complex LinkedIn operations. We plan on adding a lot more in future based on feedback.

## ✨ Features

### 👤 Profile Analysis
- Extract comprehensive LinkedIn profile data including name, headline, experience, education
- Analyze profile strength and engagement metrics
- Track profile changes over time
- Generate insights about professional background

### 📝 Content Management
- Create and schedule LinkedIn posts with optimal timing
- Scrape and analyze posts from target profiles
- Track post performance and engagement
- Generate content from YouTube video transcripts
- Repurpose content across platforms

### 🤝 Network Building
- Send personalized connection requests at scale
- Search and connect with specific professional groups
- Automated recruiter outreach with customized messaging
- Track connection request status and responses
- Build targeted professional networks

### ✍️ Content Generation
- AI-powered post creation using multiple LLM options
- Content repurposing from various sources (YouTube, articles, etc.)
- Writing style mimicking based on successful profiles
- SEO optimization for maximum visibility
- Hashtag optimization and trend analysis

### 🛠️ Automation Tools
- Headless browser automation with Playwright
- Robust session management and cookie handling
- Rate limiting protection
- Comprehensive error handling and recovery
- Detailed logging and monitoring

## 🔧 Available Tools

```python
# Get profile information
await get_linkedin_profile_info(linkedin_profile_id="profile_id")

# Scrape posts
await get_linkedin_profile_posts(linkedin_profile_id="profile_id", max_posts=5)

# Create a post
await create_linkedin_post(content="Your post content")

# Send connection requests
await send_linkedin_connection_requests(connection=ConnectionRequest(...))
```

## 📋 Prompt Templates

- `connection_requests_to_recruiters_prompt`: Generate personalized outreach messages to recruiters
- `connection_requests_with_custom_note`: Create tailored connection requests
- `research_and_create_post`: Research and generate authentic LinkedIn posts (Requires Brave MCP)
- `scrape_linkedin_posts_and_post_to_linkedin`: Analyze and create content from influencers
- `create_linkedin_post_from_youtube`: Convert YouTube content into LinkedIn posts (requires youtube transcript MCP)

## ⚙️ Configuration

To add this tool as an MCP server, modify your Claude desktop configuration file:

- MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "linkedin-influencer-mcp": {
    "command": "uv",
    "args": ["run", "linkedin-influencer-mcp"],
    "env": {
      "LINKEDIN_EMAIL": "your email",
      "LINKEDIN_PASSWORD": "your password",
      "GROQ_API_KEY": "GROQ API KEY, for generating custom note",
      "USER_LINKEDIN_PROFILE_ID": "your linkedin profile ID",
      "GOOGLE_API_KEY": "OPTIONAL: IF GROQ API rate limit is reached, use google",
      "OPENAI_API_KEY": "OPTIONAL: IF you need more requests,use openai"
    }
  }
}
```

## 🎯 Use Cases

### Example #1: Automated Recruiter Outreach

Use the recruiter outreach template to automatically connect with relevant recruiters:

<img width="693" alt="Recruiter Outreach Example" src="https://github.com/user-attachments/assets/PLACEHOLDER_FOR_SCREENSHOT" />

Example prompt to Claude:
```
Connect with tech recruiters in the San Francisco Bay Area who are hiring for senior software engineering roles. Personalize the message based on my experience with Python and distributed systems.
```

### Example #2: Content Creation from Research

Use the research and post creation template to generate engaging content:

Example prompt:
```
Research the latest trends in AI and create a LinkedIn post about the impact of large language models on software development. Include relevant statistics and tag key influencers in the space.
```

## 📚 Documentation
For development setup and contribution guidelines, please see [DEVELOPMENT.md](https://github.com/shahshrey/linkedin_influencer_mcp/blob/main/DEVELOPMENT.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
