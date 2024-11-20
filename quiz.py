import random
import time
import json

# Load questions from JSON file
def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Function to shuffle questions (for randomization)
def randomize_questions(questions):
    random.shuffle(questions)

# Function to display a question
def display_question(question_data, index):
    print(f"\nQuestion {index + 1}: {question_data['question']}")
    for i, option in enumerate(question_data['options'], start=1):
        print(f"{i}. {option}")

# Function to get the user's answer
def get_user_answer():
    while True:
        try:
            answer = int(input("Your answer (1/2/3/4): "))
            if answer in [1, 2, 3, 4]:
                return answer
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to save high scores
def save_score(username, score):
    with open('scores.txt', 'a') as file:
        file.write(f"{username}: {score}\n")

# Function to display high scores
def display_high_scores():
    print("\nHigh Scores:")
    try:
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
            for line in scores:
                print(line.strip())
    except FileNotFoundError:
        print("No high scores yet.")

# Function to handle 50-50 lifeline
def use_50_50(options, correct_answer):
    incorrect_options = [i for i in range(1, 5) if i != correct_answer]
    removed = random.sample(incorrect_options, 2)
    print("Remaining options:")
    for i in range(1, 5):
        if i not in removed:
            print(f"{i}. {options[i-1]}")

# Function to start the quiz based on selected mode
def run_quiz(questions):
    score = 0
    for index, question in enumerate(questions):
        display_question(question, index)
        user_answer = get_user_answer()
        correct_answer = question['answer']
        
        if user_answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was option {correct_answer}.")
        
        # Option for 50-50 lifeline
        if input("Do you want to use a lifeline (50-50)? (yes/no): ").lower() == 'yes':
            use_50_50(question['options'], question['answer'])
        
    return score

# Main function to run the app
def main():
    filename = './questions.json'
    questions = load_questions(filename)
    randomize_questions(questions)  # Shuffle the questions for randomness
    print("\nWelcome to the Quiz App!")
    print("Answer the following questions:\n")

    username = input("Enter your username: ")
    score = run_quiz(questions)
    total_questions = len(questions)

    print(f"\nYou scored {score} out of {total_questions}.")
    percentage = (score / total_questions) * 100
    print(f"Your score percentage is: {percentage:.2f}%")

    save_score(username, score)  # Save score after quiz
    display_high_scores()  # Show high scores at the end

if __name__ == "__main__":
    main()
