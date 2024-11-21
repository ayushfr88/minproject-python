import json
import random
import tkinter as tk
from tkinter import messagebox

# Global variables
quiz_active = True
score = 0
current_question_index = 0
username = ""

# Load questions and duration from JSON file
def load_quiz_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data.get("duration", 0), data.get("questions", [])
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        return 0, []
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Failed to parse the JSON file '{filename}'.")
        return 0, []

# Function to start the quiz timer
def quiz_timer(duration, root):
    global quiz_active
    if duration <= 0 or not quiz_active:
        return

    mins, secs = divmod(duration, 60)
    timer_label.config(text=f"Time left: {mins:02}:{secs:02}")

    if duration > 0:
        root.after(1000, quiz_timer, duration - 1, root)  # Continue counting down
    else:
        quiz_active = False  # Stop the quiz when time runs out
        messagebox.showinfo("Time's Up!", "The quiz has ended!")
        save_score_to_file(username, score)  # Save score to file
        root.quit()  # Close the quiz window

# Function to display the next question
def display_question(root, questions):
    global current_question_index, score, quiz_active

    if not quiz_active or current_question_index >= len(questions):
        quiz_active = False
        messagebox.showinfo("Quiz Over", f"{username}'s score: {score}")
        save_score_to_file(username, score)  # Save score to file
        root.quit()
        return

    question_data = questions[current_question_index]
    question_label.config(text=f"Q{current_question_index + 1}: {question_data['question']}")

    for i, option in enumerate(question_data['options']):
        option_buttons[i].config(text=option, state=tk.NORMAL)

# Function to handle answer selection
def check_answer(selected_option, root, questions):
    global current_question_index, score, quiz_active

    if not quiz_active:
        return

    correct_answer = questions[current_question_index]['answer']
    if selected_option == correct_answer:
        score += 1

    current_question_index += 1
    display_question(root, questions)

# Function to save score to a file (append mode)
def save_score_to_file(username, score):
    try:
        with open("score.txt", "a") as file:  # Open in 'append' mode ('a')
            file.write(f"Username: {username}\n")
            file.write(f"Your score: {score}\n")
            file.write("-" * 30 + "\n")  # Add a separator for clarity between different sessions
        print(f"Score saved to score.txt: {username} - {score}")
    except Exception as e:
        print(f"Error saving score: {e}")

# Function to ask for username and start the quiz
def ask_for_username():
    global username  # Access the global variable `username`

    def submit_username():
        global username  # Access the global variable `username`
        username = username_entry.get().strip()
        if username:  # Ensure username is not empty
            username_window.destroy()  # Close the username entry window
            start_quiz()  # Start the quiz
        else:
            messagebox.showwarning("Input Error", "Please enter a valid username.")

    # Create a new Tkinter window to ask for the username
    username_window = tk.Tk()
    username_window.title("Enter Username")
    username_window.geometry("300x150")

    username_label = tk.Label(username_window, text="Enter your username:", font=("Helvetica", 12))
    username_label.pack(pady=10)

    global username_entry
    username_entry = tk.Entry(username_window, font=("Helvetica", 14), width=20)
    username_entry.pack(pady=5)

    submit_button = tk.Button(username_window, text="Submit", font=("Helvetica", 14), command=submit_username)
    submit_button.pack(pady=10)

    username_window.mainloop()

# Function to start the quiz
def start_quiz():
    global quiz_active

    # Load questions and duration
    filename = './questions.json'
    timer_duration, questions = load_quiz_data(filename)
    if not questions or timer_duration <= 0:
        return

    random.shuffle(questions)  # Shuffle questions

    # Create a new Tkinter window for the quiz
    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("600x400")

    # Timer
    global timer_label
    timer_label = tk.Label(root, text="", font=("Helvetica", 14))
    timer_label.pack(pady=10)

    # Question Label
    global question_label
    question_label = tk.Label(root, text="", wraplength=500, font=("Helvetica", 16))
    question_label.pack(pady=20)

    # Option Buttons
    global option_buttons
    option_buttons = []
    for i in range(4):
        btn = tk.Button(root, text="", font=("Helvetica", 14), width=30,
                        command=lambda i=i: check_answer(i + 1, root, questions))
        btn.pack(pady=5)
        option_buttons.append(btn)

    # Display the first question
    display_question(root, questions)

    # Start the timer using root.after
    quiz_active = True
    quiz_timer(timer_duration, root)

    # Start the Tkinter main loop
    root.mainloop()

# Main function
if __name__ == "__main__":
    ask_for_username()
