from typing import Any, List

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shahnameh")

SHAHNAMEH_API_BASE = "http://127.0.0.1:8000/api/v1"
USER_AGENT = "shahnameh-mcp-server/1.0"


async def make_http_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Shahnameh API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            print(response.status_code, response.headers.get("location"))
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_chapters(title: str = None) -> Any:
    """Get all chapters of Shahnameh with their sub-chapters if exist.

    Args:
        title: If provided, filters chapters by title

    Persian explanation:
    شاهنامه فردوسی از بخش های مختلفی تشکیل شده است. اگر بخشی والد نداشت یعنی جزو بخش های اصلی کتاب است.
    هر بخش اصلی می تواند شامل زیر بخش هایی باشد
    می توان بخش ها را با عنوان آنها جستجو کرد
    """
    url = f"{SHAHNAMEH_API_BASE}/chapters"
    if title:
        url += f"?title={title}"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch chapters or no chapters found."

    return data


@mcp.tool()
async def get_chapter_by_id(id: str = None) -> Any:
    """Get a specific chapter of Shahnameh by its ID.

        Args:
            id: The id of the chapter to retrieve

        Persian explanation:
    هر بخش از شاهنامه یک شناسه یکتا دارد که با آن می توان بخش مورد نظر را دریافت کرد"""
    url = f"{SHAHNAMEH_API_BASE}/chapters/{id}"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch chapter or chapter not found."

    return data


@mcp.tool()
async def list_chapter_verses(chapter_id: str = None) -> Any:
    """List all verses of a specific chapter in the Shahnameh.

        Args:
            chapter_id: The id of the chapter to retrieve verses for

        Persian explanation:
    هر بخش از شاهنامه شامل چندین بیت است. این متد تمام بیت های یک بخش را بر می گرداند."""
    url = f"{SHAHNAMEH_API_BASE}/chapters/{chapter_id}/verses"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch verses or no verses found."

    return data


@mcp.tool()
async def list_verses_by_substrings(substrings: List[str]) -> Any:
    """
        List all verses containing all of the specified substrings.

        Args:
            Filter verses by substrings (at least one required)

        Persian explanation:
    می توان بیت های شاهنامه را با زیر رشته هایی که در آنها وجود دارد فیلتر کرد.
    این متد تمام بیت هایی که شامل تمام زیر رشته های داده شده باشد را بر می گرداند.
    """
    url = f"{SHAHNAMEH_API_BASE}/verses/search?{'&'.join(f'substrings={s}' for s in substrings)}"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch verses or no verses found."

    return data


@mcp.tool()
async def search_explanations(query: str = None) -> Any:
    """Search for explanations of the Shahnameh's chapters as vector embeddings.
        Each chapter might have multiple explanations and this method embeds the given query,
        to search for relevant explanations.

        Args:
            query: The query string to search for explanations

        Persian explanation:
    هر بخش از شاهنامه درای یک یا چند توضیح به زبان پارسی و با حالت فارسی مدرن دارد که به صورت امبدینگ در دیتابیس ذخیره شده است.
    متد حاضر یک رشته را به امبدینگ تبدیل میکند و به دنبال نزدیک ترین توضیحات می گردد و آن را باز می گرداند.
    """
    url = f"{SHAHNAMEH_API_BASE}/explanations/search?query={query}"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch explanations or no explanations found."

    return data


@mcp.tool()
async def get_verse_by_id(id: str = None) -> Any:
    """Get a specific verse of Shahnameh by its ID.

        Args:
            id: The id of the verse to retrieve

        Persian explanation:
    هر بیت از شاهنامه یک شناسه یکتا دارد که با آن می توان بیت مورد نظر را دریافت کرد"""
    url = f"{SHAHNAMEH_API_BASE}/verses/{id}"
    data = await make_http_request(url)

    if not data:
        return "Unable to fetch verse or verse not found."

    return data


if __name__ == "__main__":
    mcp.run(transport="stdio")
