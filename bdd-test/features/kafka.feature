Feature: Sending JSON to Kafka

  Scenario: Send a JSON message to a Kafka topic
    Given following json
        """
          {
              "specversion" : "1.0",
              "type" : "com.example.someevent",
              "source" : "/mycontext",
              "id" : "C234-1234-1234",
              "time" : "2018-04-05T17:31:00Z",
              "comexampleextension1" : "value",
              "comexampleothervalue" : 5,
              "datacontenttype" : "application/json",
              "data" : {
                  "appinfoA" : "abc",
                  "appinfoB" : 123,
                  "appinfoC" : true
              }
          }
        """
    When kafka - sending json to broker "kafka:29092" and topic "test-topic"

  Scenario: Consume JSON message from Kafka topic
    When kafka - consuming json from broker "kafka:29092" and topic "test-topic"
    Then json attribute "[0]["id"]" is equal to "C234-1234-1234"
    Then json attribute "[0]["data"]["appinfoA"]" is equal to "abc"
    Then json attribute "[0]["data"]["appinfoB"]" is equal to "123"
    Then json attribute "[0]["data"]["appinfoC"]" is equal to "True"
