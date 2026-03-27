# XDB API Reference — AI Agent Guide

> **Base URL:** `https://web.askbuddy.ai/devspacexdb`  
> **Auth:** All endpoints require an `apiKey` or `userKey` in the request body (no Authorization header needed unless noted).  
> **Content-Type:** `application/json` for all requests.

---

## Standard Response Envelope

Every endpoint returns the same top-level shape:

```json
{
  "status": "string",
  "message": "string",
  "data": { ... },
  "timestamp": "string",
  "processId": "string"
}
```

---

## Group 1 — User Management

### 1.1 Create Workspace (Register)

**POST** `/api/auth/register`

Registers a new workspace/institution. Returns an `apiKey` used in subsequent calls.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Display name of the institution |
| `institutionId` | string | ✅ | Short unique identifier (e.g. `"TSOL"`) |
| `institutionName` | string | ✅ | Full institution name |

**Example Request**
```json
{
  "name": "Tech Solutions",
  "institutionId": "TSOL",
  "institutionName": "Tech Solutions"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `name` | string | Registered institution name |
| `apiKey` | string | API key for future requests |
| `status` | string | Registration status |

---

### 1.2 Activate Workspace

**POST** `/api/auth/activate`

Activates a previously registered workspace.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Name of the workspace to activate |

**Example Request**
```json
{
  "name": "Tech Solutions"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `apiKey` | string | Confirmed API key |
| `status` | string | Activation status |

---

### 1.3 Workspace Submit Key

**POST** `/api/auth/submit-key`

Associates a public key (RSA/EC, base64-encoded PEM) with a workspace, enabling signed/encrypted API operations.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | ✅ | The workspace API key |
| `publicKey` | string | ✅ | Base64-encoded PEM public key |

**Example Request**
```json
{
  "apiKey": "s5Lh8TFKDRUH59FZ4LwqLu6GoZD6PRlqbD7XpQGS58",
  "publicKey": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0..."
}
```

---

### 1.4 Create User Profile

**POST** `/api/auth/create-profile`

Creates a user profile within a workspace.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Full name of the user |
| `identification` | string | ✅ | A unique identifier string for the user |
| `identificationType` | string | ✅ | Type of ID — e.g. `"UNIQUE_ID"` |

**Example Request**
```json
{
  "name": "James Watson",
  "identification": "e5c6f5e2f6f5e8a8c8e8d8f5a5f8njknk55e24",
  "identificationType": "UNIQUE_ID"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `userkey` | string | Generated key for this user (used in memory API calls) |
| `name` | string | User name |
| `identification` | string | Provided identification |
| `profileId` | number | Numeric profile ID |

---

### 1.5 Register LLM

**POST** `/api/user/register-llm`

Associates an LLM model and its API key with a workspace, enabling the memory chat endpoint to use it.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | ✅ | XDB workspace API key |
| `model` | string | ✅ | LLM model name (e.g. `"gpt-4"`) |
| `identifier` | string | ✅ | Custom identifier for this LLM registration |
| `key` | string | ✅ | LLM provider API key (e.g. OpenAI `sk-...`) |

**Example Request**
```json
{
  "apiKey": "s5Lh8TFKDRUH59FZ4LwqLu6GoZD6PRlqbD7XpQGS58",
  "model": "gpt-4",
  "identifier": "ID123456789",
  "key": "sk-proj-..."
}
```

---

## Group 2 — Memories

> All memory endpoints use `userKey` (from **Create User Profile**) as the primary auth token.

---

### 2.1 Health Check

**POST** `/api/memory/health`

Pings the memory service to confirm it is running.

**Request Body**
```json
{
  "ping": "test"
}
```

**Response:** Returns a status/message confirming service health.

---

### 2.2 Create Memory

**POST** `/api/memory/create`

Stores a new memory entry for a user.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `content` | string | ✅ | The memory text to store |
| `tag` | string | ✅ | Category tag for the memory (can be empty string) |
| `sessionId` | string | ✅ | Session identifier string (e.g. `"2025060400001"`) |

**Example Request**
```json
{
  "userKey": "f43d94a0935eb7eeb2323638b9d0af57c24975dc25c6e335e0d55b11025a9ebc",
  "tag": "immigration",
  "content": "Need to visit office wed and friday for PR, this is a must as per contracts",
  "sessionId": "2025060400001"
}
```

---

### 2.3 Create Memory with Image

**POST** `/api/memory/create`

Same endpoint as **Create Memory** but accepts an additional base64-encoded image payload.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `content` | string | ✅ | Memory text |
| `tag` | string | ✅ | Category tag |
| `sessionId` | string | ✅ | Session identifier |
| `imageData` | string | ✅ | Base64-encoded image (PNG/JPEG) |

---

### 2.4 Memory Status

**POST** `/api/memory/memory-status`

Checks the processing status of a previously submitted memory.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `tag` | string | ✅ | Tag of the memory to check |
| `content` | string | ✅ | Content of the memory to check |
| `sessionId` | string | ✅ | Session identifier |

**Example Request**
```json
{
  "userKey": "f43d94a0935eb7eeb2323638b9d0af57c24975dc25c6e335e0d55b11025a9ebc",
  "tag": "food_preferences",
  "content": "I like south indian food, especially idly and dosa which is homemade",
  "sessionId": "2025060400001"
}
```

---

### 2.5 List Memories

**POST** `/api/memory/list`

Retrieves memories for a user, optionally filtered by tokens or a natural-language query.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `tokens` | array | ✅ | Array of token strings to filter by (empty `[]` returns all) |
| `query` | string | ✅ | Natural language query to match memories against |
| `require_llm_summary` | boolean | ❌ | If `true`, returns an LLM-generated summary (default: `false`) |
| `suggestedTokens` | object | ❌ | Token hints with `high`/`low` priority synonyms |

**Example Request**
```json
{
  "userKey": "f43d94a0935eb7eeb2323638b9d0af57c24975dc25c6e335e0d55b11025a9ebc",
  "tokens": [],
  "query": "where should I give blood sample",
  "require_llm_summary": false,
  "suggestedTokens": {
    "high": [
      { "token": "blood", "synonyms": ["hemoglobin", "plasma", "red blood cells"] }
    ]
  }
}
```

**Response `data.memories[]` Fields**

| Field | Type | Description |
|---|---|---|
| `memory` | string | The stored memory content |
| `language` | string\|null | Detected language |
| `transactionNumber` | string | Unique ID for this memory entry |
| `date` | string | Creation date |
| `docId` | string\|null | Associated document ID |
| `fileID` | string\|null | Associated file ID |
| `notesKey` | string\|null | Notes reference key |
| `tokens` | string[] | Extracted keyword tokens |

---

### 2.6 Chat (Query Memories with LLM)

**POST** `/api/memory/chat`

Sends a natural language statement/question and retrieves a context-aware answer derived from the user's stored memories using the registered LLM.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `statement` | string | ✅ | The user's question or statement |
| `existing_tags` | string[] | ✅ | Tags to scope the memory search |

**Example Request**
```json
{
  "userKey": "f43d94a0935eb7eeb2323638b9d0af57c24975dc25c6e335e0d55b11025a9ebc",
  "statement": "where should I give blood sample",
  "existing_tags": ["XBD_Changes", "food_preferences", "banking"]
}
```

---

### 2.7 Summarize Memory

**POST** `/api/memory/summarize-memory`

Generates an LLM summary from a provided set of memory objects.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `memories` | array | ✅ | Array of memory objects (same shape as returned by **List Memories**) |

**Example Request**
```json
{
  "userKey": "4e984be16442a99515ca63a32d5ce28273a5b355a1027a4a8955d27e7d6c4129",
  "memories": [
    {
      "memory": "I love Italian food",
      "language": null,
      "transactionNumber": "XD93BDB752BE4E11F0BC396A2E821FB445:0",
      "date": "11/10/2025 11:02:04",
      "docId": null,
      "fileID": null,
      "notesKey": null,
      "isEncrypted": false,
      "keyUUID": null
    }
  ]
}
```

---

### 2.8 Forget Memory

**POST** `/api/memory/forget`

Permanently deletes a specific memory entry identified by its query hash.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `queryHash` | string | ✅ | Hash of the memory to delete |

**Example Request**
```json
{
  "userKey": "4e984be16442a99515ca63a32d5ce28273a5b355a1027a4a8955d27e7d6c4129",
  "queryHash": "e881b06effd5e07a26551cad1008c5177b78b07f9bf17271fb275f8dc9508d6a"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `profileId` | integer | Profile associated with the deleted memory |
| `status` | string | Deletion status |

---

### 2.9 List Tags

**POST** `/api/memory/list-tag`

Returns all tags associated with a user's stored memories.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |

**Example Request**
```json
{
  "userKey": "4e984be16442a99515ca63a32d5ce28273a5b355a1027a4a8955d27e7d6c4129"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `notesTag` | string[] | All tags used by this user |

---

### 2.10 Add Tag

**POST** `/api/memory/add-tag`

Adds a tag to all memories belonging to a given session.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `sessionId` | string | ✅ | Session whose memories should be tagged |
| `tag` | string | ✅ | Tag to apply |

**Example Request**
```json
{
  "userKey": "9b5f195385b58b331c7390a1a013f00ad56130dfbeab59b860ef38a32fc18577",
  "sessionId": "2025032602",
  "tag": "things to do in 30s"
}
```

---

### 2.11 Get Memories by Tag

**POST** `/api/memory/by-tag`

Retrieves all memories associated with one or more tags.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `tag` | string[] | ✅ | Array of tags to filter by |

**Example Request**
```json
{
  "userKey": "4e984be16442a99515ca63a32d5ce28273a5b355a1027a4a8955d27e7d6c4129",
  "tag": ["XBD_Changes"]
}
```

**Response `data.memories[]` Fields:** Same as **List Memories**.

---

### 2.12 Change Tag

**POST** `/api/memory/change-tag`

Renames a tag across all memories for a user.

**Request Body**

| Field | Type | Required | Description |
|---|---|---|---|
| `userKey` | string | ✅ | User's unique key |
| `currentTag` | string | ✅ | Existing tag to rename |
| `updatedTag` | string | ✅ | New tag name |

**Example Request**
```json
{
  "userKey": "c0312641aade88080be0c7f0801bc4dc6edbeb2752cb1530ae0483728e6a4f81",
  "currentTag": "things to do in 30s",
  "updatedTag": "30s wishlist"
}
```

**Response `data` Fields**

| Field | Type | Description |
|---|---|---|
| `profileId` | number | User's profile ID |
| `status` | string | Operation status |
| `updatedCount` | number | Number of memories whose tag was changed |

---

## Quick Reference

| Endpoint | Method | Path |
|---|---|---|
| Create Workspace | POST | `/api/auth/register` |
| Activate Workspace | POST | `/api/auth/activate` |
| Workspace Submit Key | POST | `/api/auth/submit-key` |
| Create User Profile | POST | `/api/auth/create-profile` |
| Register LLM | POST | `/api/user/register-llm` |
| Health Check | POST | `/api/memory/health` |
| Create Memory | POST | `/api/memory/create` |
| Create Memory w/ Image | POST | `/api/memory/create` |
| Memory Status | POST | `/api/memory/memory-status` |
| List Memories | POST | `/api/memory/list` |
| Chat (LLM Query) | POST | `/api/memory/chat` |
| Summarize Memory | POST | `/api/memory/summarize-memory` |
| Forget Memory | POST | `/api/memory/forget` |
| List Tags | POST | `/api/memory/list-tag` |
| Add Tag | POST | `/api/memory/add-tag` |
| Get by Tag | POST | `/api/memory/by-tag` |
| Change Tag | POST | `/api/memory/change-tag` |