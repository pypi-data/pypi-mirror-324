Feature: Simple storage

    Scenario: Publish Activity Works
        Given A new user called "Alice"
        And A new user called "Bob"
        And "Bob" follows "Alice"
        When "Alice" publishes a "moo" animal sound to her follows
        Then "Bob" receives an activity
        And the received activity is of type "AnimalSound"