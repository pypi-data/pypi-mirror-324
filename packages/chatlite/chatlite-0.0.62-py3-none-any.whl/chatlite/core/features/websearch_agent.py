from concurrent.futures import ThreadPoolExecutor

from litegen import LLM
from pydantic import Field

from .base import Feature

from fastapi import WebSocket
from visionlite import visionai

from fastapi import WebSocket
from liteutils import remove_references

from .base import Feature

import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from openai import OpenAI, api_key
import asyncio
from liteauto import web, wlsplit

from liteauto import google, wlanswer
from liteauto.parselite import aparse

from ..model_names import HUGGINGCHAT_MODELS, GPU_MODELS


def streamer(res: str):
    "simulating streaming by using streamer"
    for i in range(0, len(res), 20):
        yield res[i:i + 20]


async def handle_google_search(websocket: WebSocket, message: str):
    """Handle Google search-like responses"""
    try:
        for chunk in streamer(message):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk,
                "type": "stream"
            }))
            await asyncio.sleep(0.001)

        await websocket.send_text(json.dumps({
            "sender": "bot",
            "type": "end_stream"
        }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "message": f"Error: {str(e)}",
            "type": "error"
        }))


class WebSearchAgent(Feature):
    """Google search feature implementation"""

    async def get_web_result(self, message: str, max_urls):
        print(f'{message=}')
        print(f'{max_urls=}')

        urls = google(message, max_urls=max_urls)
        print(f'{urls=}')

        web_results = await aparse(urls)
        web_results = [w for w in web_results if w.content]

        res = ""
        for w in web_results:
            try:
                if 'arxiv' in w.url:
                    content = remove_references(w.content)
                else:
                    content = w.content
                res += f"{content}\n"
            except:
                pass
        return res

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        print(f'{kwargs=}')

        if kwargs.get("model") in HUGGINGCHAT_MODELS:
            api_key = "huggingchat"
        elif kwargs.get("model") in GPU_MODELS:
            api_key = "dsollama"
        else:
            api_key = "ollama"

        llm = LLM(api_key)

        step_result: str = await self.get_web_result(message=message, max_urls=kwargs.get("is_websearch_k"))

        answer = llm(
            f"use the realtime results : {step_result}\n\n"
            f"Answer the user question: {message}",
            model=kwargs.get("model"))

        await handle_google_search(websocket=websocket,
                                   message=answer)
