Feature: Tenant Management

  Scenario: Create a new tenant
    Given following json
    """
    {
      "tenant_id": "12345",
      "name": "TestTenant"
    }
    """
    When send "POST" to "http://idemax:8080/tenants"
    Then expect response code "201"
    And json attribute "["message"]" is equal to "Tenant created successfully"
