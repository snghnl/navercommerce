"""Restructure data to distinguish categories from individual APIs."""
import json
import re
from pathlib import Path
from typing import List, Dict, Any


def contains_hangeul(text: str) -> bool:
    """Check if text contains any Hangeul (Korean) characters."""
    return bool(re.search(r'[가-힣]', text))


def restructure_data(flat_data: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Restructure flat data into hierarchical categories and APIs.

    Categories have Hangeul in their slugs.
    Individual APIs have English-only slugs.
    """
    categories = []
    current_category = None

    for item in flat_data:
        slug = item['slug']

        if contains_hangeul(slug):
            # This is a category
            if current_category is not None:
                # Save the previous category
                categories.append(current_category)

            # Start a new category
            current_category = {
                'name': item['name'],
                'slug': item['slug'],
                'url': item['url'],
                'file_path': item['file_path'],
                'type': 'category',
                'apis': []
            }
        else:
            # This is an individual API
            api_item = {
                'name': item['name'],
                'slug': item['slug'],
                'url': item['url'],
                'file_path': item['file_path'],
                'type': 'api'
            }

            if current_category is not None:
                # Add to current category
                current_category['apis'].append(api_item)
            else:
                # No category yet, create a default one
                if not categories or categories[0].get('slug') != '_uncategorized':
                    uncategorized = {
                        'name': 'Uncategorized',
                        'slug': '_uncategorized',
                        'url': None,
                        'file_path': None,
                        'type': 'category',
                        'apis': []
                    }
                    categories.insert(0, uncategorized)

                categories[0]['apis'].append(api_item)

    # Don't forget the last category
    if current_category is not None:
        categories.append(current_category)

    return {
        'total_categories': len(categories),
        'total_apis': sum(len(cat['apis']) for cat in categories),
        'categories': categories
    }


def create_flat_api_list(structured_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Create a flat list of only individual APIs (excluding categories)."""
    apis = []

    for category in structured_data['categories']:
        for api in category['apis']:
            apis.append({
                'name': api['name'],
                'slug': api['slug'],
                'url': api['url'],
                'file_path': api['file_path'],
                'category': category['name'],
                'category_slug': category['slug']
            })

    return apis


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    input_file = project_root / 'data' / 'structure.json'
    output_structured = project_root / 'data' / 'structure_hierarchical.json'
    output_apis_only = project_root / 'data' / 'apis_only.json'

    # Load original structure
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        flat_data = json.load(f)

    print(f"Found {len(flat_data)} total items")

    # Count categories vs APIs
    categories_count = sum(1 for item in flat_data if contains_hangeul(item['slug']))
    apis_count = sum(1 for item in flat_data if not contains_hangeul(item['slug']))

    print(f"  - Categories (Hangeul slugs): {categories_count}")
    print(f"  - Individual APIs (English slugs): {apis_count}")
    print()

    # Restructure data
    print("Restructuring data...")
    structured_data = restructure_data(flat_data)

    print(f"Created {structured_data['total_categories']} categories")
    print(f"Total APIs: {structured_data['total_apis']}")
    print()

    # Save hierarchical structure
    with open(output_structured, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved hierarchical structure to {output_structured}")

    # Create and save flat API list (for scraping)
    apis_only = create_flat_api_list(structured_data)
    with open(output_apis_only, 'w', encoding='utf-8') as f:
        json.dump(apis_only, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved APIs-only list to {output_apis_only}")
    print(f"  (Contains {len(apis_only)} individual APIs, excluding {categories_count} category pages)")
    print()

    # Show sample
    print("Sample categories with their APIs:")
    for category in structured_data['categories'][:3]:
        print(f"\n  [{category['name']}] ({len(category['apis'])} APIs)")
        for api in category['apis'][:3]:
            print(f"    - {api['name']}")
        if len(category['apis']) > 3:
            print(f"    ... and {len(category['apis']) - 3} more")


if __name__ == '__main__':
    main()
