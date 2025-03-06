Feature: Sending JSON to Kafka

  Scenario: Send a JSON message to a Kafka topic
    Given following json
        """
        {
          "index": 1,
          "message": "Hello Kafka"
        }
        """
    When kafka - sending json to broker "kafka:29092" and topic "test-topic"

  Scenario: Consume JSON message from Kafka topic
    When kafka - consuming json from broker "kafka:29092" and topic "test-topic"
    Then json attribute "[0]["message"]" is equal to "Hello Kafka"
    And json attribute "[0]["index"]" is equal to "1"
