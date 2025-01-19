# imports
import random
import pathlib
import countdown_solver
import helper

# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()
        target = random.randint(100, 1000)
        selected = helper.get_countdown_number_selection()
        countdown_solver.OPTIMIZE = 1
        (answers_list, summary) = countdown_solver.solve(selected, target)
        string = f"- Target: {target}, using {selected}\n"
        if answers_list:
            string += "<details><summary><code>Solution</code></summary>\n\n"
            string += f"\nSolution: {answers_list[0]}\n\n"
            string += f"{summary}\n\n"
            string += "</details>\n"
        f = root / "_pages/morning.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "game_marker", f"\n{string}")
        f.open("w").write(c)
        print("Game Completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
