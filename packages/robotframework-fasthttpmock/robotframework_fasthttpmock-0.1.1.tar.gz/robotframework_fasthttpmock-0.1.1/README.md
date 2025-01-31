# robotframework-fasthttpmock

HTTP mock server library for Robot Framework powered by FastAPI. This library enables easy mocking of HTTP endpoints in your Robot Framework tests with minimal setup and configuration.

## Features

- 🚀 Lightweight and fast mock server using FastAPI
- 🤖 Simple Robot Framework keywords
- 🔄 Dynamic mock interaction management
- ✅ Request verification capabilities
- 🧹 Automatic server cleanup
- 🌐 Support for all HTTP methods (GET, POST, PUT, DELETE, PATCH)

## Installation
```bash
pip install robotframework-fasthttpmock
```

The editable mode (`-e`) allows you to modify the source code and see the changes immediately without reinstalling.

## Available Keywords

| Keyword | Description |
|---------|-------------|
| `Start Mock Server` | Start the mock HTTP server with optional host and port |
| `Stop Mock Server` | Gracefully stop the mock server |
| `Add Mock Interaction` | Add a new mock interaction with request/response definitions |
| `Remove Mock Interaction` | Remove an existing mock interaction |
| `Verify Interaction Called` | Verify the number of times an interaction was called |

## Quick Start

Here's a simple example of how to use the library in your Robot Framework tests:

```robot
*** Settings ***
Library    FastHTTPMock
Library    RequestsLibrary

*** Test Cases ***
Mock Simple API Response
    Start Mock Server port=8000
    
    # Define mock interaction
    ${request}=    Create Dictionary   method=GET  path=/api/users
    ${response}=    Create Dictionary  status=200  body={"users": ["user1", "user2"]}
    ${id}=    Add Mock Interaction    ${request}    ${response}
    
    # Make request to mock server
    ${resp}=    GET    http://localhost:8000/api/users
    Should Be Equal As Strings    ${resp.status_code}    200
    
    # Verify the interaction
    Verify Interaction Called    ${id}    1
    [Teardown]    Stop Mock Server
```



## Advanced Usage

### Multiple Endpoints Example
```robot
*** Test Cases ***
Mock Multiple API Endpoints
    Start Mock Server    port=8000
    
    # Mock GET endpoint
    ${get_request}=    Create Dictionary   method=GET  path=/api/users/1
    ${get_response}=    Create Dictionary  status=200  body={"id": 1, "name": "John Doe"}
    ${get_id}=    Add Mock Interaction    ${get_request}    ${get_response}
    
    # Mock POST endpoint
    ${post_request}=    Create Dictionary  method=POST path=/api/users
    ${post_response}=    Create Dictionary    status=201  body={"message": "User created"}
    ${post_id}=    Add Mock Interaction    ${post_request}    ${post_response}
    
    # Test both endpoints
    ${get_resp}=    GET    http://localhost:8000/api/users/1
    Should Be Equal As Strings    ${get_resp.status_code}    200
    ${post_resp}=    POST    http://localhost:8000/api/users
    Should Be Equal As Strings    ${post_resp.status_code}    201
    [Teardown]    Stop Mock Server
```

## Contributing

Refer to [Contributing Docs](./CONTRIBUTING.md) for more details

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests and ensure they pass
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/leelaprasadv/robotframework-fasthttpmock/issues) page
2. Create a new issue if your problem isn't already listed

## Acknowledgments

- Inspired by [PactumJS](https://github.com/pactumjs/pactum)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Made for [Robot Framework](https://robotframework.org/)