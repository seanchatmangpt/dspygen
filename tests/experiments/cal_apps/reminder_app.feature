Feature: Reminder App Functionality
  As a user of the Reminder App
  I want to manage my reminders and lists
  So that I can organize my tasks effectively

  Scenario: Create a new reminder list
    Given the Reminder App is initialized
    When I add a new reminder list called "Work Tasks"
    Then the "Work Tasks" list should be in the app's lists

  Scenario: Add a reminder to a list
    Given the Reminder App is initialized
    And a reminder list called "Personal Tasks" exists
    When I select the "Personal Tasks" list
    And I add a reminder "Buy groceries" with due date "2023-05-01 18:00"
    Then the "Personal Tasks" list should contain the reminder "Buy groceries"

  Scenario: Mark a reminder as completed
    Given the Reminder App is initialized
    And a reminder list called "Home Chores" exists
    And the list "Home Chores" has a reminder "Clean the kitchen"
    When I select the "Home Chores" list
    And I mark the reminder "Clean the kitchen" as completed
    Then the reminder "Clean the kitchen" should be marked as completed

  Scenario: Remove a reminder list
    Given the Reminder App is initialized
    And a reminder list called "Temporary Tasks" exists
    When I remove the "Temporary Tasks" list
    Then the "Temporary Tasks" list should not be in the app's lists

  Scenario: Clear completed reminders
    Given the Reminder App is initialized
    And a reminder list called "Daily Tasks" exists
    And the list "Daily Tasks" has a completed reminder "Make bed"
    And the list "Daily Tasks" has an incomplete reminder "Do laundry"
    When I select the "Daily Tasks" list
    And I clear completed reminders
    Then the "Daily Tasks" list should not contain the reminder "Make bed"
    And the "Daily Tasks" list should contain the reminder "Do laundry"