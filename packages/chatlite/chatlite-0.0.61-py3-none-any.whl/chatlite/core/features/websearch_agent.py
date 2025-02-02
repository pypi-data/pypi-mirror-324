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
from openai import OpenAI
import asyncio
from liteauto import web, wlsplit

from liteauto import google, wlanswer
from liteauto.parselite import aparse


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

    async def get_web_result(self, message: str, **kwargs):
        max_urls = kwargs.get("is_websearch_k", 3)
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
                ans = wlanswer(content, message, k=kwargs.get("k", 1))
                res += f"Source: [{w.url}]\n\n{ans}\n"
                res += f"-" * 50 + "\n"
            except:
                pass
        return res

    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        llm = LLM("huggingchat")

        from pydantic import BaseModel, Field

        class UserIntent(BaseModel):
            keywords: list[str]

        class Plan(BaseModel):
            plan: list[str]

        class Insights(BaseModel):
            three_key_findings: list[str] = Field(
                description="the findings for the answer , it can also be python code found")


        message = "gguf model run  using transformers"
        planner_prompt = (
            'Given user query, create a three stage websearch step-by-step plan in simple basic english minimal step each'
            ' the User query: {message}')

        plan: Plan = llm(planner_prompt.format(message=message),
                         response_format=Plan, model='Qwen/Qwen2.5-Coder-32B-Instruct'
                         )

        key_insights = ""
        for idx, step in enumerate(plan.plan):
            kwargs['k'] = 1
            # print(f'{step=}')
            step_result: str = await self.get_web_result(message=step, kwargs=kwargs)
            insights: Insights = llm(model='Qwen/Qwen2.5-Coder-32B-Instruct',
                                     prompt=f'for [query] {step} [/query], given search result generate ONLY THREE insights , result: {step_result}',
                                     response_format=Insights)
            # print(f'{step_result=}')
            # print(insights)
            kp = "\n".join(insights.three_key_findings)
            key_insights += f'[STEP]{step}\n[INSIGHTS] {kp}\n'
            # print(f'{key_insights=}')

        answer = llm(
            f"Based on user question: {message}\n\n and the realtime resutls insgihts : {key_insights}\n, answer the user question",
            model='Qwen/Qwen2.5-Coder-32B-Instruct')

        await handle_google_search(websocket=websocket,
                                   message=answer)
