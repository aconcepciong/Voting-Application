from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect submit button to func submit_vote
        self.button_submit.clicked.connect(self.submit_vote)

        # Creates constant obj associated with the csv file with store vote data later
        self.vote_file = "votes.csv"

    def submit_vote(self):
        """
        Handles vote submission, validates id, checks for candidate selected,
        prevents duplicate vote submission, writes a valid vote to csv file, and
        displays a confirmation message.
        """
        voter_id = self.input_voter_id.text().strip()  # Creates voter_id from input

        # Validate voter ID: must be exactly 6 digits
        if not voter_id.isdigit() or len(voter_id) != 6:  # AI help set up if not statement: id must be 6 digits
            self.label_validation.setStyleSheet("color: red;")  # Google AI help to set text to different colors
            self.label_validation.setText("Invalid ID (6 digits.)")
            return

        # Checks who is selected, else it prompts to select someone
        if self.button_jane.isChecked():
            selected_candidate = "Jane"
        elif self.button_john.isChecked():
            selected_candidate = "John"
        else:
            self.label_validation.setStyleSheet("color: red;")
            self.label_validation.setText("Please select a candidate.")
            return

        # If both are valid
        self.label_validation.setStyleSheet("")  # Text color reset for successful validation
        self.label_validation.setText(f"Voter {voter_id} has voted for candidate: {selected_candidate}")

        # Check for duplicates stored in a vote file and does not allow for dupe votes, added try/except in case file is not already in directory
        try:
            with open(self.vote_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == voter_id:
                        self.label_validation.setStyleSheet("color: red;")
                        self.label_validation.setText("This ID has already voted.")
                        return
        except FileNotFoundError:
            pass # File not found in case no one has voted yet

        # if it passes the above check, the file opens in appended mode and vote info is appended
        with open(self.vote_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, selected_candidate])

        self.input_voter_id.clear()  # Clears the id field after vote submission
