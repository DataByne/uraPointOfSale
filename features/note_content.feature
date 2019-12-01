Feature: Checking the contents of a file
    I want to examine the contents of a note and check the title and the body of
    said note.

    Scenario: A note is created
        Given I want to create a note
        And I create a note
        Then The note is created

    Scenario: An empty note is created
        Given I want to create a note
        And I try to make an empty note
        Then the note is not created

    Scenario: A note is created without a title
        Given we want to create a note
        And the note has no title
        Then that note is not created

    Scenario: A note is created without a body
        Given we want to create a note
        And the note has not body
        Then the note is not created
