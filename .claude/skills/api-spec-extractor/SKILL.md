---
name: api-spec-extractor
description: Extract and convert plain text API specifications into structured OpenAPI/Swagger JSON format. Use when processing API documentation, converting unstructured API specs to OpenAPI, or when the user provides plain text API specifications with endpoints, parameters, and response schemas. Supports Korean, English, and multi-language API documentation.
---

# API Specification Extractor

Converts plain text API specifications (including Korean documentation) into structured OpenAPI 3.0 JSON format.

## When to use this Skill

Use this Skill when:
- User provides plain text API documentation
- Converting unstructured API specs to OpenAPI format
- Processing API specifications in Korean or other languages
- Extracting endpoint details, request parameters, and response schemas

## Instructions

### Step 1: Parse the input text

Analyze the plain text input to identify these components:

1. **Title/Summary**: The API operation name (e.g., "인증 토큰 발급 요청")
2. **HTTP Method**: GET, POST, PUT, DELETE, PATCH, etc.
3. **Endpoint**: The API path (e.g., `/v1/oauth2/token`)
4. **Description**: Explanatory text about what the API does
5. **Request section**:
   - Content type (e.g., `application/x-www-form-urlencoded`, `application/json`)
   - Parameters with:
     - Name
     - Type (string, integer, boolean, object, array)
     - Required/optional status
     - Description
     - Example values
6. **Response section**:
   - Status codes (200, 400, 403, 500, etc.)
   - Response content type
   - Schema with properties, types, descriptions

### Step 2: Structure the data

Convert the extracted information into OpenAPI 3.0 format:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "API Specification",
    "version": "1.0.0"
  },
  "paths": {
    "/endpoint/path": {
      "method": {
        "summary": "Operation title",
        "description": "Detailed description",
        "requestBody": {
          "required": true,
          "content": {
            "content-type": {
              "schema": {
                "type": "object",
                "required": ["field1", "field2"],
                "properties": {
                  "field1": {
                    "type": "string",
                    "description": "Field description",
                    "example": "example value"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "field1": {
                      "type": "string",
                      "description": "Response field"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Step 3: Handle data types

Map common type descriptions to OpenAPI types:

- `string` → "string"
- `integer`, `int64`, `int32` → "integer" with format
- `boolean`, `bool` → "boolean"
- `number`, `float`, `double` → "number" with format
- `array` → "array" with items schema
- `object` → "object" with properties

### Step 4: Extract required fields

Identify required fields by looking for:
- Explicit "required" markers
- Korean markers: "필수", "required"
- Position of "required" near parameter name

Optional fields should NOT be in the `required` array.

### Step 5: Handle examples

Extract example values from:
- "Example: value" patterns
- Inline examples in descriptions
- Sample values in the text

Place examples in the `example` field of each property.

### Step 6: Map response codes

Extract all response status codes mentioned:
- 200: Success responses
- 400: Bad request/validation errors
- 403: Forbidden/authentication errors
- 500: Server errors
- Any other codes mentioned

### Step 7: Preserve descriptions

Keep all description text, including:
- Multi-line descriptions
- Korean text
- Special notes or constraints
- Valid time periods or limitations

### Step 8: Output clean JSON

Return the complete OpenAPI JSON with:
- Proper indentation (2 spaces)
- All extracted fields populated
- Valid JSON structure
- UTF-8 encoding for Korean/international text

## Example transformation

**Input:**
```
인증 토큰 발급 요청
POST
/v1/oauth2/token

API 활용을 위한 인증 토큰을 발급/갱신 요청합니다.

Request
application/x-www-form-urlencoded
Body required
client_id
string
required
제공된 애플리케이션 ID

Example: 7dMvteboKNHwyRremLXXXX
timestamp
integer<int64>
required
전자서명 생성 시 사용된 밀리초(millisecond) 단위의 Unix 시간. 5분간 유효

Example: 1706671059230
grant_type
string
required
OAuth2 인증 방식.
- 고정값 client_credentials 사용

Example: client_ccp_2sRZTWJVbDtHPoz9OXXXX

Responses
200
400
403
500
발급 성공 결과

application/json
Schema
access_token
string
인증 토큰

expires_in
integer<int64>
인증 유효 기간(초)

token_type
string
인증 토큰 종류
```

**Output:**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "API Specification",
    "version": "1.0.0"
  },
  "paths": {
    "/v1/oauth2/token": {
      "post": {
        "summary": "인증 토큰 발급 요청",
        "description": "API 활용을 위한 인증 토큰을 발급/갱신 요청합니다.",
        "requestBody": {
          "required": true,
          "content": {
            "application/x-www-form-urlencoded": {
              "schema": {
                "type": "object",
                "required": ["client_id", "timestamp", "grant_type"],
                "properties": {
                  "client_id": {
                    "type": "string",
                    "description": "제공된 애플리케이션 ID",
                    "example": "7dMvteboKNHwyRremLXXXX"
                  },
                  "timestamp": {
                    "type": "integer",
                    "format": "int64",
                    "description": "전자서명 생성 시 사용된 밀리초(millisecond) 단위의 Unix 시간. 5분간 유효",
                    "example": 1706671059230
                  },
                  "grant_type": {
                    "type": "string",
                    "description": "OAuth2 인증 방식.\n- 고정값 client_credentials 사용",
                    "example": "client_ccp_2sRZTWJVbDtHPoz9OXXXX"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "발급 성공 결과",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "access_token": {
                      "type": "string",
                      "description": "인증 토큰"
                    },
                    "expires_in": {
                      "type": "integer",
                      "format": "int64",
                      "description": "인증 유효 기간(초)"
                    },
                    "token_type": {
                      "type": "string",
                      "description": "인증 토큰 종류"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Bad Request"
          },
          "403": {
            "description": "Forbidden"
          },
          "500": {
            "description": "Internal Server Error"
          }
        }
      }
    }
  }
}
```

## Best practices

1. **Preserve all information**: Don't lose details from the original text
2. **Handle multi-language**: Support Korean, English, and mixed content
3. **Extract all parameters**: Include all request and response fields
4. **Map types correctly**: Use proper OpenAPI types and formats
5. **Required vs optional**: Accurately identify required fields
6. **Clean formatting**: Output well-formatted JSON with proper indentation
7. **Complete responses**: Include all mentioned status codes
8. **Examples matter**: Extract and include example values

## Edge cases to handle

- **Missing sections**: Some specs may not have request body or certain response codes
- **Nested objects**: Handle complex nested request/response structures
- **Arrays**: Detect array types and define item schemas
- **Multiple content types**: Handle specs with both JSON and form data
- **Query parameters**: Detect URL parameters vs body parameters
- **Headers**: Extract header requirements if mentioned
- **Enum values**: Identify fixed value sets (e.g., "고정값")

## Output format

Always output:
1. Valid OpenAPI 3.0 JSON
2. UTF-8 encoded to preserve Korean/international characters
3. Properly indented (2 spaces)
4. Complete structure even if some sections are empty
5. All extracted information from the input text

## Validation checklist

Before outputting, verify:
- [ ] Valid JSON syntax
- [ ] All HTTP methods lowercase (get, post, put, delete)
- [ ] Required fields properly marked
- [ ] Types match OpenAPI specification
- [ ] Examples included where available
- [ ] Korean text preserved correctly
- [ ] All response codes included
- [ ] Content types specified
