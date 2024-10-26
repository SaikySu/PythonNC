# main.py
import ttkbootstrap as ttkb
from db_setting import DatabaseConnection
from UI import DatabaseUI

def main():
    root = ttkb.Window(themename="cosmo")
    db = DatabaseConnection()
    app = DatabaseUI(root, db)
    root.mainloop()
    db.close()

if __name__ == "__main__":
    main()