from fastapi import Request


async def add_process_token(request: Request, call_next):
    token = request.cookies.get("access_token")
    print(token)
    if token:
        request.headers.__dict__["_list"].append(
            (b"authorization", f"Bearer {token}".encode())
        )
    response = await call_next(request)
    return response
