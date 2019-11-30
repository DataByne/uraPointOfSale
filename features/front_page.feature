Feature: Front Page
    I want a meaningful landing page that displays the company name and has links to other pages within the site.

    Scenario: I navigate to company website
        Given I am on the landing page
        Then I see the company name
        Then I see a link to "https://github.com/DataByne/uraPointOfSale"
        And I see a link to "https://www.kent.edu/cs"

    Scenario: From front page I can navigate to other pages
        Given I am on the landing page
        Then I see the navigation bar
        And I can navigate to other pages

    Scenario: I see welcome back message as registered
        Given I am on the landing page
        And I am logged in
        Then I see the text "Welcome back to Note Weaver!"

    Scenario: I see welcome back message as anonymous
        Given I am on the landing page
        And I am not logged in
        Then I see generic welcome back message

    Scenario: I see company logo
        Given I am on the landing page
        Then I see the image company logo
