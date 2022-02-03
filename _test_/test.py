import pytest
import sys
import random
import os
import io
from schema import Schema
from src import table
from contextlib import redirect_stdout, contextmanager


@contextmanager
def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


teams = ["Wolves", "Parrots", "Monkeys", "Wild Dogs", "Ducks"]
dictionary = Schema({str: str, str: int})


class Test:
    # Test splitting of teams matches schema
    def test_one(self):
        print("inicando prueba")
        file = open("test.txt", "w")
        for i in range(8):
            randomMatch = random.sample(teams, 2)
            file.write("{} {}, {} {}\n".format(randomMatch[0], random.randint(
                0, 4), randomMatch[1], random.randint(0, 4)))
        file.close()
        emptyTeams = {}
        matchResult = {}
        with open(os.path.dirname(__file__) + '/../test.txt') as file:
            line = file.readline()
        table.splitNameAndScore(line, emptyTeams, matchResult)
        print(matchResult)
        assert dictionary.validate(matchResult)

    # Test getting winner
    def test_two(self):
        testMatch = {
            "Wolves": 0,
            "Parrots": 2
        }
        result = table.getWinner(testMatch)
        assert result == "Parrots"

    # Test getting a tie
    def test_three(self):
        testMatch = {
            "Wolves": 0,
            "Parrots": 0
        }
        result = table.getWinner(testMatch)
        assert result == False

    # Test getting sorted dictionary by value in ascending order
    def test_four(self):
        testDict = {}
        for i in teams:
            testDict[i] = random.randint(0, 12)
        testDict = table.orderTable(testDict)
        idx = 1
        for v in testDict:
            print(v)
            if(v[0] == testDict[-1][0]):
                break
            if(v[1] > testDict[idx][1]):
                assert False
            idx += 1
        assert True
