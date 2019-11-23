Feature: Manipulating the notes in one way or another

    Scenario: Note needs to be edited
        Given a note exists
        When the person wants to change somthin in that note
        Then the person can change the content of that note
        And changes the origional note.

    Scenario: A note is no longer needed
        Given a not exists
        And the note is no longer needed
        When the person requests to delete the note
        Then the person is asked if they wat to confirm
        And the note is deleted if confirmed yes

    Scenario: Note needs to change position
        Given more than one note exists
        When the person wants to change what order they're in
        Then the person can change the order of the notes

    Scenario: Person need to search for notes via keywords
        Given a note exists
        When a person enters a letter, word, or multiple words
        Then notes are searched through for keywords
        And are displayed in most relivant order