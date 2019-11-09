Feature: Checking the contents of a file
    I want to examine the contents of a note and check the title and the body of
    said note.

Scenario: A note is created
    Given We have a note
    When we implement a test
    Then we will check the contents of the notes 

 Scenario: A note has a title
    Given we have a note
    When we have a test
    Then the title will be checked

Scenario: An empty note
    Given we have an empty note
    When we implement a test
    Then an error will show that the note is empty

Scenario: A note is created without a title
    Given we have a note without a title
    When we create a note
    Then a note without a title is created

Scenario: A note is created without a body
    Given we have a note without content in the body
    When we create a note
    Then a note without a body is created 


