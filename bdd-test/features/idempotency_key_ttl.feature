Feature: Idempotency Key TTL feature - idempotency key gone after ttl

  Scenario: Create a new idempotencies key
    Given following json
    """
    {
      "tenant_id": "12345",
      "idempotency_key": "req-789",
      "ttl_seconds": 1,
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

  Scenario: Wait until ttl expires and check if idempotency key is gone
    When wait for "1500" msecs
    When send "GET" to "http://idemax:8080/idempotencies/12345/req-789"
    Then expect response code "404"
    And json attribute "["error"]" is equal to "Idempotency key not found"
    

  