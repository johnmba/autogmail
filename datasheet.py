
from tksheet import Sheet


class Datasheet(Sheet):
    
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(parent=master, *args, **kwargs)
        
        self.heading = ['Full name', 'Username', 'Address', 'Password', "Active", "Registered", "Date"]
        self.headers(self.heading)
        self.column_width(column=1, width=180, only_set_if_too_small=False)
        self.column_width(column=2, width=200, only_set_if_too_small=False)
        self.column_width(column=3, width=180, only_set_if_too_small=False)
        self.column_width(column=4, width=150, only_set_if_too_small=False)
        self.column_width(column=6, width=100, only_set_if_too_small=False)
        self.enable_bindings('all')
        self.disable_bindings([
            'rc_insert_column', 'rc_delete_column', 'edit_cell', 'delete', 'paste',
            'cut', 'rc_delete_row', 'rc_insert_row'
        ])
        
    def add(self, data):
           
        if type(data) is dict:
            self.insert_row(
                values=(
                    data['fullname'], data['username'], data['address'], data['password'], 
                    data["active"], data["registered"], data["dated"]
                ), idx='end', add_columns=False
            )
        else:
            self.heading.insert(0, 'ID')
            self.column_width(column=0, width=50, only_set_if_too_small=False)
            self.insert_row(
                values=(
                    data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]
                ), idx='end', add_columns=False
            )
        
    def clear(self):
        self.select_all(redraw=False, run_binding_func=True)
        rows_number = len(self.get_selected_rows(get_cells_as_rows=True))
        self.MT.del_row_positions(idx=0, numrows=rows_number, deselect_all=True)