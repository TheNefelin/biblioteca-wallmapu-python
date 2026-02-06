from fastapi import Request

def get_base_url(request: Request) -> str:
  return f"{request.url.scheme}://{request.url.netloc}{request.url.path}"

def get_static_url(request: Request) -> str:
  return f"{request.url.scheme}://{request.url.netloc}/static{request.url.path}"
