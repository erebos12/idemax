Feature: Idempotency Key Management

  Scenario: Create a new idempotency key
    Given following json
    """
    {
      "tenant_id": "12345",
      "idempotency_key": "req-789",
      "ttl_seconds": 60,
      "status": "pending",
      "http_status": 202,
      "response": "{}"
    }
    """
    When send "POST" to "http://idemax:8080/idempotencies"
    Then expect response code "201"
    And json attribute "["message"]" is equal to "Idempotency key stored"
