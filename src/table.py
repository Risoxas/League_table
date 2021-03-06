# table.py
# Read input from file or any source of text
import re
import sys
import glob
import os


def getWinner(matchResult):
    # Compare values in dictionary to find same score
    if(len(list(set(list(matchResult.values())))) == 1):
        return False
    else:
        return max(matchResult, key=matchResult.get)


def splitNameAndScore(*args):
    line, teams, matchResult = args[0], args[1], args[2]
    score = line.split(', ')
    splitScore = re.compile("([a-zA-Z ]+)([0-9]+)")
    for team in score:
        try:
            team = splitScore.match(team).groups()
        except:
            print("\nPlease choose a valid file")
            sys.exit()
        teamName = team[0].rstrip()
        if not teamName in teams:
            teams[teamName] = 0
        teamScore = int(team[1])
        matchResult[teamName] = teamScore


def orderTable(teams):
    teams = sorted(teams.items(), key=lambda x: (x[1], x[0]), reverse=True)
    teams = {teams[i][0]: teams[i][1] for i in range(0, len(teams))}
    return sorted(teams.items(), key=lambda x: (x[1]))


def main():
    # Look for files in root directory
    path = os.path.abspath(__file__ + "/../../")
    os.chdir(path)
    files = []
    for file in glob.glob("*.txt"):
        files.append(file)
    files = tuple(files)
    text = 'Select your file'
    idx = 1
    for file in files:
        text += '\n' + str(idx) + ' ' + file + ' '
        idx += 1

    if files:
        valid = False
        while valid == False:
            try:
                selection = int(input(text + '\n'))
            except:
                print("Invalid input")
                sys.exit()
            if(selection - 1 >= len(files)):
                print("choose a valid file from the list")
            else:
                valid = True
        files = files[selection-1]
        with open(files) as file:
            lines = file.readlines()

    # insert manually or use sample file
    else:
        answer = input("Do you want to use sample input? (yes or no)\n")
        if(answer.lower() == 'yes'):
            with open(os.path.dirname(__file__) + '/../sample/sample.txt') as file:
                lines = file.readlines()
        else:

            lines = []
            print("Please manually add the results and press enter when done")
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break

    teams = {}
    for line in lines:
        # generate dictionary with key value pairs
        matchResult = {}
        # retrieve team name and score in two different collections
        splitNameAndScore(line, teams, matchResult)
        # compare scores to decide winner
        result = getWinner(matchResult)
        # Compute points for each team
        if result == False:
            for team in matchResult:
                teams[team] = teams.get(team, 0) + 1
        else:
            teams[result] = teams.get(result, 0) + 3
    # Order table by value and key in descending order
    teams = orderTable(teams)
    idx = 1
    for item in reversed(teams):
        place, name, score = idx, item[0], item[1]
        if(idx > 1):
            prevScore = teams[len(teams) + 1 - idx][1]
        try:
            if(prevScore == score):
                prevPlace += 1
                place -= prevPlace
            else:
                prevPlace = 0

        except:
            pass
        print("{}. {}, {} {}".format(place, name,
              score, 'pts' if score != 1 else 'pt'))
        idx += 1


if __name__ == "__main__":
    main()
    input("\nPress enter key to exit")
