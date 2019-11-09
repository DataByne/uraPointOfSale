Feature: Listing notes
    Viewing all notes will show the list of notes for the particular user in the database

    Background: Someone asked to view notes

    Scenario: The user is not logged in
        Given someone asks for a list of notes
        When that person is not logged in
        Then they are prompted to log in

    Scenario: The user is logged in
        Given someone asks for a list of notes
        When that person has one or more notes saved
        Then their list of notes are displayed

    Scenario: The user is logged in
        Given someone asks for a list of notes
        When that person does not have any notes saved
        Then a message appears saying that there are no notes