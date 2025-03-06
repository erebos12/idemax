Feature: Test health-check endpoint

Scenario: health-check endpoint
  When send "GET" to "http://idemax:8080/health-check"
  Then expect response code "200"