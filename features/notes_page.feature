Feature: Manipulation and viewing the notes

    Scenario: Note needs to be edited
        Given I am registered
        And I am logged in
        And I have a note
        And I edit that note
        Then the note should be edited

    Scenario: A note is no longer needed
        Given I am registered
        And I am logged in
        And I have a note
        And I delete that note
        Then I see the text "You currently have no notes."

    Scenario: Person need to search for notes via keywords
        Given I am registered
        And I am logged in
        And I have a note
        And I search for that note
        Then I see that note
