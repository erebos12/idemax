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
