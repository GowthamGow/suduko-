from flask import Flask, render_template, request, session
from random import randrange
import math
import copy

app = Flask(__name__)

class sudoku:
    def __init__(self, N, k):
        self.N = N
        self.k = k
        self.ans = None
        self.mat = list()
        self.SRN = int(math.sqrt(self.N))
        for i in range(self.N):
            self.mat.append([-1 for j in range(N)])

    def fillRemaining(self, i, j):
        if (j >= self.N and i < self.N - 1):
            i = i + 1
            j = 0
        if (i >= self.N and j >= self.N):
            return True
        if (i < self.SRN):
            if (j < self.SRN):
                j = self.SRN
        elif (i < self.N - self.SRN):
            if (j == (int)(i / self.SRN) * self.SRN):
                j = j + self.SRN
        else:
            if (j == self.N - self.SRN):
                i = i + 1
                j = 0
                if (i >= self.N):
                    return True
        for num in range(1, self.N + 1):
            if (self.CheckIfSafe(i, j, num)):
                self.mat[i][j] = num
                if (self.fillRemaining(i, j + 1)):
                    return True
                self.mat[i][j] = 0
        return False

    def removeKDigits(self):
        count = self.k
        while (count != 0):
            i = randrange(0, self.N)
            j = randrange(0, self.N)
            if (self.mat[i][j] != 0):
                count -= 1
                self.mat[i][j] = 0

    def fillValues(self):
        self.fillDiagonal()
        self.fillRemaining(0, self.SRN)
        self.ans = copy.deepcopy(self.mat)
        self.removeKDigits()

    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)

    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if (self.mat[rowStart + i][colStart + j] == num):
                    return False
        return True

    def fillBox(self, row, col):
        for i in range(self.SRN):
            for j in range(self.SRN):
                num = randrange(1, self.N + 1)
                while (not self.unUsedInBox(row, col, num)):
                    num = randrange(1, self.N + 1)
                self.mat[row + i][col + j] = num

    def CheckIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN,
                                                                                           j - j % self.SRN, num))

    def unUsedInRow(self, i, num):
        for j in range(0, self.N):
            if (self.mat[i][j] == num):
                return False
        return True

    def unUsedInCol(self, j, num):
        for i in range(0, self.N):
            if (self.mat[i][j] == num):
                return False
        return True


def usedbox(arr, row, col, num, r, c):
    for i in range(3):
        for j in range(3):
            if(arr[i + row][j + col] == num and not((i+row == r) and (j+col == c))):
                return True
    return False


def usedcol(arr, row, col, num):
    for i in range(9):
        if(arr[i][col] == num and i != row):
            return True
    return False


def usedrow(arr, row, col, num):
    for i in range(9):
        if(arr[row][i] == num and i != col):
            return True
    return False


def locationsafe(mat):
    for i in range(9):
        for j in range(9):
            if(not usedrow(mat, i, j, mat[i][j]) and not usedcol(mat, i, j, mat[i][j]) and not usedbox(mat, i - i % 3, j - j % 3, mat[i][j], i, j)):
                continue
            else:
                return False
    return True


qus = []
answer = []


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        p1 = sudoku(9, 20)
        p1.fillValues()
        global qus
        global answer
        q, ans, qus, answer = p1.mat, p1.ans, p1.mat, p1.ans
        fls = []
        for k in range(9):
            rowls = []
            for l in range(9):
                colls = []
                if q[k][l] != 0:
                    colls.append(q[k][l])
                    colls.append("disabled")
                    colls.append(str(k)+str(l))
                else:
                    colls.append("")
                    colls.append("required")
                    colls.append(str(k)+str(l))
                rowls.append(colls)
            fls.append(rowls)
        return render_template("index1.html", ls=fls)


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        result = request.form
        global qus
        for i, k in result.items():
            a, b = int(i[0]), int(i[1])
            qus[a][b] = k
        if locationsafe(qus):
            return '<h1 align="center">Your answer is correct</h1><div><a href="/" ><button style="display: block;margin-left: auto;margin-right: auto;" class="btn" >New game</button></a></div>'
        else:
            return render_template("ans.html", ls=answer, comment='Your answer is Worng')


@app.route('/ans')
def ans():
    return render_template("ans.html", ls=answer)


if __name__ == "__main__":
    app.run(port=6020)
