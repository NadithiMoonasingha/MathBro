import random
import datetime
import tkinter as tk
from tkinter import messagebox
from typing import Tuple


class MathGame:
    def __init__(self, mode: str = "demo"):
        self.mode = mode

        self.modes = {
            "demo": {"ops": ["+"], "range": (0, 5), "questions": 3},
            "-e": {"ops": ["+", "-"], "range": (0, 10), "questions": 5},
            "-m": {"ops": ["+", "-"], "range": (0, 10), "questions": 10},
            "-h": {"ops": ["+", "-", "*"], "range": (0, 20), "questions": 10}
        }

        self.session_results = []
        self.session_date = datetime.datetime.now()
        self.session_id = self.session_date.strftime("%Y%m%d_%H%M")
        self.random_suffix = f"_{random.randint(100, 999)}"

        self.TICK = "\u2713"
        self.CROSS = "\u2717"

    def format_date(self):
        return self.session_date.strftime("%Y-%m-%d")

    def generate_question(self) -> Tuple[str, int]:
        mode_config = self.modes[self.mode]

        num1 = random.randint(*mode_config["range"])
        num2 = random.randint(*mode_config["range"])
        op = random.choice(mode_config["ops"])

        expression = f"{num1} {op} {num2}"

        if op == "+":
            answer = num1 + num2
        elif op == "-":
            answer = num1 - num2
        elif op == "*":
            answer = num1 * num2

        return expression, answer

    def save_session(self):
        filename = f"{self.session_id}{self.random_suffix}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("MathsBro Game Session Report\n")
            f.write(f"Date: {self.format_date()}\n")
            f.write(f"Time: {self.session_date.strftime('%H:%M')}\n")
            f.write("=" * 50 + "\n\n")

            for game_num, game in enumerate(self.session_results, 1):
                f.write(f"Game {game_num}\n")
                f.write(f"Mode: {game['mode']}\n")
                f.write(f"Time: {game['timestamp'].strftime('%H:%M:%S')}\n\n")

                for idx, result in enumerate(game["results"], 1):
                    status = self.TICK if result["is_correct"] else self.CROSS
                    f.write(f"Q{idx}: {result['question']} = {result['user_answer']} [{status}]\n")

                    if not result["is_correct"]:
                        f.write(f"   Correct answer: {result['correct_answer']}\n")

                f.write(f"\nTotal Questions: {game['total_questions']}\n")
                f.write(f"Correct Answers: {game['correct_count']}\n")
                f.write(f"Percentage: {game['percentage']:.1f}%\n")
                f.write("\n" + "-" * 50 + "\n\n")

        return filename


def save_as_html(game: MathGame):
    filename = f"{game.session_id}{game.random_suffix}.html"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MathsBro Game Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
            background-color: #f7f4ff;
            color: #222;
        }}

        h1 {{
            color: #5b2c83;
        }}

        .game {{
            background-color: white;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }}

        .correct {{
            color: green;
        }}

        .incorrect {{
            color: red;
        }}
    </style>
</head>
<body>
    <h1>MathsBro Game Session Report</h1>
    <p>Date: {game.format_date()}</p>
    <p>Time: {game.session_date.strftime('%H:%M')}</p>
"""

    for game_num, game_result in enumerate(game.session_results, 1):
        html_content += f"""
    <div class="game">
        <h2>Game {game_num}</h2>
        <p>Mode: {game_result['mode']}</p>
        <p>Time: {game_result['timestamp'].strftime('%H:%M:%S')}</p>
"""

        for idx, result in enumerate(game_result["results"], 1):
            css_class = "correct" if result["is_correct"] else "incorrect"
            symbol = game.TICK if result["is_correct"] else game.CROSS

            html_content += f"""
        <p class="{css_class}">
            Q{idx}: {result['question']} = {result['user_answer']} [{symbol}]
"""

            if not result["is_correct"]:
                html_content += f"<br>Correct answer: {result['correct_answer']}"

            html_content += "</p>"

        html_content += f"""
        <p><strong>Total Questions:</strong> {game_result['total_questions']}</p>
        <p><strong>Correct Answers:</strong> {game_result['correct_count']}</p>
        <p><strong>Percentage:</strong> {game_result['percentage']:.1f}%</p>
    </div>
"""

    html_content += """
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filename


class MathGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MathsBro Quiz Game")
        self.root.geometry("650x720")
        self.root.configure(bg="#1E262F")

        self.game = None
        self.current_question = ""
        self.correct_answer = 0
        self.question_number = 0
        self.correct_count = 0
        self.results = []

        self.create_widgets()

    def create_widgets(self):
        BG_DARK = "#1E262F"         # Black Pearl
        BG_CARD = "#415365"         # Into the Stratosphere
        BLUE_SOFT = "#697F93"       # Blue Prince
        GREY_SOFT = "#9D9F97"       # Wet Pavement
        TEXT_LIGHT = "#D6D4C9"      # Soft Secret

        BUTTON_START = "#D6D4C9"    # light contrasting button
        BUTTON_START_HOVER = "#c9c6b9"

        BUTTON_SUBMIT = "#697F93"   # blue contrasting button
        BUTTON_SUBMIT_HOVER = "#5d7185"

        ENTRY_BG = "#D6D4C9"
        ENTRY_TEXT = "#1E262F"

        self.main_frame = tk.Frame(self.root, bg=BG_DARK)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        title = tk.Label(
            self.main_frame,
            text="MathsBro Quiz Game",
            font=("Arial", 28, "bold"),
            bg=BG_DARK,
            fg=TEXT_LIGHT
        )
        title.pack(pady=(15, 20))

        mode_text = tk.Label(
            self.main_frame,
            text="Choose a difficulty level",
            font=("Arial", 15, "bold"),
            bg=BG_DARK,
            fg=TEXT_LIGHT
        )
        mode_text.pack(pady=(5, 10))

        self.mode_var = tk.StringVar(value="demo")

        mode_frame = tk.Frame(self.main_frame, bg=BG_DARK)
        mode_frame.pack(pady=10)

        radio_style = {
            "variable": self.mode_var,
            "bg": BG_DARK,
            "fg": TEXT_LIGHT,
            "selectcolor": BG_DARK,
            "activebackground": BG_DARK,
            "activeforeground": TEXT_LIGHT,
            "font": ("Arial", 12),
            "highlightthickness": 0,
            "bd": 0
        }

        tk.Radiobutton(mode_frame, text="Demo", value="demo", **radio_style).grid(row=0, column=0, padx=15)
        tk.Radiobutton(mode_frame, text="Easy", value="-e", **radio_style).grid(row=0, column=1, padx=15)
        tk.Radiobutton(mode_frame, text="Medium", value="-m", **radio_style).grid(row=0, column=2, padx=15)
        tk.Radiobutton(mode_frame, text="Hard", value="-h", **radio_style).grid(row=0, column=3, padx=15)

        self.start_button = tk.Button(
            self.main_frame,
            text="Start Game",
            font=("Arial", 14, "bold"),
            width=18,
            height=2,
            bg=BUTTON_START,
            fg=BG_DARK,
            activebackground=BUTTON_START_HOVER,
            activeforeground=GREY_SOFT,
            disabledforeground="#7b7b7b",
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            command=self.start_game
        )
        self.start_button.pack(pady=20)

        # Question card
        self.question_card = tk.Frame(
            self.main_frame,
            bg=BG_CARD,
            bd=0,
            highlightthickness=0
        )
        self.question_card.pack(fill="x", pady=(10, 25), padx=30)

        self.question_label = tk.Label(
            self.question_card,
            text="Question will appear here",
            font=("Arial", 24, "bold"),
            bg=BG_CARD,
            fg=TEXT_LIGHT,
            pady=25
        )
        self.question_label.pack()

        answer_label = tk.Label(
            self.main_frame,
            text="Enter your answer:",
            font=("Arial", 14, "bold"),
            bg=BG_DARK,
            fg=TEXT_LIGHT
        )
        answer_label.pack(pady=(5, 8))

        self.answer_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 22, "bold"),
            justify="center",
            width=15,
            bg=ENTRY_BG,
            fg=ENTRY_TEXT,
            insertbackground=ENTRY_TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        self.answer_entry.pack(pady=10, ipady=10)
        self.answer_entry.config(state="disabled")

        self.submit_button = tk.Button(
            self.main_frame,
            text="Submit Answer",
            font=("Arial", 13, "bold"),
            width=18,
            height=2,
            bg=BUTTON_SUBMIT,
            fg=BLUE_SOFT,
            activebackground=BUTTON_SUBMIT_HOVER,
            activeforeground=BLUE_SOFT,
            disabledforeground="#c0c0c0",
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            command=self.submit_answer
        )
        self.submit_button.pack(pady=15)
        self.submit_button.config(state="disabled")

        self.feedback_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 15, "bold"),
            bg=BG_DARK,
            fg=TEXT_LIGHT
        )
        self.feedback_label.pack(pady=(10, 8))

        self.score_label = tk.Label(
            self.main_frame,
            text="Score: 0 / 0",
            font=("Arial", 15, "bold"),
            bg=BG_DARK,
            fg=TEXT_LIGHT
        )
        self.score_label.pack(pady=(5, 10))

        self.result_text = tk.Text(
            self.main_frame,
            width=60,
            height=10,
            font=("Arial", 11),
            bg=BG_CARD,
            fg=TEXT_LIGHT,
            insertbackground=TEXT_LIGHT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=15,
            pady=12
        )
        self.result_text.pack(pady=15)
        self.result_text.config(state="disabled")

        self.root.bind("<Return>", lambda event: self.submit_answer())

    def start_game(self):
        selected_mode = self.mode_var.get()

        self.game = MathGame(selected_mode)

        self.question_number = 0
        self.correct_count = 0
        self.results = []

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

        self.feedback_label.config(text="")
        self.score_label.config(text="Score: 0 / 0")

        self.answer_entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.start_button.config(state="disabled")

        self.next_question()

    def next_question(self):
        total_questions = self.game.modes[self.game.mode]["questions"]

        if self.question_number < total_questions:
            self.question_number += 1
            self.current_question, self.correct_answer = self.game.generate_question()

            #print(f"Question {self.question_number}: {self.current_question} = ?")

            self.question_label.config(
                text=f"Question {self.question_number}:   {self.current_question} = ?"
            )

            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()

        else:
            self.finish_game()

    def submit_answer(self):
        if self.game is None:
            return

        user_input = self.answer_entry.get().strip()

        if user_input == "":
            messagebox.showwarning("Empty Answer", "Please enter an answer.")
            return

        try:
            user_answer = float(user_input)

            if user_answer == self.correct_answer:
                is_correct = True
                self.correct_count += 1
                self.feedback_label.config(text="Correct!", fg="#D6D4C9")
            else:
                is_correct = False
                self.feedback_label.config(
                    text=f"Invalid input! Correct answer is {self.correct_answer}",
                    fg="#9D9F97"
                )

        except ValueError:
            user_answer = "Invalid"
            is_correct = False
            self.feedback_label.config(
                text=f"Wrong! Correct answer is {self.correct_answer}",
                fg="#9D9F97"
            )

        self.results.append({
            "question": self.current_question,
            "user_answer": user_answer,
            "correct_answer": self.correct_answer,
            "is_correct": is_correct
        })

        total_questions = self.game.modes[self.game.mode]["questions"]
        self.score_label.config(text=f"Score: {self.correct_count} / {total_questions}")

        self.show_result_line(is_correct, user_answer)

        self.root.after(800, self.next_question)

    def show_result_line(self, is_correct, user_answer):
        symbol = self.game.TICK if is_correct else self.game.CROSS

        self.result_text.config(state="normal")
        self.result_text.insert(
            tk.END,
            f"Q{self.question_number}: {self.current_question} = {user_answer} [{symbol}]\n"
        )

        if not is_correct:
            self.result_text.insert(
                tk.END,
                f"   Correct answer: {self.correct_answer}\n"
            )

        self.result_text.insert(tk.END, "\n")
        self.result_text.config(state="disabled")

    def finish_game(self):
        total_questions = self.game.modes[self.game.mode]["questions"]
        percentage = (self.correct_count / total_questions) * 100

        game_result = {
            "timestamp": datetime.datetime.now(),
            "mode": self.game.mode,
            "results": self.results,
            "total_questions": total_questions,
            "correct_count": self.correct_count,
            "percentage": percentage
        }

        self.game.session_results.append(game_result)

        self.question_label.config(text="Game Finished!")
        self.feedback_label.config(
            text=f"Final Score: {self.correct_count}/{total_questions} | {percentage:.1f}%",
            fg="#D6D4C9"
        )

        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.start_button.config(state="normal")

        txt_file = self.game.save_session()
        html_file = save_as_html(self.game)

        messagebox.showinfo(
            "Game Finished",
            f"Your score is {self.correct_count}/{total_questions}\n"
            f"Percentage: {percentage:.1f}%\n\n"
            f"Saved as:\n{txt_file}\n{html_file}"
        )


def main():
    root = tk.Tk()
    app = MathGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()