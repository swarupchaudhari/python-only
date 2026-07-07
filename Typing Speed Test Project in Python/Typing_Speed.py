import time
import random

# List of sentences
sentences = [
    "Python is a powerful programming language.",
    "Practice makes a person perfect.",
    "Data science is the future of technology.",
    "Typing fast requires regular practice.",
    "Artificial intelligence is changing the world."
]

def typing_test():
    # Select a random sentence
    test_sentence = random.choice(sentences)

    print("===== Typing Speed Test =====")
    print("\nType the following sentence:\n")
    print(test_sentence)

    input("\nPress Enter to start...")

    # Start timer
    start_time = time.time()

    # User input
    typed_text = input("\nType here: ")

    # End timer
    end_time = time.time()

    # Calculate time
    time_taken = end_time - start_time

    # Calculate typing speed (Words Per Minute)
    word_count = len(test_sentence.split())
    wpm = (word_count / time_taken) * 60

    print("\n===== Result =====")
    print(f"Time Taken: {time_taken:.2f} seconds")
    print(f"Typing Speed: {wpm:.2f} WPM")

    # Check accuracy
    if typed_text == test_sentence:
        print("Accuracy: 100%")
        print("Excellent! You typed correctly.")
    else:
        correct_chars = 0
        for i in range(min(len(typed_text), len(test_sentence))):
            if typed_text[i] == test_sentence[i]:
                correct_chars += 1

        accuracy = (correct_chars / len(test_sentence)) * 100
        print(f"Accuracy: {accuracy:.2f}%")
        print("Keep practicing!")

# Run the program
typing_test()