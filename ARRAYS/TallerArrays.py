class ArrayWorkshop:
    def __init__(self):
        self.one_d = []
        self.two_d = []

    #1 Declaration and initialization 
    def create_1d_array(self):
        # Size 5, values you like
        self.one_d = ["Apple", "Book", "Coffee", "Desk", "Earphones"]
        print("1D array created:", self.one_d)

    def create_2d_array(self):
        
        self.two_d = [
            [10, 20, 30],
            [40, 50, 60],
            [70, 80, 90]
        ]
        print("\n2D array created:")
        self.print_2d()

    #2 Access
    def print_second_element_1d(self):
       
        value = self.one_d[1]
        print("\nSecond element in 1D array:", value)

    def print_second_row_second_col_2d(self):
        value = self.two_d[1][1]
        print("Element at (row 2, col 2) in 2D array:", value)

    #3 Insertion and deletion
    def insert_value_in_position_3(self, value="Estructura de datos"):
       
        self.one_d.insert(2, value)
        print(f"\nInserted '{value}' at position 3 in 1D array:")
        print(self.one_d)

    def delete_third_row_third_col(self):

        removed = self.two_d[2][2]
        self.two_d[2][2] = None  # keeps 3x3 structure
        print(f"\nDeleted element at (row 3, col 3). Removed value: {removed}")
        self.print_2d()

    #4 Search
    def find_in_1d(self, value="Estructura de datos"):
        if value in self.one_d:
            idx = self.one_d.index(value)
            print(f"\n'{value}' found in 1D array at index (0-based): {idx}")
            print(f"'{value}' found in 1D array at position (1-based): {idx + 1}")
        else:
            print(f"\n'{value}' not found in 1D array.")

    def find_in_second_row_2d(self, value):
   
        second_row = self.two_d[1]
        if value in second_row:
            col_idx = second_row.index(value)
            print(f"\n'{value}' found in 2D array (row 2) at column index (0-based): {col_idx}")
            print(f"'{value}' found in 2D array (row 2) at column position (1-based): {col_idx + 1}")
        else:
            print(f"\n'{value}' not found in the second row of the 2D array.")


    def print_2d(self):
        for row in self.two_d:
            print(row)


if __name__ == "__main__":
    workshop = ArrayWorkshop()

    # 1) Create arrays
    workshop.create_1d_array()
    workshop.create_2d_array()

    # 2) Access elements
    workshop.print_second_element_1d()
    workshop.print_second_row_second_col_2d()

    # 3) Insert / delete
    workshop.insert_value_in_position_3("Estructura de datos")
    workshop.delete_third_row_third_col()

    # 4) Search
    workshop.find_in_1d("Estructura de datos")
    workshop.find_in_second_row_2d(50)