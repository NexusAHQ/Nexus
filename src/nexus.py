import os
import json


class QuestionAnsweringSystem:
    def __init__(self, qa_database):
        self.qa_database = qa_database

    def find_matching_question(self, user_input):
        user_input_lower = user_input.lower().strip()
        return [
            entry
            for entry in self.qa_database
            if entry["question"].lower().strip() == user_input_lower
        ]

    def answer_question(self, user_input):
        matches = self.find_matching_question(user_input)
        if matches:
            return matches[0]["answer"]
        else:
            return "Sorry, I don't have information on that."


def load_qa_database(directory_path):
    qa_database = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.lower().endswith(".json"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r") as file:
                        qa_database.extend(json.load(file))
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {file_path}: {e}")
                    print(f"Error on line {e.lineno}, column {e.colno}: {e.msg}")
                except Exception as e:
                    print(
                        f"An unexpected error occurred while loading {file_path}: {e}"
                    )

    return qa_database


if __name__ == "__main__":
    data_directory = "data"
    qa_database = load_qa_database(data_directory)
    qa_system = QuestionAnsweringSystem(qa_database)

    while True:
        user_message = input("User: ")
        if user_message.lower() == "exit":
            break

        try:
            answer = qa_system.answer_question(user_message)
            print(f"Nexus: {answer}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
