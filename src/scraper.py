"""Scrape Naver Commerce API documentation pages."""
import asyncio
import json
from pathlib import Path
from typing import List, Dict
import httpx


BASE_URL = "https://apicenter.commerce.naver.com"


async def test_static_scraping(url: str) -> bool:
    """Test if a page can be scraped without JavaScript."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=30.0)
            if response.status_code == 200:
                html = response.text
                # Check if the page has meaningful content
                # If it's mostly empty or has a loading div, we need JS
                if len(html) > 5000 and 'class="theme-doc-markdown' in html:
                    return True
            return False
        except Exception as e:
            print(f"Error testing static scraping: {e}")
            return False


async def scrape_page_httpx(url: str) -> str:
    """Scrape a page using httpx (static scraping)."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text


async def scrape_page_playwright(url: str):
    """Scrape a page using Playwright (dynamic scraping)."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise ImportError(
            "Playwright is not installed. Install it with: "
            "pip install playwright && playwright install"
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait for the main content to load
            await page.wait_for_selector('.theme-doc-markdown', timeout=10000)
            html = await page.content()
            return html
        finally:
            await browser.close()


async def scrape_with_retry(
    url: str,
    use_playwright: bool,
    max_retries: int = 3
) -> str:
    """Scrape a page with retry logic."""
    for attempt in range(max_retries):
        try:
            if use_playwright:
                return await scrape_page_playwright(url)
            else:
                return await scrape_page_httpx(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"  Retry {attempt + 1}/{max_retries} for {url}: {e}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff


async def scrape_all_pages(
    structure: List[Dict[str, str]],
    output_dir: Path,
    use_playwright: bool = False,
    batch_size: int = 5
):
    """Scrape all pages and save to HTML files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scraping {len(structure)} pages...")
    print(f"Method: {'Playwright (dynamic)' if use_playwright else 'httpx (static)'}")
    print(f"Batch size: {batch_size}")
    print()

    successful = 0
    failed = []

    # Process in batches to avoid overwhelming the server
    for i in range(0, len(structure), batch_size):
        batch = structure[i:i + batch_size]
        tasks = []

        for entry in batch:
            url = BASE_URL + entry['url']
            file_path = output_dir.parent / entry['file_path']
            tasks.append(scrape_and_save(url, file_path, entry['name'], use_playwright))

        # Run batch concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for entry, result in zip(batch, results):
            if isinstance(result, Exception):
                failed.append({
                    'name': entry['name'],
                    'url': entry['url'],
                    'error': str(result)
                })
                print(f"✗ Failed: {entry['name']}")
            else:
                successful += 1
                print(f"✓ [{successful}/{len(structure)}] {entry['name']}")

        # Small delay between batches
        if i + batch_size < len(structure):
            await asyncio.sleep(1)

    print()
    print(f"Completed: {successful}/{len(structure)} successful")
    if failed:
        print(f"Failed: {len(failed)} pages")
        failed_file = output_dir.parent / 'failed_pages.json'
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)
        print(f"Failed pages saved to {failed_file}")


async def scrape_and_save(url: str, file_path: Path, name: str, use_playwright: bool):
    """Scrape a single page and save to file."""
    html = await scrape_with_retry(url, use_playwright)

    # Create directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save HTML
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)


async def main():
    """Main function."""
    import sys

    project_root = Path(__file__).parent.parent

    # Choose which file to use
    if len(sys.argv) > 1 and sys.argv[1] == '--apis-only':
        structure_file = project_root / 'data' / 'apis_only.json'
        print("Using APIs-only list (excluding category pages)")
    else:
        structure_file = project_root / 'data' / 'structure.json'
        print("Using full structure (includes category pages)")

    output_dir = project_root / 'data' / 'pages'

    # Load structure
    with open(structure_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    print(f"Loaded {len(structure)} pages from structure.json")
    print()

    # Test if we need Playwright
    print("Testing if static scraping works...")
    test_url = BASE_URL + structure[0]['url']
    use_playwright = not await test_static_scraping(test_url)

    if use_playwright:
        print("⚠️  Static scraping insufficient. Will use Playwright.")
        print("   Make sure Playwright is installed:")
        print("   pip install playwright && playwright install")
        print()
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("❌ Playwright not found. Please install it first.")
            return
    else:
        print("✓ Static scraping works! Using httpx.")
        print()

    # Scrape all pages
    await scrape_all_pages(structure, output_dir, use_playwright, batch_size=5)


if __name__ == '__main__':
    asyncio.run(main())
