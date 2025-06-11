from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResolutionWindow(object):
    def setupUi(self, ResolutionWindow):
        ResolutionWindow.setObjectName("ResolutionWindow")
        ResolutionWindow.resize(600, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(ResolutionWindow)
        self.labelInput = QtWidgets.QLabel("შეიყვანე კლაუსები (CNF): თითო ხაზზე თითო კლაუსი")
        self.verticalLayout.addWidget(self.labelInput)

        self.inputClauses = QtWidgets.QTextEdit()
        self.verticalLayout.addWidget(self.inputClauses)

        self.btnResolve = QtWidgets.QPushButton("გაშვება (რეზოლუციის ალგორითმი)")
        self.verticalLayout.addWidget(self.btnResolve)

        self.labelOutput = QtWidgets.QLabel("რეზულტატი:")
        self.verticalLayout.addWidget(self.labelOutput)

        self.outputResult = QtWidgets.QTextEdit()
        self.outputResult.setReadOnly(True)
        self.verticalLayout.addWidget(self.outputResult)

        self.btnResolve.clicked.connect(self.run_resolution)

    def run_resolution(self):
        input_text = self.inputClauses.toPlainText().strip()
        lines = input_text.split("\n")
        clauses = [parse_clause(line) for line in lines if line.strip()]

        result_log = "რეზოლუციის დაწყება...\n\n"
        contradiction, log = resolution_algorithm(clauses)
        result_log += log
        result_log += "\n\nშედეგი: "
        result_log += "ფორმულა არის UNSAT (წინააღმდეგობა!)" if contradiction else "ფორმულა შეიძლება დაკმაყოფილდეს (SAT)"

        self.outputResult.setPlainText(result_log)


def parse_clause(clause_str):
    parts = clause_str.split("∨")
    return [p.strip() for p in parts if p.strip()]

def negate(literal):
    return literal[1:] if literal.startswith("¬") else "¬" + literal

def resolve(c1, c2):
    for lit1 in c1:
        opposite = negate(lit1)
        if opposite in c2:
            new_clause = [l for l in c1 if l != lit1]
            new_clause += [l for l in c2 if l != opposite and l not in new_clause]
            return new_clause
    return None

def resolution_algorithm(clauses):
    new_clauses = []
    log = ""
    while True:
        added = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = resolve(clauses[i], clauses[j])
                if resolvent is not None:
                    log += f"რეზოლუცია: {clauses[i]} + {clauses[j]} → {resolvent}\n"
                    if resolvent == []:
                        log += "მივიღეთ ცარიელი კლაუსი → წინააღმდეგობა!\n"
                        return True, log
                    if resolvent not in clauses and resolvent not in new_clauses:
                        new_clauses.append(resolvent)
                        added = True
        if not added:
            log += "ახალი კლაუსები აღარ მიიღება → წინააღმდეგობა ვერ დადგინდა.\n"
            return False, log
        clauses += new_clauses
        new_clauses = []

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ResolutionWindow = QtWidgets.QWidget()
    ui = Ui_ResolutionWindow()
    ui.setupUi(ResolutionWindow)
    ResolutionWindow.show()
    sys.exit(app.exec_())
