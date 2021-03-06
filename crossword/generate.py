import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        # print("Final assignment: ",assignment)
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                # print("word: ",word,"letter: ",word[k])
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            for w in self.domains[v].copy():
                if(len(w) != v.length):
                    self.domains[v].remove(w)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if (x, y) in self.crossword.overlaps:
            #if given variables x and y overlap then we go to revise
            if(self.crossword.overlaps[(x,y)] is not None):
                #index of the letters in x and y that needs to be equal in tuple (xIndex, yIndex)
                letterIndex = self.crossword.overlaps[(x,y)]
                for wordX in self.domains[x].copy():
                    count = 0
                    for wordY in self.domains[y]:
                        #if the letter at index overlapped break the loop
                        if(wordX[letterIndex[0]] == wordY[letterIndex[1]]):
                            break
                        #if not raise count
                        else:
                            count += 1
                    #if not overlapped until the end of the list remove the word
                    if(len(self.domains[y]) == count):
                        self.domains[x].remove(wordX)
                        revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        aQueue = arcs
        if(aQueue is None):
            aQueue = []
            for i in self.crossword.variables:
                for j in self.crossword.variables:
                    if(i != j):
                        aQueue.append((i,j))
        while(len(aQueue) > 0):
            (X, Y) = aQueue.pop(0)
            # print(self.domains[X], " => ", self.domains[Y])
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                for Z in self.crossword.neighbors(X):
                    if(Z != Y):
                        aQueue.append((Z, X))
            # print([(self.domains[k[0]], self.domains[k[1]]) for k in aQueue])
            # print(aQueue)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if(len(assignment) == 0):
            return False
        for variable in assignment:
            #if the variable is assigned more than just one word, then return false
            if len(self.domains[variable]) < 1:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #function assumes that enforce_node_consistency() is applied already
        # print("my assignment",assignment)
        for variable in assignment:
            #if words are not distinct in assignment return False
            # print("Error: ",variable," => ",assignment[variable])
            if(len(self.domains[variable]) != len(set(self.domains[variable]))):
                # print("length fault")
                return False
            for neighbor in self.crossword.neighbors(variable): #neighbor of variable
                for wN in self.domains[neighbor].copy(): #words in neighbors
                    for wV in self.domains[variable].copy(): #words in variable itself
                        if(wN == wV):
                            if len(self.domains[variable]) > len(self.domains[neighbor]):
                                self.domains[variable].remove(wV)
                            else:
                                self.domains[neighbor].remove(wN)
                        overLapIndex = self.crossword.overlaps[(variable,neighbor)] # index where letter should be overlapped
                        if(wV[overLapIndex[0]] != wN[overLapIndex[1]]): #if letter don't overlap at given index then return False
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #dictionary mapping variable and count of elimination in neighbor variables
        dictionary = dict()
        aVar = self.select_unassigned_variable(assignment)
        surrounding = self.crossword.neighbors(aVar)
        # print(self.select_unassigned_variable(assignment), "'s surrounding: ",surrounding)
        # print(aVar,"'s surrounding",surrounding)
        for neighbor in surrounding:
            # print("ran")
            if neighbor not in assignment:
                count = 0
                for wN in self.domains[neighbor]: #words in neighbors
                    for wV in self.domains[var]: #words in variable itself
                        overLapIndex = self.crossword.overlaps[(var,neighbor)] # index where letter should be overlapped
                        if(wV[overLapIndex[0]] != wN[overLapIndex[1]]): #if letter don't overlap at given index
                            count += 1
                        # if(wV[overLapIndex[0]] == wN[overLapIndex[1]]):
                        #     print(wV," => ",wN)
                dictionary[wV] = count
                # print(dictionary)
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
            ans = [k for k in dictionary]
        return ans

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        ans = dict()
        max = float('inf') #biggest number integer
        for variable in self.domains:
            if variable not in assignment:
                if len(self.domains[variable]) < max:
                    ans = dict()
                    ans[variable] = len(self.crossword.neighbors(variable))
                    max = len(self.domains[variable])
                if len(self.domains[variable]) == max:
                    ans[variable] = len(self.crossword.neighbors(variable))
        ans = dict(sorted(ans.items(), key=lambda item: item[1]))
        return list(ans)[-1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        import random
        #check if assignment is complete
        if(self.assignment_complete(assignment)):
            return assignment
        var = self.select_unassigned_variable(assignment)
        # print("my var: ",self.domains[var])
        # print(self.domains)
        for value in self.order_domain_values(var, assignment):
            # print("assignment for self.consistent: ",self.order_domain_values(var, assignment))
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(self.crossword.neighbors(var)):
                assignment[var] = list(self.domains[var])[0]
                result = self.backtrack(assignment)
                # print("result: ",result)
                # print(assignment, " => ", result)
                temp = {}
                # print(self.domains)
                for k in self.domains:
                    #if there are more than 1 word that works then choose one in random
                    temp[k]=random.choice(list(self.domains[k]))
                if result is not None:
                    return temp
                # print("removed ",var)
                assignment.remove(var)
        return None
        



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
