Feature: Idempotency Key Management

  Scenario: Create a new idempotency key
    Given following json
    """
    {
      "status": "pending",
      "http_status": 202,
      "response": "{}"
    }
    """
    Given header "X-Tenant-ID" is "12345"
    Given form-data "idempotency_key" is "req-789"
    Given form-data "ttl_seconds" is "60"
    When send "POST" to "http://idemax:8080/idempotencies"
    Then expect response code "201"
    And json attribute "["message"]" is equal to "Idempotency key stored"
