# Naver Commerce SDK for Python

A production-grade Python SDK for the [Naver Commerce API](https://commerce.naver.com/), providing type-safe, developer-friendly access to Naver's e-commerce platform with both synchronous and asynchronous support.

## Features

- **🔐 OAuth 2.0 Authentication**: Automatic token management with refresh
- **🔄 Sync & Async Support**: Use synchronous or asynchronous clients based on your needs
- **📝 Type-Safe**: Full type hints and Pydantic models for IDE autocomplete and validation
- **🔁 Auto-Retry**: Exponential backoff retry logic for transient failures
- **🎯 Resource-Based**: Clean, intuitive API organized by resource types
- **⚠️ Comprehensive Error Handling**: Detailed exceptions mapped to Naver error codes
- **🧪 Well-Tested**: Extensive test coverage with respx for HTTP mocking

## Installation

```bash
pip install navercommerce
```

Or using uv:
```bash
uv add navercommerce
```

## Quick Start

### Synchronous Usage

```python
from navercommerce import NaverCommerce

# Initialize client with credentials
client = NaverCommerce(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Get seller information
account = client.seller.account()
print(f"Seller: {account.seller_name}")

# List sales channels
channels = client.seller.channels()
for channel in channels:
    print(f"Channel: {channel.channel_name}")
```

### Asynchronous Usage

```python
import asyncio
from navercommerce import AsyncNaverCommerce

async def main():
    async with AsyncNaverCommerce(
        client_id="your_client_id",
        client_secret="your_client_secret"
    ) as client:
        # Get seller information
        account = await client.seller.account()
        print(f"Seller: {account.seller_name}")

        # List sales channels
        channels = await client.seller.channels()
        for channel in channels:
            print(f"Channel: {channel.channel_name}")

asyncio.run(main())
```

### Environment Variables

You can also set credentials via environment variables:

```bash
export NAVER_CLIENT_ID="your_client_id"
export NAVER_CLIENT_SECRET="your_client_secret"
```

Then initialize without parameters:
```python
client = NaverCommerce()  # Reads from environment
```

## Available Resources

### Seller Resource

Access seller account information, channels, and address book:

```python
# Get account information
account = client.seller.account()

# Get sales channels
channels = client.seller.channels()

# Get address book
addresses = client.seller.addresses()
```

### Products Resource

Manage products, categories, and brands:

```python
# Create a product
product = client.products.create(
    name="Product Name",
    sale_price=29900,
    category_id="50000000",
    origin_area_code="01",  # Korea
    stock_quantity=100,
    status="SALE"
)

# Retrieve product
product = client.products.retrieve("product_id")
print(f"Product: {product.name}")
print(f"Price: {product.sale_price}원")

# Update product
product = client.products.update(
    "product_id",
    name="New Product Name",
    sale_price=34900
)

# Delete product
client.products.delete("product_id")

# List products with pagination
products = client.products.list(page=1, size=20)
for product in products:
    print(f"{product.name}: {product.sale_price}원")

# Browse categories
categories = client.products.list_categories()
for category in categories:
    print(f"Category: {category.name}")

# Get specific category
category = client.products.get_category("50000000")

# List brands
brands = client.products.list_brands(page=1, size=50)
for brand in brands:
    print(f"Brand: {brand.name}")
```

### Orders Resource (Coming Soon)

Manage orders, confirmations, and shipping:

```python
# List orders
orders = client.orders.list(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Get order details
order = client.orders.retrieve("order_id")

# Confirm order
client.orders.confirm(product_order_ids=["order1", "order2"])

# Ship order
client.orders.ship(
    product_order_ids=["order1"],
    tracking_info={...}
)
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from navercommerce import (
    NaverCommerce,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    InternalServerError
)

client = NaverCommerce()

try:
    account = client.seller.account()
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Error code: {e.code}")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
    print(f"Invalid fields: {e.invalid_inputs}")
except NotFoundError as e:
    print(f"Resource not found: {e.message}")
except InternalServerError as e:
    print(f"Server error: {e.message}")
```

### Exception Hierarchy

```
NaverCommerceError (base)
├── APIError
│   ├── APIConnectionError
│   ├── APITimeoutError
│   └── APIStatusError
│       ├── BadRequestError (400)
│       ├── AuthenticationError (401)
│       ├── PermissionDeniedError (403)
│       ├── NotFoundError (404)
│       └── InternalServerError (500)
└── OAuthError
    ├── TokenExpiredError
    └── TokenRefreshError
```

## Configuration

### Timeout

Set custom timeout for requests:

```python
client = NaverCommerce(
    client_id="...",
    client_secret="...",
    timeout=120  # 120 seconds
)
```

### Max Retries

Configure retry behavior:

```python
client = NaverCommerce(
    client_id="...",
    client_secret="...",
    max_retries=3  # Retry up to 3 times
)
```

### Base URL

Override the base URL (useful for testing):

```python
client = NaverCommerce(
    client_id="...",
    client_secret="...",
    base_url="https://custom.api.url"
)
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/navercommerce.git
cd navercommerce
```

2. Install dependencies:
```bash
uv sync --extra dev
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=navercommerce tests/

# Run specific test file
uv run pytest tests/test_client_basic.py -v
```

### Type Checking

```bash
# Run pyright
uv run pyright src/

# Run mypy
uv run mypy src/
```

### Linting

```bash
# Check with ruff
uv run ruff check src/

# Auto-fix issues
uv run ruff check --fix src/
```

## Architecture

The SDK follows a 3-tier layered architecture inspired by the OpenAI Python SDK:

```
BaseClient (HTTP, OAuth, retry logic)
  ├─ SyncAPIClient
  │   └─ NaverCommerce (main sync client)
  └─ AsyncAPIClient
      └─ AsyncNaverCommerce (main async client)
```

### Key Components

- **OAuth Token Manager**: Automatic token refresh with thread-safe caching
- **Base Client**: HTTP communication with retry logic and error handling
- **Resource Classes**: Clean separation of API endpoints by resource type
- **Type Models**: Pydantic models for request/response validation
- **Exception Hierarchy**: Detailed error types mapped to Naver error codes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Architecture inspired by the [OpenAI Python SDK](https://github.com/openai/openai-python)
- Built with [httpx](https://www.python-httpx.org/), [Pydantic](https://docs.pydantic.dev/), and [anyio](https://anyio.readthedocs.io/)

## Links

- [Naver Commerce API Documentation](https://commerce.naver.com/)
- [Issue Tracker](https://github.com/yourusername/navercommerce/issues)
- [PyPI Package](https://pypi.org/project/navercommerce/)

## Status

**Current Version**: 0.1.0 (Alpha)

Currently implemented:
- ✅ Core infrastructure (auth, retry, error handling)
- ✅ Seller resource (account, channels, address book)
- ✅ Products resource (full CRUD, categories, brands)
- 🚧 Orders resource (in progress)

Coming soon:
- Orders resource (list, retrieve, confirm, ship)
- Product image uploads
- Analytics resource
- Settlement resource
- Comprehensive test coverage with API mocking
