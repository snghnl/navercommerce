"""Extract links from list.html and prepare for scraping."""
import json
import re
from pathlib import Path
from typing import List, Dict
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    """Custom HTML parser to extract menu links."""

    def __init__(self):
        super().__init__()
        self.links = []
        self.current_link = None
        self.capturing_text = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'menu__link' in attrs_dict.get('class', ''):
                href = attrs_dict.get('href', '')
                # Only capture commerce-api links
                if '/docs/commerce-api/current/' in href and href != '/docs/commerce-api/current':
                    self.current_link = {
                        'href': href,
                        'text': ''
                    }
                    self.capturing_text = True

    def handle_data(self, data):
        if self.capturing_text and self.current_link:
            self.current_link['text'] += data.strip()

    def handle_endtag(self, tag):
        if tag == 'a' and self.current_link:
            if self.current_link['text']:  # Only add if we captured text
                self.links.append(self.current_link)
            self.current_link = None
            self.capturing_text = False


def extract_links_from_html(html_path: Path) -> List[Dict[str, str]]:
    """Extract all commerce API links from the HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = LinkExtractor()
    parser.feed(html_content)

    # Remove duplicates while preserving order
    seen = set()
    unique_links = []
    for link in parser.links:
        key = link['href']
        if key not in seen:
            seen.add(key)
            unique_links.append(link)

    return unique_links


def create_file_structure(links: List[Dict[str, str]], base_path: Path) -> List[Dict[str, str]]:
    """Create a structured list with file paths for saving HTML."""
    structured_data = []

    for link in links:
        # Extract the slug from href
        slug = link['href'].split('/')[-1]

        # Create a safe filename
        safe_filename = re.sub(r'[^\w\-가-힣]', '_', slug) + '.html'
        file_path = base_path / 'pages' / safe_filename

        structured_data.append({
            'name': link['text'],
            'slug': slug,
            'url': link['href'],
            'file_path': str(file_path.relative_to(base_path))
        })

    return structured_data


def main():
    """Main function to extract links and create structure."""
    # Paths
    project_root = Path(__file__).parent.parent
    html_file = project_root / 'data' / 'list.html'
    output_json = project_root / 'data' / 'structure.json'

    print(f"Extracting links from {html_file}...")
    links = extract_links_from_html(html_file)
    print(f"Found {len(links)} unique links")

    # Create structured data with file paths
    print("Creating file structure...")
    structured_data = create_file_structure(links, project_root / 'data')

    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"Saved structure to {output_json}")
    print(f"\nFirst 5 entries:")
    for entry in structured_data[:5]:
        print(f"  - {entry['name']} -> {entry['file_path']}")


if __name__ == '__main__':
    main()
