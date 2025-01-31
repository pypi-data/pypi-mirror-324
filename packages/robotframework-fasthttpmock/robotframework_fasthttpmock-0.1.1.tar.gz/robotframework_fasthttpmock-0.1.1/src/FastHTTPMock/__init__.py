from importlib.metadata import version

from .keywords import FastHTTPMockKeywords

class FastHTTPMock(FastHTTPMockKeywords):
    """
    FastHTTPMock is a lightweight HTTP mock server library for Robot Framework powered by FastAPI.

    = Table of Contents =

    - Introduction
    - Installation
    - Examples
    - Keyword Documentation

    = Introduction =

    FastHTTPMock provides an easy way to mock HTTP endpoints in your Robot Framework tests.
    It uses FastAPI and uvicorn to create a high-performance mock server that can be controlled
    through Robot Framework keywords.

    = Installation =

    To install the library, run:
    | ``pip install robotframework-fasthttpmock``

    = Examples =

    == Basic Usage ==

    | *** Settings ***          |                |                |
    | Library                   | FastHTTPMock   |                |
    | Library                   | RequestsLibrary |                |

    | *** Test Cases ***        |                |                |
    | Mock Simple API Response  |                |                |
    |    Start Mock Server      | port=8085      |                |
    |    ${request}=            | Create Dictionary | method=GET    | path=/api/users |
    |    ${response}=           | Create Dictionary | status=${200} | body={"users": ["user1", "user2"]} |
    |    ${id}=                 | Add Mock Interaction | ${request} | ${response} |
    |    ${resp}=               | GET            | http://localhost:8085/api/users |
    |    Should Be Equal As Strings | ${resp.status_code} | 200    |
    |    Verify Interaction Called | ${id}       | 1       |
    |    [Teardown]             | Stop Mock Server |       |

    """
    __version__ = version("robotframework-fasthttpmock")
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_DOC_FORMAT = 'HTML'

    def __init__(self):
        super().__init__()

# Make the library directly available
__all__ = ['FastHTTPMock'] 