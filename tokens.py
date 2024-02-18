class Token:
    def __init__(self, class_, lexeme, row=0, col=0):
        self.class_ = class_
        self.lexeme = lexeme
        self.row = row
        self.col = col

    def __str__(self):
        return "<{} {}. ({}, {})>".format(self.class_, self.lexeme, self.row, self.col)
    
    def get_pos(self):
        return (self.row, self.col)
        