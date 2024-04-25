import csv
import subprocess
import matplotlib.pyplot as plt

def run_file():
    x_win = []
    o_win = []
    draw = []

    for _ in range(100):
        command = "C:/Users/Chip/AppData/Local/Programs/Python/Python311/python.exe c:/Users/Chip/Desktop/CS_420/gen_ttt/game.py"
        result = subprocess.run(command.split(), capture_output=True, text=True)

        if result.stdout == "X won!\n":
            x_win.append(1)
        elif result.stdout == "O won!\n":
            o_win.append(1)
        else:
            draw.append(1)

    # Count the number of wins for each category
    x_win_count = len(x_win)
    o_win_count = len(o_win)
    draw_count = len(draw)

    # Plotting the bar graph
    categories = ['X wins', 'O wins', 'draw']
    counts = [x_win_count, o_win_count, draw_count]

    plt.bar(categories, counts, color=['blue', 'green', 'red'])
    plt.xlabel('Winners')
    plt.ylabel('Number of Wins')
    plt.title('Stage 4')
    plt.show()

    print(x_win_count)
    # with open('results.csv', 'a', newline='') as csvfile:
    #     count = [x_win_count]
    #     writer = csv.writer(csvfile)
    #     writer.writerow(count)

run_file()