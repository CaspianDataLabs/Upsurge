class Cell:
    def __init__(self, content: str):
        self.content : str = content
        
class Table:
    def __init__(self, name: str):
        self.name : str = name

class Section:
    def __init__(self, title: str):
        self.title = title

class Report:
    def __init__(self, title: str):
        self.title = title
        self.sections : list[Section] = []