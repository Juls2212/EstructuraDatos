class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
        return None

    def is_empty(self):
        return len(self._items) == 0


class File:
    def __init__(self, name):
        self.name = name
        self.folder = "Desktop"
        self.is_zipped = False

    def show_state(self):
        print("\nCurrent File State:")
        print(f"Name: {self.name}")
        print(f"Folder: {self.folder}")
        print(f"Zipped: {self.is_zipped}")


class SubmissionManager:
    def __init__(self, file):
        self.file = file
        self.history = Stack()

    def rename(self, new_name):
        old_name = self.file.name
        print(f"Renaming {old_name} -> {new_name}")
        self.file.name = new_name
        self.history.push(lambda: self._undo_rename(old_name))

    def zip_file(self):
        print("Compressing file...")
        self.file.is_zipped = True
        self.history.push(lambda: self._undo_zip())

    def move_to_submission(self):
        old_folder = self.file.folder
        print("Moving file to SUBMISSION folder")
        self.file.folder = "SUBMISSION"
        self.history.push(lambda: self._undo_move(old_folder))

    def undo_last(self):
        print("\nUndoing last action...")
        undo_action = self.history.pop()
        if undo_action:
            undo_action()
        else:
            print("Nothing to undo.")

    def _undo_rename(self, old_name):
        print(f"Reverting name back to {old_name}")
        self.file.name = old_name

    def _undo_zip(self):
        print("Reverting compression")
        self.file.is_zipped = False

    def _undo_move(self, old_folder):
        print(f"Moving file back to {old_folder}")
        self.file.folder = old_folder


file = File("report.pdf")
manager = SubmissionManager(file)

file.show_state()

manager.rename("final_report.pdf")
manager.zip_file()
manager.move_to_submission()

file.show_state()

manager.undo_last()
manager.undo_last()

file.show_state()