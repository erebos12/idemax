Feature: Idempotency Key Management

  Scenario: Create a new idempotencies key
    Given following json
    """
    {
      "tenant_id": "12345",
      "idempotency_key": "req-789",
      "ttl_seconds": 10,
      "status": "pending",
      "http_status": 202,
      "response": "{}"
    }
    """
    When send "POST" to "http://idemax:8080/idempotencies"
    Then expect response code "201"
    And json attribute "["message"]" is equal to "Idempotency key stored"

  Scenario: Retrieve an existing idempotency key
    When send "GET" to "http://idemax:8080/idempotencies/12345/req-789"
    Then expect response code "200"
    And json attribute "["status"]" is equal to "pending"
    And json attribute "["http_status"]" is equal to "202"
    And json attribute "["response"]" is equal to "{}"

  Scenario: Create a duplicate idempotency key
    Given following json
    """
    {
      "tenant_id": "12345",
      "idempotency_key": "req-789",
      "ttl_seconds": 10,
      "status": "pending",
      "http_status": 202,
      "response": "{}"
    }
    """
    When send "POST" to "http://idemax:8080/idempotencies"
    Then expect response code "409"
    
  Scenario: Retrieve a non-existent idempotency key
    When send "GET" to "http://idemax:8080/idempotencies/12345/non-existent-key"
    Then expect response code "404"
    And json attribute "["error"]" is equal to "Idempotency key not found"

  Scenario: Retrieve an idempotency key for a non-existent tenant
    When send "GET" to "http://idemax:8080/idempotencies/99999/req-789"
    Then expect response code "404"
    And json attribute "["error"]" is equal to "Tenant not found"

  Scenario: Missing tenant ID in request
    When send "GET" to "http://idemax:8080/idempotencies/req-789"
    Then expect response code "404"

  Scenario: Missing idempotency key in request
    When send "GET" to "http://idemax:8080/idempotencies/12345/"
    Then expect response code "404"

  Scenario: Successfully delete an existing idempotency key
    When send "DELETE" to "http://idemax:8080/idempotencies/12345/req-789"
    Then expect response code "200"
    And json attribute "["message"]" is equal to "Idempotency key deleted"

  Scenario: Delete a non-existent idempotency key
    When send "DELETE" to "http://idemax:8080/idempotencies/12345/non-existent-key"
    Then expect response code "404"
    And json attribute "["error"]" is equal to "Idempotency key not found"

  Scenario: Delete an idempotency key for a non-existent tenant
    When send "DELETE" to "http://idemax:8080/idempotencies/99999/req-789"
    Then expect response code "404"
    And json attribute "["error"]" is equal to "Tenant not found"

  Scenario: Missing tenant ID in request
    When send "DELETE" to "http://idemax:8080/idempotencies/req-789"
    Then expect response code "404"

  Scenario: Missing idempotency key in request
    When send "DELETE" to "http://idemax:8080/idempotencies/12345/"
    Then expect response code "404"




