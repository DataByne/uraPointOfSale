Feature: Checking the contents of a file
    I want to examine the contents of a note and check the title and the body of
    said note.

    Background: We are on the note creation page
        Given I am logged in
        And we are on the note creation page

    Scenario: A note is created
        Given we have a note
        When we implement a test
        Then we will check the contents of title and body of a note

    Scenario: A note has a title
        Given we have a note
        And the note has a title
        When we have a test
        Then the title will be checked

    Scenario: An empty note
        Given we have an empty note
        When we implement a test
        Then an error will show that the note is empty

    Scenario: A note is created without a title
        Given we have a note
        And the note has no title
        When we create a note
        Then a note without a title is created

    Scenario: A note is created without a body
        Given we have a note
        And the note has a title
        And the note has a body
        When we create a note
        Then a note without a body is created
