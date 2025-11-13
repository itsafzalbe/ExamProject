from postgreSQL import ConnectData


db = ConnectData(
    dbname='ExamDB',
    user='postgres',
    password='123',
    host='localhost',
    port=5433
)

def admin_menu(user):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Edit Product")
        print("5. View Balance")
        print("6. View Sold Items")
        print("7. Edit Your Info")
        print("8. Show Users")
        print("0. Logout")
        choice = input("Your choice: ")
        if choice == "1":
            db.view_products_admin()
        elif choice == "2":
            db.add_product_admin()
        elif choice == "3":
            db.remove_product_admin()
        elif choice == "4":
            db.edit_product_admin()
        elif choice == "5":
            db.view_shop_balance_admin()
        elif choice == "6":
            db.view_sold_items()
        elif choice == "7":
            db.edit_info_users(user)
        elif choice == "8":
            db.show_users()
        elif choice == "0":
            break
def customer_menu(user):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. View and Add products to the Basket")
        print("2. View Items in Basket")
        print("3. Edit Basket Items")
        print("4. Proceed to payment")
        print("5. Edit Your Info")
        print("6. View Balance")
        print("7. Top your Balance")
        print("0. Log out")
        choice = input("Your choice: ")
        if choice == "1":
            db.view_and_buy_products_user(user)
        elif choice == "2":
            db.view_basket(user['id'])
        elif choice == "3":
            db.edit_basket(user['id'])
        elif choice == "4":
            db.proceed_to_payment(user)
        elif choice == "5":
            db.edit_info_users(user)
        elif choice == "6":
            db.view_user_balance(user)
        elif choice == "7":
            db.top_up_balance_user(user)
        elif choice == "0":
            break
def main():
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Login")
        print("0. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = db.login()
            if user['type'] == "admin":
                admin_menu(user)
            elif user['type'] == "customer":
                customer_menu(user)
        else:
            db.close()
            print("Exiting the program...")
            break

