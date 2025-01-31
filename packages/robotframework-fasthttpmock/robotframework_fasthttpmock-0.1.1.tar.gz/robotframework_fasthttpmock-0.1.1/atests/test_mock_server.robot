*** Settings ***
Library    FastHTTPMock
Library    RequestsLibrary
Library    Process
Library    OperatingSystem

Suite Setup    Start Mock Server    port=8085
Test Teardown    Clear All Mock Interactions
Suite Teardown   Stop Mock Server

*** Test Cases ***
Test Basic Mock Server Functionality
    ${request}=    Create Dictionary    method=GET    path=/api/users
    ${response}=    Create Dictionary    status=${200}    body={"users": ["user1", "user2"]}
    ${id}=    Add Mock Interaction    ${request}    ${response}

    ${resp}=    GET    http://localhost:8085/api/users
    Should Be Equal As Strings    ${resp.status_code}    200
    ${body}=    Set Variable    ${resp.json()}
    Should Be Equal    ${body["users"][0]}    user1

    Verify Interaction Called    ${id}    1


Mock Simple API Response
    # Define mock interaction
    ${request}=    Create Dictionary   method=GET    path=/api/users
    ${response}=    Create Dictionary  status=${200}    body={"users": ["user1", "user2"]}
    ${id}=    Add Mock Interaction    ${request}    ${response}
    
    # Make request to mock server
    ${resp}=    GET    http://localhost:8085/api/users
    Should Be Equal As Strings    ${resp.status_code}    200
    
    # Verify the interaction
    Verify Interaction Called    ${id}    1


Mock Multiple API Endpoints
    # Mock GET endpoint
    ${get_request}=    Create Dictionary   method=GET    path=/api/users/1
    ${get_response}=    Create Dictionary  status=${200}  body={"id": 1, "name": "John Doe"}
    ${get_id}=    Add Mock Interaction    ${get_request}    ${get_response}

    # Test GET endpoint
    ${get_resp}=    GET    http://localhost:8085/api/users/1
    Should Be Equal As Strings    ${get_resp.status_code}    200
    Should Be Equal As Strings    ${get_resp.json()}[name]    John Doe
    
    # Mock POST endpoint
    ${post_request}=    Create Dictionary  method=POST    path=/api/users
    ${post_response}=    Create Dictionary    status=${201}    body={"message": "User created"}
    ${post_id}=    Add Mock Interaction    ${post_request}    ${post_response}

    # Test POST Endpoint
    ${post_resp}=    POST    http://localhost:8085/api/users
    Should Be Equal As Strings    ${post_resp.status_code}    201
    Should Be Equal As Strings    ${post_resp.json()}[message]    User created
    
    # Clear GET and add another interaction
    Remove Mock Interaction    ${get_id}
    ${get_request}=    Create Dictionary   method=GET    path=/api/users/1
    ${get_response}=    Create Dictionary  status=${200}  body={"id": 1, "name": "Yoda"}
    ${get_id}=    Add Mock Interaction    ${get_request}    ${get_response}

    # Test GET endpoint
    ${get_resp}=    GET    http://localhost:8085/api/users/1
    Should Be Equal As Strings    ${get_resp.status_code}    200
    Should Be Equal As Strings    ${get_resp.json()}[name]    Yoda
