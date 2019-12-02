Feature: Listing notes
    Viewing all notes will show the list of notes for the particular user in the database

    Background: Someone asked to view notes

    Scenario: The user is not logged in
        Given I am not logged in
        And I visit my notes
        Then I am redirected to login

    Scenario: The user has notes
        Given I am registered
        And I am logged in
        And I want to create a note
        And I create a note
        And I visit my notes
        Then I see the text "You have weaved these notes!"

    Scenario: The user has no notes
        Given I am registered
        And I am logged in
        And I have zero notes
        And I visit my notes
        Then I see the text "You currently have no notes."
