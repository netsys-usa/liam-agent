# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of LIAM Python SDK
- Synchronous client (`LIAMClient`)
- Asynchronous client (`LIAMClientAsync`)
- ECDSA P-256 key generation utilities
- Full API coverage for memory operations:
  - `create_memory`
  - `create_memory_with_image`
  - `list_memories`
  - `chat`
  - `summarize_memory`
  - `forget_memory`
  - `memory_status`
- Full API coverage for tag operations:
  - `list_tags`
  - `add_tag`
  - `get_by_tag`
  - `change_tag`
- Health check endpoint
- Batch operations for async client
- Environment variable configuration support
- Comprehensive examples and documentation
- Unit tests with pytest

### Security
- ECDSA P-256 signature-based authentication
- Secure key generation with cryptography library
- No plaintext credential storage
