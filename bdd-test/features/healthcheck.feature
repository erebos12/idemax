Feature: Test health-check endpoint

Scenario: health-check endpoint
  When sending get to "http://idemax:8080/health-check"
  Then expect response code "200"