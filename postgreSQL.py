import psycopg2

class ConnectData:
    def __init__(self, dbname, user, password, host="localhost", port=5433):
        self.connection = psycopg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host,
            port = port
        )
        self.cursor = self.connection.cursor()

    #===================================================================================================================
    def login(self):
        print("\n--- LOGIN PAGE ----")
        name = input("Enter username: ")
        password = input("Enter password: ")
        self.cursor.execute("""SELECT user_id, name, user_type FROM users WHERE name= %s AND password = %s""", (name, password))
        user = self.cursor.fetchone()

        if user:
            user_id, name, user_type = user
            print(f"\nWelcome, {name}!")
            return {'id': user_id, 'name': name, 'type': user_type}
        else:
            print("User not found !")
            return None
    #===================================================================================================================
    # View Products For Admin and Customers
    def view_fruits(self):
        self.cursor.execute("""SELECT * FROM products WHERE category_id = 1;""")
        fruits = self.cursor.fetchall()
        print("\n--- FRUITS ---")
        for item in fruits:
            print(f"""
Product ID: {item[0]}
Category ID: {item[4]}
Product Name: {item[1]}
Price: ${item[2]} per kg
Quantity: {item[3]}
""")
    def view_vegetables(self):
        self.cursor.execute("""SELECT * FROM products WHERE category_id = 2;""")
        vegetables = self.cursor.fetchall()
        print("\n--- VEGETABLES ---")
        for item in vegetables:
            print(f"""
Product ID: {item[0]}
Category ID: {item[4]}
Product Name: {item[1]}
Price: {item[2]} per kg
Quantity: {item[3]}
""")
    def view_dairy(self):
        self.cursor.execute("""SELECT * FROM products WHERE category_id = 3;""")
        dairy = self.cursor.fetchall()
        print("\n--- DAIRY PRODUCTS ---")
        for item in dairy:
            print(f"""
Product ID: {item[0]}
Category ID: {item[4]}
Product Name: {item[1]}
Price: {item[2]} per pcs
Quantity: {item[3]}
""")
    def view_beverages(self):
        self.cursor.execute("""SELECT * FROM products WHERE category_id = 4;""")
        beverages = self.cursor.fetchall()
        print("\n--- BEVERAGES ---")
        for item in beverages:
            print(f"""
Product ID: {item[0]}
Category ID: {item[4]}
Product Name: {item[1]}
Price: {item[2]} per pcs
Quantity: {item[3]}
""")
    def view_snacks(self):

        self.cursor.execute("""SELECT * FROM products WHERE category_id = 5;""")
        snacks = self.cursor.fetchall()
        print("\n--- SNACKS AND CANDIES ---")
        for item in snacks:
            print(f"""
Product ID: {item[0]}
Category ID: {item[4]}
Product Name: {item[1]}
Price: {item[2]} per pcs
Quantity: {item[3]}
""")
    #===================================================================================================================
    def p_details(self, cat):
        p_name = input("Product Name: ")
        p_price = float(input("Price ($/kg or $/pcs): "))
        p_quantity = int(input("Quantity (in kg/pcs): "))
        self.cursor.execute("""INSERT INTO products (name, price, quantity, category_id) VALUES (%s, %s, %s, %s);""", (p_name, p_price, p_quantity, cat))
        self.connection.commit()
        print("Added")

    def add_product_admin(self):
        while True:
            print("""\n--- ADD PRODUCT SECTION ---
1. Fruits
2. Vegetables
3. Dairy Products
4. Beverages 
5. Snacks and Candies
0. Back to Admin menu
""")
            usr_input = int(input("Choose the type of product you want to add: "))
            if usr_input == 1:
                self.p_details(usr_input)
            elif usr_input == 2:
                self.p_details(usr_input)
            elif usr_input == 3:
                self.p_details(usr_input)
            elif usr_input == 4:
                self.p_details(usr_input)
            elif usr_input == 5:
                self.p_details(usr_input)
            else:
                break

    def view_products_admin(self):
        while True:
            self.view_fruits()
            self.view_vegetables()
            self.view_dairy()
            self.view_beverages()
            self.view_snacks()
            break

    def for_editing(self, cat_id, p_id):
        self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (cat_id, p_id,))
        product = self.cursor.fetchone()
        if not product:
            print("Product with this ID not found! Add the product first.")
            return
        print("""
1. Name
2. Price
3. Quantity
0. Back to Edit menu
""")
        choice = input("Choose what you want to edit: ")
        if choice == '1':
            new_name = input("Enter the new product name: ")
            self.cursor.execute("""UPDATE products SET name = %s WHERE category_id = %s AND product_id = %s;""", (new_name, cat_id, p_id))
            self.connection.commit()
            print("Updated!!!")
        elif choice == '2':
            new_price = float(input("Enter the new product price: "))
            self.cursor.execute("""UPDATE products SET price =%s WHERE category_id = %s AND product_id = %s;""", (new_price, cat_id, p_id))
            self.connection.commit()
            print("Updated!!!")
        elif choice == '3':
            new_quantity = int(input("Enter the new product quantity: "))
            self.cursor.execute("""UPDATE products SET quantity = %s WHERE category_id = %s AND product_id = %s;""", (new_quantity, cat_id, p_id))
            self.connection.commit()
            print("Updated!!!")
        else:
            return

    def edit_product_admin(self):
        while True:
            print("\n--- EDIT PRODUCT SECTION ---")
            print("""
1. Fruits
2. Vegetables
3. Dairy Products
4. Beverages
5. Snacks and Candies
0. Back to admin menu
""")
            usr_input = int(input("Choose the type of product you want to edit: "))
            if usr_input == 1:
                self.view_fruits()
                f_id = int(input("Enter the ID of the fruit you want to edit: "))
                self.for_editing(usr_input, f_id)
            elif usr_input == 2:
                self.view_vegetables()
                v_id = int(input("Enter the ID of the vegetable you want to edit: "))
                self.for_editing(usr_input, v_id)
            elif usr_input == 3:
                self.view_dairy()
                d_id = int(input("Enter the ID og the Dairy Product you want to edit: "))
                self.for_editing(usr_input, d_id)
            elif usr_input == 4:
                self.view_beverages()
                b_id = int(input("Enter the ID of the Beverage you want to edit: "))
                self.for_editing(usr_input, b_id)
            elif usr_input == 5:
                self.view_snacks()
                s_id = int(input("Enter the ID pf the Snack or Candy you want to edit: "))
                self.for_editing(usr_input, s_id)
            else:
                break

    def remove_product_admin(self):
        while True:
            print("\n--- REMOVE PRODUCT SECTION ---")
            print("""
1. Fruits
2. Vegetables
3. Dairy Products
4. Beverages
5. Snacks and Candies
0. Back to Admin menu
""")
            usr_input = int(input("Choose the type of product you want to remove: "))
            if usr_input == 1:
                self.view_fruits()
                f_id = int(input("Enter the ID of fruit you want to delete: "))
                self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (usr_input, f_id))
                product = self.cursor.fetchone()
                if not product:
                    print("Product with this ID not found.")
                    return
                self.cursor.execute("""DELETE FROM products WHERE category_id = %s AND product_id = %s""", (usr_input, f_id,))
                self.connection.commit()
                print(f"The product with the ID: {f_id} removed")

            elif usr_input == 2:
                self.view_vegetables()
                v_id = int(input("Enter the ID of vegetable you want to delete: "))
                self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (usr_input, v_id))
                product = self.cursor.fetchone()
                if not product:
                    print("Product with this ID not found.")
                    return
                self.cursor.execute("""DELETE FROM products WHERE category_id = %s AND product_id = %s""", (usr_input, v_id))
                self.connection.commit()

            elif usr_input == 3:
                self.view_dairy()
                d_id = int(input("Enter the ID of Dairy Product you want to delete: "))
                self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (usr_input, d_id))
                product = self.cursor.fetchone()
                if not product:
                    print("Product with this ID not found.")
                    return
                self.cursor.execute("""DELETE FROM products WHERE category_id = %s AND product_id = %s""", (usr_input, d_id))
                self.connection.commit()

            elif usr_input == 4:
                self.view_beverages()
                b_id = int(input("Enter the ID of Beverage you want to delete: "))
                self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (usr_input, b_id))
                product = self.cursor.fetchone()
                if not product:
                    print("Product with this ID not found.")
                    return
                self.cursor.execute("""DELETE FROM products WHERE category_id = %s AND product_id = %s""", (usr_input, b_id))
                self.connection.commit()

            elif usr_input == 5:
                self.view_snacks()
                s_id = int(input("Enter the ID of Snack or Candy you want to delete: "))
                self.cursor.execute("""SELECT product_id FROM products WHERE category_id = %s AND product_id = %s;""", (usr_input, s_id))
                product = self.cursor.fetchone()
                if not product:
                    print("Product with this ID not found.")
                    return
                self.cursor.execute("""DELETE FROM products WHERE category_id = %s AND product_id = %s""", (usr_input, s_id))
                self.connection.commit()
            else:
                break
    def view_shop_balance_admin(self):
        self.cursor.execute("""SELECT * FROM shops""")
        shops = self.cursor.fetchall()
        print("\n--- MARKETS BALANCE ---")
        for shop in shops:
            print(f"Shop ID: {shop[0]} | Name: {shop[1]}| Current Balance: {shop[2]}")

    def view_sold_items(self):
        print("\n--- SOLD ITEMS ---")
        query = """
        SELECT o.order_id, u.name AS customer_name, o.total_amount, p.name AS product_name, oi.quantity, p.price FROM orders o
        INNER JOIN users u ON o.user_id = u.user_id
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        INNER JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.order_id, u.name;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if not rows:
            print("No items have been sold yet.")
            return

        current_order = None
        for row in rows:
            order_id, customer_name, total_amount, product_name, quantity, price = row
            if order_id != current_order:
                if order_id is not None:
                    print()
                print(f"Customer: {customer_name} bought items worth: ${total_amount}")
                current_order = order_id
            print(f"    - {product_name} x {quantity} = {price * quantity}")
    #===================================================================================================================
    def add_to_basket(self, user_id, product_id, user_quantity):
        self.cursor.execute("""SELECT name, price, quantity FROM products WHERE product_id = %s;""", (product_id,))
        product = self.cursor.fetchone()
        if not product:
            print("No product found with this ID!")
            return
        name, price, available_quantity = product
        if user_quantity > available_quantity:
            print(f"Not enough in stock! Only {available_quantity} left")
            return

        self.cursor.execute("""SELECT basket_id FROM baskets WHERE user_id = %s;""", (user_id,))
        basket = self.cursor.fetchone()
        if not basket:
            print("Basket not found for this user!")
            return
        basket_id = basket[0]

        self.cursor.execute("SELECT quantity FROM basket_items WHERE basket_id =%s AND product_id =%s;", (basket_id, product_id))
        existing = self.cursor.fetchone()
        if existing:
            new_qty = existing[0] + user_quantity
            if new_qty > available_quantity:
                print(f"Not enough in stock! Only {available_quantity} left.")
                return
            self.cursor.execute("UPDATE basket_items SET quantity = %s WHERE basket_id = %s AND product_id = %s;", (new_qty, basket_id, product_id))
        else:
            self.cursor.execute("INSERT INTO basket_items (basket_id, product_id, quantity) VALUES (%s, %s, %s);", (basket_id, product_id, user_quantity))
        self.connection.commit()
        print(f"{user_quantity}kg/pcs x {name} added to basket.")

    def user_choices(self, n, user):
        p_id = int(input("Enter the ID of the product to add to basket (0 to go back): "))
        if p_id == 0:
            return
        self.cursor.execute("""SELECT * FROM products WHERE category_id =%s AND product_id =%s;""", (n, p_id))
        product = self.cursor.fetchone()
        if not product:
            print("No product found with this ID!")
            return
        product_id, name, price, available_quantity, category_id = product
        qty = int(input(f"Enter quantity to add to basket for {name}: "))
        if qty <= 0:
            print("Quantity must be positive.")
            return
        self.add_to_basket(user["id"], product_id, qty)

    def view_and_buy_products_user(self, user):

        while True:
            print("\n-- View Products Section --")
            print("""
1. Fruits 
2. Vegetables
3. Dairy Products
4. Beverages
5. Snacks and Candies
0. Back to Customer Menu
""")
            choice = int(input("Choose the type of product you want to buy: "))
            if choice == 1:
                self.view_fruits()
                self.user_choices(choice, user)
            elif choice == 2:
                self.view_vegetables()
                self.user_choices(choice, user)
            elif choice == 3:
                self.view_dairy()
                self.user_choices(choice, user)
            elif choice == 4:
                self.view_beverages()
                self.user_choices(choice, user)
            elif choice == 5:
                self.view_snacks()
                self.user_choices(choice, user)
            else:
                break

    def view_basket(self, user_id):
        self.cursor.execute("""SELECT basket_id FROM baskets WHERE user_id = %s;""", (user_id,))
        basket = self.cursor.fetchone()
        basket_id = basket[0]
        query = """
        SELECT bi.item_id, p.product_id, p.name, bi.quantity, p.price FROM basket_items bi
        INNER JOIN products p ON bi.product_id = p.product_id 
        WHERE bi.basket_id = %s;
        """

        self.cursor.execute(query, (basket_id,))
        items = self.cursor.fetchall()
        if not items:
            print("Your basket is empty.")
            return
        print("\n--- YOUR BASKET ---")
        for item_id, p_id, p_name, p_quantity, p_price in items:
            print(f"""\nItems -> Item ID: {item_id}, Product ID: {p_id}.
    {p_name} - {p_quantity}pcs/kgs x ${p_price}""")

    def edit_basket(self, user_id):
        self.view_basket(user_id)
        edit_choice = int(input("Enter the item ID of the product you want to edit: (0 to go back) "))
        if edit_choice == 0:
            return

        self.cursor.execute("""SELECT basket_id FROM baskets WHERE user_id = %s;""", (user_id,))
        basket = self.cursor.fetchone()
        if not basket:
            print("Basket not found for this user.")
            return
        basket_id = basket[0]

        self.cursor.execute("SELECT item_id, product_id, quantity FROM basket_items WHERE item_id = %s AND basket_id = %s;", (edit_choice, basket_id))
        basket_item = self.cursor.fetchone()
        if not basket_item:
            print("Item not found in your basket.")
            return
        item_id, product_id, old_qty = basket_item

        self.cursor.execute("SELECT product_id, name, price, quantity FROM products WHERE product_id = %s;", (product_id,))
        product = self.cursor.fetchone()
        if not product:
            print("Product not found!")
            return
        p_id, name, price, available_qty = product
        print(f"Current quantity in basket: {old_qty}")
        new_qty = int(input(f"Enter new quantity for {name} (available at the store: {available_qty}): "))
        if new_qty > available_qty:
            print(f"Not enough in stock! Only {available_qty} left")
            return

        if new_qty <= 0:
            self.cursor.execute("DELETE FROM basket_items WHERE item_id = %s;",(item_id,))
            print(f"{name} removed from basket.")
        else:
            self.cursor.execute("UPDATE basket_items SET quantity = %s WHERE item_id = %s;",(new_qty, item_id))
            print(f"Quantity for {name} updated to {new_qty}.")
        self.connection.commit()

    def proceed_to_payment(self, user):
        user_id = user['id']
        self.cursor.execute("SELECT basket_id FROM baskets WHERE user_id = %s ORDER BY created_at DESC LIMIT 1;", (user_id,))
        basket = self.cursor.fetchone()
        if not basket:
            print("Your basket is empty!")
            return
        basket_id = basket[0]
        query = """
        SELECT p.product_id, p.name, bi.quantity, p.price FROM basket_items bi
        INNER JOIN products p ON bi.product_id = p.product_id
        WHERE bi.basket_id = %s;
        
        """
        self.cursor.execute(query, (basket_id,))
        items = self.cursor.fetchall()
        if not items:
            print("Your basket is empty!")
            return
        total = sum(qty * price for _, _, qty, price in items)
        print(f"Total amount to pay: ${total}")
        self.cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
        balance = self.cursor.fetchone()
        balance = balance[0]
        if balance < total:
            print(f"Not enough balance to complete the purchase.")
            return
        confirm = input("Confirm the payment? (y/n): ").lower()
        if confirm != "y":
            print("Payment cancelled.")
            return
        new_balance = balance - total
        self.cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s;", (new_balance, user_id))

        self.cursor.execute("INSERT INTO orders (user_id, total_amount, created_at) VALUES (%s, %s, NOW()) RETURNING order_id;", (user_id, total))
        orders = self.cursor.fetchone()
        order_id = orders[0]
        for product_id, name, qty, price in items:
            self.cursor.execute("UPDATE products SET quantity = quantity - %s WHERE product_id = %s;", (qty, product_id))
            self.cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s);", (order_id, product_id, qty, price))

        self.cursor.execute("UPDATE shops SET balance = balance + %s WHERE shop_id = 1;", (total,))
        self.cursor.execute("DELETE FROM basket_items WHERE basket_id = %s;", (basket_id,))
        self.connection.commit()
        print(f"Payment successful! Your new balance: ${new_balance}.")

    #===================================================================================================================
    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")
    #===================================================================================================================

    def edit_info_users(self, user):
        while True:
            print(f"\n--- Edit Info for {user['name']} ---")
            print("1. Edit Name")
            print("2. Edit Phone Number")
            print("3. Edit password")
            print("0. Go back")
            choice = input("Your choice: ")
            user_id = user['id']
            if choice == '1':
                new_name = input("Your updated name: ")
                self.cursor.execute("UPDATE users SET name = %s WHERE user_id = %s;", (new_name, user_id))
                self.connection.commit()
                print("Your name id updated")
            elif choice == '2':
                new_phone = input("Your updated phone number: ")
                self.cursor.execute("UPDATE users SET phone = %s WHERE user_id = %s;", (new_phone, user_id))
                self.connection.commit()
                print("Your phone number is updated")
            elif choice == '3':
                old_password = input("Enter your old password: ")
                self.cursor.execute("SELECT password FROM users WHERE user_id = %s;", (user_id,))
                old_pass = self.cursor.fetchone()[0]
                if old_pass != old_password:
                    print("Your old password does not match")
                    return
                else:
                    new_password = input("Enter new password: ")
                    new_pass_auth = input("Enter new password again to confirm: ")
                    if new_password == new_pass_auth:
                        self.cursor.execute("UPDATE users SET password = %s WHERE user_id = %s;", (new_password, user_id))
                        self.connection.commit()
                        print("Your password updated")
                    else:
                        print("Passwords do not match.")
                        return
            else:
                break

