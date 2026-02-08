from fastapi import Request

def get_base_url(request: Request) -> str:
  return f"{request.url.scheme}://{request.url.netloc}"

def get_static_news_url(request: Request) -> str:
  return f"{get_base_url(request)}/static/news"
