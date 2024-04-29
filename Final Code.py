import csv
import re
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog

# Function to add stock to an item
def add_stock():
    selected_item = tree.focus()
    if selected_item:
        item_values = tree.item(selected_item)['values']
        name = item_values[0]
        stock = item_values[2]

        # Prompt the user to enter the quantity of stock to add
        quantity = simpledialog.askinteger("Add Stock", f"Enter the quantity of stock to add for {name}:")
        if quantity is not None and quantity > 0:
            new_stock = int(stock) + quantity

            # Update the stock in the inventory file
            update_stock(name, new_stock)

            # Update the stock in the treeview
            tree.set(selected_item, column="stock", value=new_stock)
            messagebox.showinfo("Stock Update", f"Stock for {name} updated. New stock: {new_stock}")
        else:
            messagebox.showerror("Error", "Invalid quantity entered.")

# Function to update the stock in the inventory file
def update_stock(name, new_stock):
    with open('medication.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open('medication.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0] == name:
                row[2] = str(new_stock)
            writer.writerow(row)

# Function to add an order to the cart
def add_to_cart():
    name = name_entry.get()
    quantity = quantity_entry.get()

    # Check if the name field is empty
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return

    # Check if the quantity field is empty or not a valid number
    if not quantity or not quantity.isdigit():
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return

    # Retrieve the pricing for the ordered item
    price = get_item_price(name)

    # Check if the item exists in the inventory
    if price is None:
        messagebox.showerror("Error", "Item not found in inventory.")
        return

    # Calculate the total price based on quantity
    total_price = float(price) * int(quantity)

    # Add the item and quantity to the cart
    cart.append({"name": name, "price": price, "quantity": quantity, "total_price": total_price})

    # Clear the entry fields
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

    # Show the success message
    messagebox.showinfo("Success", f"Item '{name}' added to the cart. Quantity: {quantity}")


# Function to get the price of an item
def get_item_price(name):
    with open('medication.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == name:
                # Extract the numeric part of the price and remove any non-numeric characters
                price = re.sub(r'[^\d.]+', '', row[1])
                return price
        return None


# Function to display the cart
def display_cart():
    global cart_tree
    if not cart:
        messagebox.showinfo("Cart", "Cart is empty.")
        return

    cart_items = []
    total_price = 0

    for item in cart:
        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_item_price = item["total_price"]

        cart_items.append(f"Item: {name}\tPrice: {price}\tQuantity: {quantity}\tTotal Price: {total_item_price}")
        total_price += total_item_price

    cart_text = "\n".join(cart_items)
    cart_text += f"\n\nTotal Price: {total_price}"

    messagebox.showinfo("Cart", cart_text)

    # Create the cart window
    cart_window = tk.Toplevel()
    cart_window.title("Cart")

    # Create a treeview to display the cart
    cart_tree = ttk.Treeview(cart_window, columns=("name", "price", "quantity", "total_price"), show="headings")
    cart_tree.heading("name", text="Name")
    cart_tree.heading("price", text="Price")
    cart_tree.heading("quantity", text="Quantity")
    cart_tree.heading("total_price", text="Total Price")
    cart_tree.pack(padx=10, pady=10)

    # Populate the treeview with cart items
    for item in cart:
        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_price = item["total_price"]
        cart_tree.insert("", tk.END, values=(name, price, quantity, total_price))

    # Bind the select_cart_item function to the Treeview selection event
    cart_tree.bind("<<TreeviewSelect>>", select_cart_item)

    # Create the update and remove buttons
    update_button = ttk.Button(cart_window, text="Update", command=update_cart)
    update_button.pack(pady=5)
    remove_button = ttk.Button(cart_window, text="Remove", command=remove_cart_item)
    remove_button.pack(pady=5)


# Function to select an item from the cart
def select_cart_item(event):
    selection = cart_tree.selection()
    if selection:
        selected_item = cart_tree.item(selection[0])
        name = selected_item['values'][0]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)


# Function to update the cart
def update_cart():
    selection = cart_tree.selection()
    if selection:
        selected_item = cart_tree.item(selection[0])
        name = selected_item['values'][0]
        quantity = quantity_entry.get()

        # Check if the quantity field is empty or not a valid number
        if not quantity or not quantity.isdigit():
            messagebox.showerror("Error", "Please enter a valid quantity.")
            return

        # Update the quantity and total price of the selected item in the cart
        for item in cart:
            if item["name"] == name:
                item["quantity"] = quantity
                item["total_price"] = float(item["price"]) * int(quantity)
                break

        # Update the cart treeview with the modified item
        cart_tree.set(selection[0], column="quantity", value=quantity)
        cart_tree.set(selection[0], column="total_price", value=item["total_price"])

        # Clear the entry field
        quantity_entry.delete(0, tk.END)

        messagebox.showinfo("Update", f"Item '{name}' updated in the cart.")


# Function to remove an item from the cart
def remove_cart_item():
    selection = cart_tree.selection()
    if selection:
        selected_item = cart_tree.item(selection[0])
        name = selected_item['values'][0]

        # Find the index of the item in the cart
        index = None
        for i, item in enumerate(cart):
            if item["name"] == name:
                index = i
                break

        # Remove the item from the cart and update the cart treeview
        if index is not None:
            cart_tree.delete(selection)
            remove_from_cart(index)


# Function to remove an item from the cart
def remove_from_cart(index):
    name = cart[index]["name"]

    # Remove the item from the cart
    cart.pop(index)

    # Show the success message
    messagebox.showinfo("Success", f"Item '{name}' removed from the cart.")


# Function to display the cart
def display_cart():
    global cart_tree
    if not cart:
        messagebox.showinfo("Cart", "Cart is empty.")
        return

    cart_items = []
    total_price = 0

    for item in cart:
        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_item_price = item["total_price"]

        cart_items.append(f"Item: {name}\tPrice: {price}\tQuantity: {quantity}\tTotal Price: {total_item_price}")
        total_price += total_item_price

    cart_text = "\n".join(cart_items)
    cart_text += f"\n\nTotal Price: {total_price}"

    messagebox.showinfo("Cart", cart_text)

    # Create the cart window
    cart_window = tk.Toplevel()
    cart_window.title("Cart")

    # Create a treeview to display the cart
    cart_tree = ttk.Treeview(cart_window, columns=("name", "price", "quantity", "total_price"), show="headings")
    cart_tree.heading("name", text="Name")
    cart_tree.heading("price", text="Price")
    cart_tree.heading("quantity", text="Quantity")
    cart_tree.heading("total_price", text="Total Price")
    cart_tree.pack(padx=10, pady=10)

    # Populate the treeview with cart items
    for item in cart:
        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_price = item["total_price"]
        cart_tree.insert("", tk.END, values=(name, price, quantity, total_price))

    # Bind the select_cart_item function to the Treeview selection event
    cart_tree.bind("<<TreeviewSelect>>", select_cart_item)

    # Create the update and remove buttons
    update_button = ttk.Button(cart_window, text="Update", command=update_cart)
    update_button.pack(pady=5)
    remove_button = ttk.Button(cart_window, text="Remove", command=remove_cart_item)
    remove_button.pack(pady=5)


# Function to purchase items
def purchase_items():
    # Check if the cart is empty
    if not cart:
        messagebox.showerror("Error", "Cart is empty.")
        return

    # Calculate the total cost of the items in the cart
    total_cost = sum(item["total_price"] for item in cart)

    # Show the purchase confirmation message with the total cost
    messagebox.showinfo("Purchase Confirmation", f"Total cost: {total_cost}")

    # Clear the cart
    cart.clear()


# Function to cancel the cart
def cancel_cart():
    # Clear the cart
    cart.clear()

    # Show the cancellation confirmation message
    messagebox.showinfo("Cancellation", "Cart has been cancelled.")


# Function to go back to the cart from the ordering display
def back_to_cart():
    ordering_window.destroy()


# Function to select an item from the ordering list
def select_order_item(event):
    selection = tree.selection()
    if selection:
        selected_item = tree.item(selection[0])
        name = selected_item['values'][0]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)


# Function to display the ordering display in a separate window
def display_ordering():
    # Create a new window for the ordering display
    ordering_window = tk.Toplevel(window)
    ordering_window.title("Ordering Display")

    # Create a frame to hold the ordering display
    ordering_frame = tk.Frame(ordering_window)
    ordering_frame.pack()

    # Create a label for the ordering display
    ordering_label = tk.Label(ordering_frame, text="Ordering Display", font=("Arial", 14, "bold"))
    ordering_label.pack()

    # Create a treeview to display the items in the order
    order_tree = ttk.Treeview(ordering_frame, columns=("name", "price", "quantity", "total_price"), show="headings")
    order_tree.heading("name", text="Name")
    order_tree.heading("price", text="Price")
    order_tree.heading("quantity", text="Quantity")
    order_tree.heading("total_price", text="Total Price")
    order_tree.pack()

    # Create a scrollbar for the order tree
    order_scrollbar = ttk.Scrollbar(ordering_frame, orient="vertical", command=order_tree.yview)
    order_scrollbar.pack(side="right", fill="y")
    order_tree.configure(yscrollcommand=order_scrollbar.set)

    # Populate the order tree with the items in the cart
    for item in cart:
        name = item["name"]
        price = item["price"]
        quantity = item["quantity"]
        total_price = item["total_price"]

        order_tree.insert("", tk.END, values=(name, price, quantity, total_price))

    # Create a Back button to go back to the cart
    back_button = tk.Button(ordering_frame, text="Back", command=back_to_cart)
    back_button.pack()


# Function to switch to customer mode
def switch_to_customer():
    admin_button.config(state=tk.NORMAL)
    customer_button.config(state=tk.DISABLED)
    order_button.config(state=tk.NORMAL)
    add_stock_button.config(state=tk.DISABLED)
    input_frame.grid()


    # Clear the treeview
    tree.delete(*tree.get_children())

    # Load orders from the "ordering.csv" file
    with open('ordering.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name, price = row
            tree.insert("", tk.END, values=(name, price))

    # Bind the select_order_item function to the Treeview selection event
    tree.bind("<<TreeviewSelect>>", select_order_item)


# Function to switch to admin mode
# Define the correct password
correct_password = "password123"


def switch_to_admin():
    # Create a password input dialog
    password = tk.simpledialog.askstring("Admin Mode", "Enter the password:", show="*")

    # Check if the entered password matches the correct password
    if password == correct_password:
        # Password is correct, proceed to switch to admin mode
        admin_button.config(state=tk.DISABLED)
        customer_button.config(state=tk.NORMAL)
        order_button.config(state=tk.DISABLED)
        add_stock_button.config(state=tk.NORMAL)
        input_frame.grid_remove()
        tree.delete(*tree.get_children())  # Clear the treeview
        load_inventory_with_stock()  # Load inventory data with stock column
        window.title("Inventory Management System")

    else:
        # Password is incorrect, show an error message
        messagebox.showerror("Error", "Incorrect password. Access denied.")


# Function to load inventory data with stock column
def load_inventory_with_stock():
    with open('medication.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                name = row[0]
                price = row[1]
                stock = row[2]
                tree.insert("", tk.END, values=(name, price, stock))
            else:
                print(f"Invalid row: {row}")


# Function to purchase items
def purchase_items():
    # Check if the cart is empty
    if not cart:
        messagebox.showerror("Error", "Cart is empty.")
        return

    # Calculate the total cost of the items in the cart
    total_cost = sum(item["total_price"] for item in cart)

    # Show the purchase confirmation message with the total cost
    messagebox.showinfo("Purchase Confirmation", f"Total cost: {total_cost}")

    # Update the inventory and deduct the stock
    for item in cart:
        name = item["name"]
        quantity = int(item["quantity"])

        # Update the inventory file
        update_inventory(name, quantity)

    # Clear the cart
    cart.clear()


# Function to update the inventory and deduct the stock
def update_inventory(name, quantity):
    with open('medication.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open('medication.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0] == name:
                stock = int(row[2])
                if stock >= quantity:
                    stock -= quantity
                    row[2] = str(stock)
                else:
                    messagebox.showerror("Error", f"Insufficient stock for item '{name}'.")
            writer.writerow(row)

# Create the main window
window = tk.Tk()
window.title("Ordering and Inventory System")

# Create a frame to hold the entry fields and buttons for orders
input_frame = tk.Frame(window)

# Create entry fields for order details
name_label = tk.Label(input_frame, text="Name:")
name_label.grid(row=0, column=0, sticky="E")
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1)

quantity_label = tk.Label(input_frame, text="Quantity:")
quantity_label.grid(row=1, column=0, sticky="E")
quantity_entry = tk.Entry(input_frame)
quantity_entry.grid(row=1, column=1)

# Create an "Add to Cart" button
order_button = tk.Button(input_frame, text="Add to Cart", command=add_to_cart)
order_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a frame to hold the password entry and admin/customer buttons
admin_frame = tk.Frame(window)

# Create an "Admin Mode" button
admin_button = tk.Button(admin_frame, text="Admin Mode", command=switch_to_admin)

# Create a "Customer Mode" button
customer_button = tk.Button(admin_frame, text="Customer Mode", command=switch_to_customer, state=tk.DISABLED)

# Create a treeview to display the orders
tree = ttk.Treeview(window, columns=("name", "price", "stock"), show="headings")
tree.heading("name", text="Name")
tree.heading("price", text="Price")
tree.heading("stock", text="Stock")

# Create a Cart button
cart_button = tk.Button(input_frame, text="Cart", command=display_cart)

# Create a Purchase button
purchase_button = tk.Button(input_frame, text="Purchase", command=purchase_items)

# Create a Cancel button
cancel_button = tk.Button(input_frame, text="Cancel", command=cancel_cart)

# Create a new window for ordering display
ordering_window = None

# Create the Add Stock button
add_stock_button = ttk.Button(admin_frame, text="Add Stock", command=add_stock)
add_stock_button.grid(row=3, column=3, pady=10)

# Grid configuration for widgets
input_frame.grid()
order_button.grid(row=1, column=2, columnspan=2, pady=10, padx=10)
admin_frame.grid(row=0, column=1, columnspan=2, pady=10)
admin_button.grid(row=0, column=3, padx=10)
customer_button.grid(row=1, column=3, padx=10)
tree.grid(row=3, column=0, columnspan=2)
add_stock_button.grid(row=3, column=5, pady=10)
cart_button.grid(row=2, column=0, pady=10)
purchase_button.grid(row=2, column=1, pady=10)
cancel_button.grid(row=2, column=2, pady=10)

# Switch to customer mode by default
switch_to_customer()

# Create an empty cart list to hold the added items
cart = []

# Load inventory data with stock column
load_inventory_with_stock()

# Start the Tkinter event loop
window.mainloop()
