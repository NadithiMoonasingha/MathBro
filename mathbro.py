import sys
import random
import datetime
import os
from typing import List, Dict, Tuple

class MathGame:
    def __init__(self, mode: str = "demo"):
        self.mode = mode
        self.modes = {
            "demo": {"ops": ["+"], "range": (0, 5), "questions": 3},
            "-e": {"ops": ["+", "-"], "range": (0, 10), "questions": 5},
            "-m": {"ops": ["+", "-"], "range": (0, 10), "questions": 10},
            "-h": {"ops": ["+", "-", "*"], "range": (0, 20), "questions": 10}
        }
        self.session_results = [] #To store the results of all sessions
        self.session_date = datetime.datetime.now() #Store the current date and time of the session
        self.session_id = self.session_date.strftime("%Y%m%d_%H%M")
        self.random_suffix = f"_{random.randint(100, 999)}" #Random suffix to differenciate the files of each session
        # Define symbols as class attributes
        self.TICK = '\u2713'  # Unicode for ✓(Correct answer)
        self.CROSS = '\u2717'  # Unicode for ✗(Wrong Answer)
        
    def format_date(self, date_format='dashed'):
        if date_format == 'dashed':
            return self.session_date.strftime("%Y-%m-%d")
        return self.session_date.strftime("%Y/%m/%d")

        
    def generate_question(self) -> Tuple[str, float]:
        #Generating random math question based on the selected mode
        mode_config = self.modes[self.mode]


        num1 = random.randint(*mode_config["range"])
        num2 = random.randint(*mode_config["range"])
        op = random.choice(mode_config["ops"])
        
        expression = f"{num1} {op} {num2}" #Formatting the math problem
        answer = eval(expression) #Calculate the correct answer using eva (eval= evaluating)
        
        return expression, answer
    
    def play_game(self) -> Dict:
        #Main game loop
        mode_config = self.modes[self.mode]
        questions = mode_config["questions"]
        results = [] #Store results of every question in a list
        correct_count = 0 #Correct answer count
        
        print(f"\nStarting new game in {self.mode} mode...")
        print(f"Answer {questions} questions:\n")
        
        for i in range(questions):
            question, correct_answer = self.generate_question()# Generating question
            print(f"Question {i + 1}: {question} = ", end="") #Display the question
            
            try:
                user_answer = float(input()) #Get the users input and convert it in to float
                is_correct =   user_answer==correct_answer #Check if the answer is correct
                #Append the answers and other details into the "results" dictionary
                results.append({ 
                    "question": question,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct
                }) 
                #If the answer is correct increase the correct answer count
                if is_correct:
                    correct_count += 1
                    
            #Handle the invalid inputs
            except ValueError:
                print("Invalid input. Counting as incorrect.")
                results.append({
                    "question": question,
                    "user_answer": "Invalid",
                    "correct_answer": correct_answer,
                    "is_correct": False
                })

        #Calculate the right answers count and display it as a percentage
        percentage = (correct_count / questions) * 100
        
        game_result = {
            "timestamp": datetime.datetime.now(),
            "mode": self.mode,
            "results": results,
            "total_questions": questions,
            "correct_count": correct_count,
            "percentage": percentage
        }
        
        self.session_results.append(game_result) # Save the results of the game session
        self.display_results(game_result) #Display the results to the user
        return game_result
    
    def display_results(self, game_result: Dict):
        print("\nGame Results:")
        print("-" * 50)
        
        for idx, result in enumerate(game_result["results"], 1):
            status = self.TICK if result["is_correct"] else self.CROSS
            print(f"Q{idx}: {result['question']} = {result['user_answer']} [{status}]")
            if not result["is_correct"]:
                print(f"   Correct answer: {result['correct_answer']}")
        
        print("-" * 50)
        print(f"Total Questions: {game_result['total_questions']}")
        print(f"Correct Answers: {game_result['correct_count']}")
        print(f"Percentage: {game_result['percentage']:.1f}%")
    
    def save_session(self):
        filename = f"{self.session_id}{self.random_suffix}.txt"
        formatted_date = self.format_date()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"MathsBro Game Session Report\n")
            f.write(f"Date: {formatted_date}\n")
            f.write(f"Time: {self.session_date.strftime('%H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            
            for game_num, game in enumerate(self.session_results, 1):
                f.write(f"Session {game_num}\n")
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
        
        print(f"\nSession saved to {filename}")

def save_as_html(game: MathGame):
    filename = f"{game.session_id}{game.random_suffix}.html"
    formatted_date = game.format_date()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>MathsBro Game Session Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .game {{ margin-bottom: 30px; border: 1px solid #ccc; padding: 15px; }}
            .correct {{ color: green; }}
            .incorrect {{ color: red; }}
            .question {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>MathsBro Game Session Report</h1>
        <p>Date: {formatted_date}</p>
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
            status = "correct" if result["is_correct"] else "incorrect"
            symbol = game.TICK if result["is_correct"] else game.CROSS
            html_content += f"""
            <div class="question {status}">
                Q{idx}: {result['question']} = {result['user_answer']} [{symbol}]
                {f"<br>Correct answer: {result['correct_answer']}" if not result["is_correct"] else ""}
            </div>
            """
        
        html_content += f"""
            <p>Total Questions: {game_result['total_questions']}</p>
            <p>Correct Answers: {game_result['correct_count']}</p>
            <p>Percentage: {game_result['percentage']:.1f}%</p>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML report saved to {filename}")
#Main program
def main():
    mode = "demo" if len(sys.argv) < 2 else sys.argv[1]
    
    if mode not in ["-e", "-m", "-h", "demo"]:
        print("Invalid mode. Using demo mode.")
        mode = "demo"
    
    game = MathGame(mode)
    
    while True:
        game.play_game()
        
        while True:
            play_again = input("\nWould like to play again? (y/n): ").lower()
            if play_again in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")
        
        if play_again == 'n':
            break
    
    game.save_session()
    save_as_html(game)

if __name__ == "__main__":
    main()
