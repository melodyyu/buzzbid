# gui/login_window.py
import customtkinter as ctk
import tkinter as tk
import re
from tkinter import messagebox, ttk, simpledialog,Toplevel, Scrollbar, Canvas, Frame, font
from PIL import Image
from services.authentication_service import AuthenticationService
from services.generate_report_service import GenerateReportService
from services.item_handler_service import ItemHandlerService
from datetime import datetime
from functools import reduce



class LoginWindow(ctk.CTk) :
    def __init__(self):
        super().__init__()
        self.title("BuzzBid Login")
        self.geometry("800x600+200+200")
        self.logo_photo = None
        
        # Update background color to match logo's background
        bg_color = "#ffffff"  # Light gray that matches the logo background
        self.configure(bg=bg_color)

        # Create a frame for the logo with matching background
        self.logo_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.logo_frame.pack(pady=(50, 0))

        # Load and display the logo
        logo_path = "media/buzzbid_logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((200, 200))
        self.logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(200, 200))
        self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.logo_photo, text="")
        self.logo_label.pack()

        # Input frame with matching background
        self.input_frame = ctk.CTkFrame(self, fg_color=bg_color, border_width=0,border_color=bg_color)
        self.input_frame.pack(pady=(20, 100), padx=150, fill='both', expand=True)

        # Username Entry
        self.username_label = ctk.CTkLabel(self.input_frame, text="Username:")
        self.username_label.grid(row=0, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        self.username_entry = ctk.CTkEntry(self.input_frame)
        self.username_entry.grid(row=0, column=1, pady=(20, 10), padx=(10, 10), sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1)

        # Password Entry
        self.password_label = ctk.CTkLabel(self.input_frame, text="Password:")
        self.password_label.grid(row=1, column=0, pady=10, padx=(10, 10), sticky="w")

        self.password_entry = ctk.CTkEntry(self.input_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=(10, 10), sticky="ew")

        # Buttons
        self.login_button = ctk.CTkButton(self.input_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=(20, 10), padx=(10, 10), columnspan=2)

        self.register_button = ctk.CTkButton(self.input_frame, text="Register", command=self.register)

        self.register_button.grid(row=3, column=0, pady=(10, 20), padx=(10, 10), columnspan=2)

        # Set focus to the username entry initially
        self.username_entry.focus_force()

    def login(self):
        # print('login function')
        username = self.username_entry.get()
        password = self.password_entry.get()
        # AuthenticationService would handle the verification
        if AuthenticationService.login(username, password):
            messagebox.showinfo("Login Success", "You are now logged in.")
            current_user = AuthenticationService.get_user_details(username)
            self.destroy()
            main_menu = MainMenuWindow(current_user)
            main_menu.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    def register(self):
        self.destroy()
        registration_window = RegistrationWindow()
        registration_window.mainloop()


class MainMenuWindow(ctk.CTk):
    def __init__(self, current_user):
        super().__init__()
        self.title("Buzzbid Main Menu")
        self.geometry("800x600+200+200")
        self.configure(bg="#D3D3D3")  # Light grey

        # Check if the current user is an admin
        if current_user['user_type'] == "Admin":
            # Welcome message for admin users
            welcome_message = f"Welcome, {current_user['first_name']} {current_user['last_name']}! \nAdministrative position: {current_user['position']}"
            self.show_report_section = True
        else:
            # Welcome message for non-admin users
            welcome_message = f"Welcome, {current_user['first_name']} {current_user['last_name']}!\n"
            self.show_report_section = False

        # Display the welcome message
        self.welcome_label = ctk.CTkLabel(self, text=welcome_message)
        self.welcome_label.pack(pady=20)

        # Current user
        self.current_user = current_user

        # Frame for the menu options
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(pady=20, fill='both', expand=True)

        # Auction Option Title
        self.auction_option_label = ctk.CTkLabel(self.options_frame, text="Auction Options", font=('Helvetica', 18, 'bold'))
        self.auction_option_label.grid(row=0, column=0, padx=100, pady=(10, 3), sticky="w")

        # Report Title (only displayed for admin users)
        if self.show_report_section:
            self.report_label = ctk.CTkLabel(self.options_frame, text="Reports", font=('Helvetica', 18, 'bold'))
            self.report_label.grid(row=0, column=1, padx=100, pady=(10, 3), sticky="w")
        else:
            # Hide the Report Title for non-admin users
            self.report_label = ctk.CTkLabel(self.options_frame, text="", font=('Helvetica', 18, 'bold'))
            self.report_label.grid(row=0, column=1, padx=100, pady=(10, 3), sticky="w")
            self.report_label.grid_remove()

        # Auction Option Buttons with corrected command references and centered positioning
        self.search_for_items_button = ctk.CTkButton(self.options_frame, text="Search for Items", command=self.search_for_items)
        self.search_for_items_button.grid(row=1, column=0, padx=100, pady=10, sticky="w")

        self.list_item_button = ctk.CTkButton(self.options_frame, text="List Item", command=self.list_item)
        self.list_item_button.grid(row=2, column=0, padx=100, pady=10, sticky="w")

        self.view_auction_results_button = ctk.CTkButton(self.options_frame, text="View Auction Results", command=self.view_auction_results)
        self.view_auction_results_button.grid(row=3, column=0, padx=100, pady=10, sticky="w")

        #Logout button
        self.logout_button = ctk.CTkButton(self.options_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=8, column=0, padx=100, pady=100, sticky="w")

        # Conditionally display Report Buttons only for admin users
        if self.show_report_section:
            self.category_report_button = ctk.CTkButton(self.options_frame, text="Category Report", command=self.category_report)
            self.category_report_button.grid(row=1, column=1, padx=100, pady=10, sticky="w")

            self.user_report_button = ctk.CTkButton(self.options_frame, text="User Report", command=self.user_report)
            self.user_report_button.grid(row=2, column=1, padx=100, pady=10, sticky="w")

            self.top_rated_items_button = ctk.CTkButton(self.options_frame, text="Top Rated Items", command=self.top_rated_items)
            self.top_rated_items_button.grid(row=3, column=1, padx=100, pady=10, sticky="w")

            self.auction_statistics_button = ctk.CTkButton(self.options_frame, text="Auction Statistics", command=self.auction_statistics)
            self.auction_statistics_button.grid(row=4, column=1, padx=100, pady=10, sticky="w")

            self.cancelled_auction_details_button = ctk.CTkButton(self.options_frame, text="Cancelled Auction Details", command=self.cancelled_auction_details)
            self.cancelled_auction_details_button.grid(row=5, column=1, padx=100, pady=10, sticky="w")

    def search_for_items(self):
        # print("Navigate to search_for_items")
        search_window = SearchWindow(self.current_user)
        self.withdraw()
        search_window.mainloop()
        self.deiconify()


    def list_item(self):
        list_item = ListItemWindow(self.current_user)

    def view_auction_results(self):
        # print("Navigate to Auction Results")
        self.destroy()
        auction_results = AuctionResultsWindow(self.current_user)
        auction_results.mainloop()

    def category_report(self):
        category_report = CategoryReportWindow(self.current_user)

    def user_report(self):
        user_report = UserReportsWindow(self.current_user)

    def top_rated_items(self):
       # print("Navigate top_rated_items report")
       if self.current_user['user_type'] != "Admin":
           messagebox.showerror("Click Failed", "Only Admin can see the report.")
       else:
           top_rate_items_view = TopRatedItems(self.current_user)

        # Only for test rate item window, comments above before you use this entrance
        # test_rate_item_view = RateItemWindow(self.current_user,1)
        # test_rate_item_view.mainloop()

    def auction_statistics(self):
        # print("Navigate auction_statistics report")
        if self.current_user['user_type'] != "Admin":
            messagebox.showerror("Click Failed", "Only Admin can see the report.")
        else:
            auction_statistics = AuctionStatsWindow(self.current_user)

    def cancelled_auction_details(self):
        cancelled_auction_details_window = CancelledAuctionDetailsWindow(self.current_user)

    def logout(self):
        self.logo_photo = None
        self.destroy()
        login_window = LoginWindow()
        login_window.mainloop()


class CategoryReportWindow(ctk.CTkToplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("Category Reports")
        self.geometry("1200x600+600+400")
        self.configure(bg="#D3D3D3")
        self.focus_force()

        self.current_user = current_user

        # Frame for the category report
        self.category_report_frame = ttk.Frame(self)
        self.category_report_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()
          
        #Button to close
        self.return_button = ctk.CTkButton(self.category_report_frame, text="Return", command=self.close)
        self.return_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def report_content(self):
        categories = GenerateReportService.category_report()

        columns = ["Category", "Total Items", "Min Price", "Max Price", "Average Price"]
        self.tree = ttk.Treeview(self.category_report_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        
        if categories != None:
            for i in range(len(categories["Category"])):
                self.tree.insert("", "end", values=(categories["Category"][i], categories["Total Items"][i], categories["Min Price"][i], categories["Max Price"][i], categories["Average Price"][i]))
        self.tree.pack(fill=tk.BOTH, expand=True)

    def close(self):
        self.destroy()


class RegistrationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Buzzbid New User Registration")
        self.geometry("800x600+200+200")
        self.configure(bg="#D3D3D3")


        # First Name Entry
        self.firstname_label = ctk.CTkLabel(self, text="First Name:")
        self.firstname_label.pack(pady=(10, 0))
        self.firstname_entry = ctk.CTkEntry(self)
        self.firstname_entry.pack(pady=(0, 10))

        # Last Name Entry
        self.lastname_label = ctk.CTkLabel(self, text="Last Name:")
        self.lastname_label.pack(pady=(10, 0))
        self.lastname_entry = ctk.CTkEntry(self)
        self.lastname_entry.pack(pady=(0, 10))


        # Username Entry
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=(0, 10))

        # Password Entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=(0, 10))

        # Confirm Password Entry
        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:")
        self.confirm_password_label.pack(pady=(10, 0))
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.pack(pady=(0, 10))

        # Register Button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.pack(pady=20)

        # Cancel Registration Button
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_registration)
        self.cancel_button.pack(pady=20)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        first_name = self.firstname_entry.get()
        last_name = self.lastname_entry.get()

        # Validate fields
        if not username or not password or not confirm_password or not first_name or not last_name:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Check if username already exists in the database
        if self.username_exists(username):
            messagebox.showerror("Error", "Username already registered.")
            return

        # If validation passes, insert new user into the database
        self.register_new_user(username, password,first_name,last_name)
        messagebox.showinfo("Success", "Registration successful.")
        self.destroy()  # Close the registration window

        # Open the login window again
        login_window = LoginWindow()
        login_window.mainloop()


    def username_exists(self, username):
        username_exists_in_system = AuthenticationService.check_existing_user(username)
        return username_exists_in_system

    def register_new_user(self, username, password,first_name, last_name):
        add_user =  AuthenticationService.add_new_user( username, password,first_name, last_name)
        return add_user

    def cancel_registration(self):
        self.destroy()  # Close the registration window

        # Open the login window again
        login_window = LoginWindow()
        login_window.mainloop()


class SearchWindow(ctk.CTk):
    #Window details
    def __init__(self, current_user):
        super().__init__()
        self.title("Item Search")
        self.geometry("800x600+200+200")
        self.configure(bg="#D3D3D3")

        self.current_user = current_user

        # Attributes to store user input
        self.user_input_keyword = ""
        self.user_input_category = ""
        self.user_input_min_price = ""
        self.user_input_max_price = ""
        self.user_input_condition = ""

        #Frame for the report
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        #Keyword label and input box
        self.keyword_label = ctk.CTkLabel(self.input_frame, text="Keyword (case sensitive)")
        self.keyword_label.grid(row=0, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        self.keyword_entry = ctk.CTkEntry(self.input_frame)
        self.keyword_entry.grid(row=0, column=1, pady=(20, 10), padx=(10, 10), sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1)

        #Category drop down menu; Is populated Category table in database
        self.category_label = ctk.CTkLabel(self.input_frame, text="Category")
        self.category_label.grid(row=1, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        categories = self.populate_categories() #Populate drop down with entries in Category table

        self.category_dropmenu = ctk.CTkOptionMenu(self.input_frame, values=categories, fg_color="#FFFFFF", text_color="#000000", button_color="#3a7ebf", button_hover_color="#2c679e")
        self.category_dropmenu.grid(row=1, column=1, pady=(20, 10), padx=(10, 10), sticky="w")
        self.category_dropmenu.set("") #Set appearance to blank row

        #restrict input to digits only
        # vcmd = (self.register(self.restrict_numbers), '%P') #'%P' is the new value of entry after edit for validatecommand 

        #Minimum price input
        self.min_price_label = ctk.CTkLabel(self.input_frame, text="Minimum Price $")
        self.min_price_label.grid(row=2, column=0, pady=(20, 10), padx=(10, 10), sticky="w")
        
        self.min_price_entry = ctk.CTkEntry(self.input_frame, validate='key')
        self.min_price_entry.grid(row=2, column=1, pady=(20, 10), padx=(10, 10), sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1)

        #Maximum price input
        self.max_price_label = ctk.CTkLabel(self.input_frame, text="Maximum Price $", )
        self.max_price_label.grid(row=3, column=0, pady=(20, 10), padx=(10, 10), sticky="w")
        
        self.max_price_entry = ctk.CTkEntry(self.input_frame, validate='key')
        self.max_price_entry.grid(row=3, column=1, pady=(20, 10), padx=(10, 10), sticky="ew")

        self.input_frame.grid_columnconfigure(1, weight=1)


        #Condition drop down
        self.condition_label = ctk.CTkLabel(self.input_frame, text="Condition at least ")
        self.condition_label.grid(row=4, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        conditions = ["", 'New', 'Very Good', 'Good', 'Fair', 'Poor']

        self.condition_dropmenu = ctk.CTkOptionMenu(self.input_frame, values=conditions, fg_color="#FFFFFF", text_color="#000000", button_color="#3a7ebf", button_hover_color="#2c679e")
        self.condition_dropmenu.grid(row=4, column=1, pady=(20, 10), padx=(10, 10), sticky="w")
        self.condition_dropmenu.set("") #Set appearance to blank row


        #Cancel button. On click returns user to main menu.
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.return_to_main_menu)
        # self.cancel_button.grid(row=99,column=99, pady=(20, 10), padx=(10, 10), sticky="w")
        self.cancel_button.pack(side='left', padx=20, pady=20)

        #Search button. On click, sends user to Search Result screen. First, validates entered information.
        self.search_button = ctk.CTkButton(self, text="Search", command=self.validate_click)
        self.search_button.pack(side='right', padx=20, pady=20) #adjust placement with grid

    #Fetch category data to populate category drop down menu
    def populate_categories(self):
        fetched_categories = ItemHandlerService.fetch_categories() #returns list of tuples
        # print("CATEGORIES:", fetched_categories)
        
        categories = []
        categories.append("") #add in blank row for default appearance

        for item in fetched_categories:
            category = item[0] #access first element of each tuple
            categories.append(category)

        
        return categories 

    #When user clicks Search, input numbers are compared. If input is invalid, display error message.
    def validate_click(self):
        #If min/max price contains anything other than numbers or a decimal
        pattern = r'[^0-9.]'
        min_price = self.min_price_entry.get()
        if re.search(pattern, min_price):
            messagebox.showerror ("Error", "Minimum price cannot contain letters or special characters")
            return

        max_price = self.max_price_entry.get()
        if re.search(pattern, max_price):
            messagebox.showerror ("Error", "Maximum price cannot contain letters or special characters")
            return
        
        #Throw error message if min_price entry is greater than max_price entry
        if (min_price > max_price) and max_price != "":
            messagebox.showerror ("Error", "Maximum price must be greater than the minimum price.")
        else: 
            # Save user input to attributes
            self.user_input_keyword = self.keyword_entry.get()
            self.user_input_category = self.category_dropmenu.get()
            self.user_input_min_price = self.min_price_entry.get()
            self.user_input_max_price = self.max_price_entry.get()
            self.user_input_condition = self.condition_dropmenu.get()

            self.show_search_results()
    
    #Functionality for Cancel button
    def return_to_main_menu(self):
        self.destroy()
        main_menu_window = MainMenuWindow(self.current_user)
        main_menu_window.mainloop()

    #Functionality for Search button
    def show_search_results(self):

        #Save user input 
        user_input_keyword = self.keyword_entry.get()
        user_input_category = self.category_dropmenu.get()
        user_input_min_price = self.min_price_entry.get()
        user_input_max_price = self.max_price_entry.get()
        user_input_condition = self.condition_dropmenu.get()

        # print("USER INPUT THESE VALUES: ", user_input_keyword, user_input_category, user_input_min_price, user_input_max_price, user_input_condition)

        #Use user input to run search query
        search_results = AuthenticationService.search_item(keyword=user_input_keyword, category = user_input_category, min_price=user_input_min_price, max_price = user_input_max_price, condition = user_input_condition)
        # print(f"SEARCH RESULTS: {search_results}")

        #Withdraw search window after user hits the button and display Search Results window
        self.withdraw() 
        search_results_window = SearchResults(self.current_user, search_results, self.user_input_keyword, self.user_input_category, self.user_input_min_price, self.user_input_max_price, self.user_input_condition)
        search_results_window.mainloop()

class SearchResults(ctk.CTk):
    #Window details 
    def __init__(self, current_user, search_results, keyword, category, min_price, max_price, condition):
        super().__init__()
        self.title("Search Results")
        self.geometry("1200x600+200+200")
        self.configure(bg="#D3D3D3")
        self.focus_force()

        self.current_user = current_user

        #Pagination variables
        self.results_per_page = 25 #number of results displayed on page
        self.current_page = 1

        self.search_results = search_results
        
        self.total_pages = (len(search_results) + self.results_per_page - 1) // self.results_per_page
        # print(f"Search query returned {len(search_results)} results, which will be displayed over {self.total_pages} page(s).")

        # search content
        self.user_input_keyword = keyword
        self.user_input_category = category
        self.user_input_min_price = min_price
        self.user_input_max_price = max_price
        self.user_input_condition = condition

        #Frame for the report
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()
        
        #Prev and Next buttons for pagination
        self.prev_button = ctk.CTkButton(self, text="< Prev", command=self.prev_page)
        self.prev_button.pack(side='left', padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next >", command=self.next_page)
        self.next_button.pack(side='left', padx=20, pady=20)

        #'Back to Search' button
        self.cancel_button = ctk.CTkButton(self, text="Back to Search", command=self.return_to_search)
        self.cancel_button.pack(side='right', padx=20, pady=20)

    #Link each label to its respective window
    def open_view_item_window(self, item_id):
        view_item_view = ViewItemWindow(self.current_user, item_id, self)

    #Overlay label on top of returned item_name on result page
    def place_label_at_index(self, row_index, column_index, label_text, item_id):
        column_width = 270 
        spacing_factor = 18 #spacing between the rows
        move_down_amount = 35 #all labels shift down this amount holistically

        # Set the x and y coordinates based on row indices
        x = column_width 
        y = (row_index * spacing_factor) + move_down_amount  

        #Truncate label_text to first 40 characters so it fits in column
        label_text = label_text[:40]

        #Create and place the label
        item_label = tk.Label(self.input_frame, text=label_text, padx=50, pady=-10, fg="blue", bg="white", cursor="hand2")
        # print ("ACTUAL LABEL HEIGHT:", item_label.winfo_height())
        item_label.place(x=x, y=y, anchor=tk.CENTER)  # Place label at calculated coordinates

        #On left-click, label opens the viewItemWindow for that item, found via item_id
        item_label.bind("<Button-1>", lambda event, item_id=item_id: self.open_view_item_window(item_id))
        return item_label

    #Clears previous labels 
    def clear_labels (self):
        for label in self.input_frame.winfo_children():
            if isinstance (label, tk.Label):
                label.destroy() 

    def report_content(self):
        
        #Clear any existing labels
        self.clear_labels()
        # print("Cleared labels")

        #Destroy the old Treeview widget, if it exists
        if hasattr(self, 'tree') and isinstance(self.tree, ttk.Treeview):
            self.tree.destroy()
            # # print("Destroyed old Treeview widget")

        columns = ["ID", "Item Name", "Current Bid", "High Bidder", "Get It Now Price", "Auction Ends"]
        self.tree = ttk.Treeview(self.input_frame, columns=columns, show="headings")

        #Calculate start and end index for curernt page
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page
        # print(f"START INDEX ({start_index}), END INDEX ({end_index})")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        #Set the default width for columns
        default_column_width = 150  
        for col in columns:
            self.tree.column(col, width=default_column_width, anchor=tk.CENTER)

        #Set special widths for certain columns
        special_widths = {"ID": 100, "Item Name": 230, "Auction Ends": 250} 
        for col, width in special_widths.items():
            self.tree.column(col, width=width, anchor=tk.CENTER)


        row_index = 0 #Row where label is placed

        #Populate row data
        for item in self.search_results[start_index:end_index]:
            item_id, item_name, current_bid, high_bidder, get_it_now_price, auction_ends = item
            self.tree.insert("", tk.END, values=(item_id, item_name, current_bid, high_bidder, get_it_now_price, auction_ends))  

            #Place label in respective row in item_name column with item_name as text. Use item_id to generate ViewItemWindow
            self.place_label_at_index(row_index, 2, item_name, item_id) 

            #Increment row index for the next item
            row_index += 1

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.input_frame.update_idletasks()  #Refresh the page

    #Prev button functionality. If user is on first page of results, display error when clicked
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.report_content()
        else:
            messagebox.showerror("Error", "You are on the first page of Search Results. There are no previous results to be seen.")

    #Next button functionality. If user is on last page of results, display error when clicked
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.report_content()
        else:
            messagebox.showerror("Error", "You are on the last page of Search Results. There are no more results to be seen.")



    #Cancel button functionality
    def return_to_search(self):
        self.destroy()
        search_window = SearchWindow(self.current_user)
        search_window.mainloop()
    

    def refresh_search_results(self):
        
        # Rerun the search query with the same parameters
        # Retrieve the search parameters
        user_input_keyword = self.user_input_keyword
        user_input_category = self.user_input_category
        user_input_min_price = self.user_input_min_price
        user_input_max_price = self.user_input_max_price
        user_input_condition = self.user_input_condition

        # Run the search query again
        new_search_results = AuthenticationService.search_item(
            keyword=user_input_keyword,
            category=user_input_category,
            min_price=user_input_min_price,
            max_price=user_input_max_price,
            condition=user_input_condition
        )

        self.withdraw() 
        search_results_window = SearchResults(self.current_user, new_search_results, self.user_input_keyword, self.user_input_category, self.user_input_min_price, self.user_input_max_price, self.user_input_condition)
        search_results_window.mainloop()



class ListItemWindow(ctk.CTkToplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("New Item for Auction")
        self.geometry("800x600+200+200")
        self.configure(bg="#D3D3D3")
        self.focus_force()

        self.current_user = current_user

        # Frame for the category report
        self.list_item_frame = ctk.CTkFrame(self)
        self.list_item_frame.pack(pady=20, fill='both', expand=True)

        # Item Name Entry
        self.item_name_label = ctk.CTkLabel(self.list_item_frame, text="Item Name:")
        self.item_name_label.grid(row=0, column=0, padx=50, pady=(10, 20), sticky="w")
        self.item_name_entry = ctk.CTkEntry(self.list_item_frame)
        self.item_name_entry.grid(row=0, column=1, padx=30, pady=(10, 20), sticky="w")


        # Description Entry
        self.description_label = ctk.CTkLabel(self.list_item_frame, text="Description:")
        self.description_label.grid(row=1, column=0, padx=50, pady=(10, 20), sticky="w")
        self.description_entry = ctk.CTkEntry(self.list_item_frame)
        self.description_entry.grid(row=1, column=1, padx=30, pady=(10, 20), sticky="w")

        # Category Entry
        categories = ItemHandlerService.fetch_categories()
        for i in range(len(categories)):
            categories[i] = categories[i][0]

        self.category_label = ctk.CTkLabel(self.list_item_frame, text="Category:")
        self.category_label.grid(row=2, column=0, padx=50, pady=(10, 20), sticky="w")
        self.category_dropdown_entry = ctk.CTkOptionMenu(self.list_item_frame, values=categories, command=None, fg_color="#FFFFFF", text_color="#000000", button_color="#3a7ebf", button_hover_color="#2c679e")
        self.category_dropdown_entry.grid(row=2, column=1, padx=50, pady=(10, 20), sticky="w")
        self.category_dropdown_entry.set("") #set to blank row

        # Condition Entry
        conditions = ItemHandlerService.fetch_conditions()
        for i in range(len(conditions)):
            conditions[i] = conditions[i][0]

        self.condition_label = ctk.CTkLabel(self.list_item_frame, text="Condition:")
        self.condition_label.grid(row=3, column=0, padx=50, pady=(10, 20), sticky="w")
        self.condition_dropdown_entry = ctk.CTkOptionMenu(self.list_item_frame, values=conditions, command=None, fg_color="#FFFFFF", text_color="#000000", button_color="#3a7ebf", button_hover_color="#2c679e")
        self.condition_dropdown_entry.grid(row=3, column=1, padx=50, pady=(10, 20), sticky="w")
        self.condition_dropdown_entry.set("") #set to blank row

        # Starting Price Entry
        self.starting_price_label = ctk.CTkLabel(self.list_item_frame, text="Start auction bidding at: $")
        self.starting_price_label.grid(row=4, column=0, padx=50, pady=(10, 20), sticky="w")
        self.starting_price_entry = ctk.CTkEntry(self.list_item_frame)
        self.starting_price_entry.grid(row=4, column=1, padx=30, pady=(10, 20), sticky="w")

        # Min Sale Price Entry
        self.min_sale_price_label = ctk.CTkLabel(self.list_item_frame, text="Minimum sale price:")
        self.min_sale_price_label.grid(row=5, column=0, padx=50, pady=(10, 20), sticky="w")
        self.min_sale_price_entry = ctk.CTkEntry(self.list_item_frame)
        self.min_sale_price_entry.grid(row=5, column=1, padx=30, pady=(10, 20), sticky="w")

        # Auction Ends Entry
        auction_lengths = ItemHandlerService.fetch_auction_lengths()
        for i in range(len(auction_lengths)):
            auction_lengths[i] = auction_lengths[i][0]

        self.auction_ends_label = ctk.CTkLabel(self.list_item_frame, text="Auction ends in (days):")
        self.auction_ends_label.grid(row=6, column=0, padx=50, pady=(10, 20), sticky="w")
        self.auction_ends_dropdown_entry = ctk.CTkOptionMenu(self.list_item_frame, values=auction_lengths, command=None, fg_color="#FFFFFF", text_color="#000000", button_color="#3a7ebf", button_hover_color="#2c679e")
        self.auction_ends_dropdown_entry.grid(row=6, column=1, padx=50, pady=(10, 20), sticky="w")
        self.auction_ends_dropdown_entry.set("") #set to blank row

        # Get It Now Price Entry
        self.get_it_now_price_label = ctk.CTkLabel(self.list_item_frame, text="Get It Now Price:")
        self.get_it_now_price_label.grid(row=7, column=0, padx=50, pady=(10, 20), sticky="w")
        self.get_it_now_price_entry = ctk.CTkEntry(self.list_item_frame)
        self.get_it_now_price_entry.grid(row=7, column=1, padx=30, pady=(10, 20), sticky="w")

        self.get_it_now_price_optional_label = ctk.CTkLabel(self.list_item_frame, text="(optional)")
        self.get_it_now_price_optional_label.grid(row=7, column=2, padx=(0, 50), pady=(10, 20), sticky="w")

        # Returns Accepted Entry
        self.returns_accepted_label = ctk.CTkLabel(self.list_item_frame, text="Returns Accepted?")
        self.returns_accepted_label.grid(row=8, column=0, padx=50, pady=(10, 20), sticky="w")
        self.returns_checkbox = ctk.BooleanVar(value=False)
        self.returns_accepted_entry = ctk.CTkCheckBox(self.list_item_frame, text="", variable=self.returns_checkbox, onvalue=True, offvalue=False) #Need to implement radio box
        self.returns_accepted_entry.grid(row=8, column=1, padx=30, pady=(10, 20), sticky="w")

        # Cancel Button
        self.cancel_button = ctk.CTkButton(self.list_item_frame, text="Cancel", command=self.return_to_main_menu)
        self.cancel_button.grid(row=9, column=0, padx=50, pady=(10, 20), sticky="w")

        # List Button
        self.list_item_button = ctk.CTkButton(self.list_item_frame, text="List Item", command=self.list_item)
        self.list_item_button.grid(row=9, column=1, padx=50, pady=(10, 20), sticky="w")

    def return_to_main_menu(self):
        self.destroy()

    def list_item(self):
        username = self.current_user["username"] #No type checking needed
        name = self.item_name_entry.get() #No type checking needed
        description = self.description_entry.get() #No type checking needed
        category = self.category_dropdown_entry.get() #No type checking needed
        condition = self.condition_dropdown_entry.get() #No type checking needed
        starting_price = self.starting_price_entry.get()
        min_sale_price = self.min_sale_price_entry.get()
        auction_ends = self.auction_ends_dropdown_entry.get() #No type checking needed
        get_it_now_price = self.get_it_now_price_entry.get() 
        returns_accepted = self.returns_accepted_entry.get() #No type checking needed
        #Field validation
        #Get it now price is optional
        #Returns accepted can be False
        if (not name or not description or not category or not condition or not starting_price or not min_sale_price or not auction_ends):
            messagebox.showerror("Error", "All fields are required.")
            return
        
        #Type checking for starting price
        try:
            starting_price = float(starting_price)
        except:
            messagebox.showerror("Error", "Auction starting price should be a number.")
            return
        
        #Type checking for min sale price
        try:
            min_sale_price = float(min_sale_price)
        except:
            messagebox.showerror("Error", "Minimum sale price should be a number.")
            return
    
        #Type checking for get_it_now_price
        if get_it_now_price != "":
            try:
                get_it_now_price = float(get_it_now_price)
            except:
                messagebox.showerror("Error", "Get It Now Price should be a number.")
                return
        
        #Price validation
        if starting_price <= 0:
            messagebox.showerror("Error", "Starting auction price must be above 0.") 
            return 
        
        if min_sale_price <= 0:
            messagebox.showerror("Error", "Minimum sale price must be above 0.")
            return 
        
        if starting_price > min_sale_price:
            messagebox.showerror("Error", "Minimum sale price must be above or equal to the starting bid!")
            return
        
        if get_it_now_price != "":
            if get_it_now_price <= 0:
                messagebox.showerror("Error", "Get It Now Price must be above 0.")
                return
            if get_it_now_price <= starting_price:
                messagebox.showerror("Error", "Get It Now Price must be above starting bid!")
                return
            if get_it_now_price <= min_sale_price:
                messagebox.showerror("Error", "Get It Now Price must be above the minimum sale price!")
                return
            
        auction_ends = '%s DAY' % auction_ends

        AuthenticationService.list_item(username, name, condition, category, description, starting_price, min_sale_price, get_it_now_price, auction_ends, returns_accepted)

        #Get item id
        latest_item_id = ItemHandlerService.get_latest_item_id()[0] #Returns as a tuple, we want the number inside
        view_item_window = ViewItemWindow(self.current_user, latest_item_id, None)
        self.destroy()

        #Need an additional window to go back to main menu

class AuctionResultsWindow(ctk.CTk):
    def __init__(self, current_user):
        super().__init__()
        self.title("Auction Results")
        self.geometry("1200x800+200+200")
        self.configure(bg="#D3D3D3")
        self.focus_force()

        self.current_user = current_user
        self.auction_results = ItemHandlerService.get_auction_results()


        # Frame for the report
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        #Pagination variables
        self.results_per_page = 25 #number of results displayed on page
        self.current_page = 1

        self.total_pages = (len(self.auction_results) + self.results_per_page - 1) // self.results_per_page
        # print(f"Search query returned {len(self.auction_results)} results, which will be displayed over {self.total_pages} page(s).")
        
        self.report_content(self.auction_results)

        #Prev and Next buttons for pagination
        self.prev_button = ctk.CTkButton(self, text="< Prev", command=self.prev_page)
        self.prev_button.pack(side='left', padx=20, pady=20)

        self.next_button = ctk.CTkButton(self, text="Next >", command=self.next_page)
        self.next_button.pack(side='left', padx=20, pady=20)

        #Done button
        self.return_button = ctk.CTkButton(self, text="Done", command=self.return_to_main_menu)
        self.return_button.pack(side='right', padx=20, pady=10)

    # Label function used exclusively for the auction results page
    def place_label_at_index2(self, row_index, column_index, label_text, item_id):
        column_width = 270 
        spacing_factor = 18 #spacing between the rows
        move_down_amount = 35 #all labels shift down this amount holistically

        # Set the x and y coordinates based on row indices
        x = column_width
        y = (row_index * spacing_factor) + move_down_amount 

        #Truncate label_text to first 40 characters so it fits in column
        label_text = label_text[:46]

        #Create and place the label
        item_label = tk.Label(self.input_frame, text=label_text, padx=5, pady=-10, fg="blue", bg="white", cursor="hand2")
        # print ("ACTUAL LABEL HEIGHT:", item_label.winfo_height())
        item_label.place(x=x, y=y, anchor=tk.CENTER)  # Place label at calculated coordinates

        #On left-click, label opens the viewItemResultsWindow for that item, found via item_id
        item_label.bind("<Button-1>", lambda event, item_id=item_id: self.open_view_item_window(item_id))
        return item_label

    #Generates item result window using item_id
    def open_view_item_window(self, item_id):
        test_view_item_view = ViewItemWindow(self.current_user, item_id, None)

    #Clears previous labels 
    def clear_labels (self):
        for label in self.input_frame.winfo_children():
            if isinstance (label, tk.Label):
                label.destroy() 

    def report_content(self, auction_results):

        #Clear old content
        self.clear_labels() #clear any existing labels
        #Destroy the old Treeview widget, if it exists
        if hasattr(self, 'tree') and isinstance(self.tree, ttk.Treeview):
            self.tree.destroy()

        columns = ["ID", "Item Name", "Sale Price", "Winner", "Auction Ended"]
        self.tree = ttk.Treeview(self.input_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        # Set the window size to match the input frame
        # self.geometry("1200x800+200+200")

        #Set special widths for each column
        special_widths = {"ID": 100, "Item Name": 220, "Sale Price": 150, "Winner": 250, "Auction Ended": 250} 
        for col, width in special_widths.items():
            self.tree.column(col, width=width, anchor=tk.CENTER)

        #Calculate start and end index for current page
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page
        row_index = 0 #Row where label is placed

        #Populate data on page from query
        for item in auction_results[start_index:end_index]:
            item_id, item_name, sale_price, winner, auction_ends = item
            # print(f"item_id: {item_id} \n item_name: {item_name} \n sale_price: {sale_price} \n winner: {winner} \n auction_ends: {auction_ends}")
            self.tree.insert("", tk.END, values=item)

            #Place label in respective row in item_name column. Clicking window leads to its ViewItemResults window, generated through its item_id 
            self.place_label_at_index2(row_index, 2, item_name, item_id) 

            #Increment row index to place next item
            row_index += 1

        self.tree.pack(fill=tk.BOTH, expand=True)

    #Done button functionality - returns user to main menu
    def return_to_main_menu(self):
        self.destroy()
        main_menu_window = MainMenuWindow(self.current_user)
        main_menu_window.mainloop()

    #Prev button functionality. If user is on first page of results, display error when clicked
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.report_content(self.auction_results)
        else:
            messagebox.showerror("Error", "You are on the first page of Auction Results. There are no previous results to be seen.")

    #Next button functionality. If user is on last page of results, display error when clicked
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.report_content(self.auction_results)
        else:
            messagebox.showerror("Error", "You are on the last page of Auction Results. There are no more results to be seen.")


class UserReportsWindow(ctk.CTkToplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("User Report")
        self.geometry("1200x600+600+400")
        self.configure(bg="#D3D3D3")
        self.focus_force()

        self.current_user = current_user

        # Frame for the report
        self.report_frame = ctk.CTkFrame(self)
        self.report_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()

        self.return_button = ctk.CTkButton(self, text="Done", command=self.return_to_main_menu)
        self.return_button.pack(side=tk.BOTTOM, padx=20, pady=10)

    def report_content(self):
        items = GenerateReportService.user_report()

        columns = ["Username", "Listed", "Sold", "Won", "Rated", "Most Frequent Condition"]
        self.tree = ttk.Treeview(self.report_frame, columns=columns, show="headings")
        
        default_column_width = 150
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=default_column_width, anchor=tk.CENTER)

        #Set special widths for username and most frequent condition column. other columns use default_column_width
        special_widths = {"Username": 250, "Most Frequent Condition": 250} 
        for col, width in special_widths.items():
            self.tree.column(col, width=width, anchor=tk.CENTER)

        for item in items:
            self.tree.insert("", tk.END, values=item)
        self.tree.pack(fill=tk.BOTH, expand=True)

    #'Done' button functionality
    def return_to_main_menu(self):
        self.destroy()


class TopRatedItems(ctk.CTkToplevel):
    def __init__(self,current_user):
        super().__init__()
        self.title("Top Rated Items")
        self.geometry("800x600+600+400")
        self.configure(bg="#D3D3D3")  # Light grey color
        self.focus_force()

        self.current_user = current_user

        self.report_frame = ttk.Frame(self)
        self.report_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()

        self.done_button = ctk.CTkButton(self.report_frame, text="Done", command=self.close_report)
        self.done_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def report_content(self,):
        items = GenerateReportService.top_rated_items_report()

        columns = ["Item Name", "Average Rating", "Rating Count"]
        self.tree = ttk.Treeview(self.report_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        for row in items:
            self.tree.insert("", "end", values=row)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def close_report(self):
        self.destroy()

class AuctionStatsWindow(ctk.CTkToplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("Auction Statistics")
        self.geometry("800x600+600+400")
        self.configure(bg="#D3D3D3")  # Light grey color
        self.focus_force()

        self.current_user = current_user

        self.report_frame = ttk.Frame(self)
        self.report_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()

        self.done_button = ctk.CTkButton(self.report_frame, text="Done", command=self.close_report)
        self.done_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def report_content(self):
        stats = GenerateReportService.auction_statistics_report()

        columns = ["Statistic", "Value"]
        self.tree = ttk.Treeview(self.report_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        for stat_name, value in stats.items():
            self.tree.insert("", "end", values=(stat_name, value))
        self.tree.pack(fill=tk.BOTH, expand=True)

    def close_report(self):
        self.destroy()

class CancelledAuctionDetailsWindow(ctk.CTkToplevel):
    def __init__(self, current_user):
        super().__init__()
        self.title("Cancelled Auction Details")
        self.geometry("1000x600+600+400")
        self.configure(bg="#D3D3D3")
        self.current_user = current_user
        self.focus_force()

        # Frame for the report
        self.report_frame = ctk.CTkFrame(self)
        self.report_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.report_content()

        self.return_button = ctk.CTkButton(self, text="Return", command=self.return_to_main_menu)
        self.return_button.pack(side=tk.BOTTOM, padx=20, pady=10)
    
    def report_content(self):
        items = GenerateReportService.cancelled_auctions_report()

        columns = ["ID", "Listed By", "Cancelled Date", "Reason"]
        self.tree = ttk.Treeview(self.report_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Setting the column widths
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Listed By", width=150, anchor=tk.CENTER)
        self.tree.column("Cancelled Date", width=250, anchor=tk.CENTER)
        self.tree.column("Reason", width=400, anchor=tk.W)  # Make "Reason" column wider

        for item in items:
            self.tree.insert("", tk.END, values=item)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def return_to_main_menu(self):
        self.destroy()

class ViewItemWindow(ctk.CTkToplevel):
    def __init__(self, current_user, item_id, parent_window):
        super().__init__()
        self.geometry("1300x600+250+250")
        self.configure(bg="#D3D3D3")  # Light grey color
        self.focus_force()
        self.current_user = current_user
        self.item_id = item_id
        self.parent_window = parent_window
        self.text_description = None
        self.item_info = {}
        self.load_item_information()
        self.current_time = AuthenticationService.get_current_time()[0][0]

    def load_item_information(self):

        # Fetch item information
        item_info_result = ItemHandlerService.fetch_item_info(self.item_id)

        if item_info_result:
            self.item_info = {
                "Item ID": item_info_result[0][0],
                "Item Name": item_info_result[0][1],
                "Description": item_info_result[0][2],
                "Category": item_info_result[0][3],
                "Condition": item_info_result[0][4],
                "Returns Accepted?": item_info_result[0][5],
                "Get It Now Price": item_info_result[0][6],
                "Auction Ends": item_info_result[0][7],
                "Cancellation Reason": item_info_result[0][8]
            }
        else:
            messagebox.showerror("Error", "Item not found.")
            self.item_info = {}  # Reset to empty dict if not found
            return

        seller_username = item_info_result[0][10]
        self.minimum_bid = item_info_result[0][9]
        min_sale_price = item_info_result[0][11]
        auction_end_time = item_info_result[0][7]
        self.current_time = AuthenticationService.get_current_time()[0][0]
        self.auction_ended = auction_end_time < self.current_time

        self.is_winner = False

        if self.auction_ended:
            self.title("Item Results")
        else:
            self.title("Item for Sale")

        # Check if current user is the seller
        is_seller = self.current_user['username'] == seller_username
        if_admin = self.current_user['user_type'] == "Admin"

        # Display item information
        for key, value in self.item_info.items():
            label_frame = ctk.CTkFrame(self)
            label_frame.pack(fill="x", padx=10, pady=2)

            if key == "Auction Ends" and self.auction_ended: #Auction Ended
                label_key = ctk.CTkLabel(label_frame, text="Auction Ended:", font=("Arial", 10))
            else: #Regular case
                label_key = ctk.CTkLabel(label_frame, text=key + ":", font=("Arial", 10))
            label_key.pack(side="left")


            if key == "Returns Accepted?":
                # Determine the text to display based on the boolean value
                returns_text = "Yes" if value else "No"
                returns_label = ctk.CTkLabel(label_frame, text=f"{returns_text}", font=("Arial", 10, "bold"))
                returns_label.pack(side="left")


            elif key == "Description":
                # Create a container frame to hold both the description and the button
                container_frame = ctk.CTkFrame(label_frame)
                container_frame.pack(fill="both", expand=True, padx=5, pady=5)

                # Create a frame within the container to hold the text widget and the scrollbar
                description_frame = ctk.CTkFrame(container_frame)
                description_frame.pack(side="left", fill="both", expand=True)

                # Create a scrollable text widget for the description
                self.text_description = tk.Text(description_frame, height=4, wrap="word", padx=5, pady=5, font=("Arial", 10))
                self.text_description.insert("1.0", value)
                self.text_description.config(state="disabled")  # Make the text read-ongitly
                self.text_description.pack(side="left", fill="both", expand=True)

                # Create a scrollbar for the text widget
                scrollbar = tk.Scrollbar(description_frame, command=self.text_description.yview)
                scrollbar.pack(side="right", fill="y")
                self.text_description.config(yscrollcommand=scrollbar.set)

                # Check if the user is a seller, and if so, add the "Edit Description" button
                if is_seller:
                    if self.auction_ended == False:
                        edit_description_button = ctk.CTkButton(container_frame, text="Edit Description",
                                                                command=self.edit_description)
                        # Place the button to the right within the container frame, aligning it with the description frame
                        edit_description_button.pack(side="right", padx=10)

            elif key == "Get It Now Price":
                inner_frame = ctk.CTkFrame(label_frame)
                inner_frame.pack(side="left")

                # Format the price with a dollar sign
                formatted_price = f"${value:.2f}" if isinstance(value, (int, float)) else f"${value}"
                label_value = ctk.CTkLabel(inner_frame, text=formatted_price, font=("Arial", 10, "bold"))
                label_value.pack(side="left")

                # Add Get It Now button, make it smaller and position it next to the Get It Now Price label
                if value and not is_seller and not self.auction_ended:
                    get_it_now_button = ctk.CTkButton(inner_frame, text="Get It Now!", command=self.buy_item)
                    get_it_now_button.pack(side="left", padx=5)

            elif key == "Item ID":
                inner_frame = ctk.CTkFrame(label_frame)
                inner_frame.pack(fill='x', expand=True)  # Ensure the frame expands
                label_value = ctk.CTkLabel(inner_frame, text=value, font=("Arial", 10, "bold"))
                label_value.pack(side="left")

                # View Rating Button
                view_ratings_button = ctk.CTkButton(inner_frame, text="View Ratings", command=self.view_ratings)
                view_ratings_button.pack(side="right", padx=5)

            else:
                # Assuming 'value' might be a numerical value needing formatting as a monetary value
                label_value = ctk.CTkLabel(label_frame, text=value, font=("Arial", 10, "bold"))
                label_value.pack(side="left")


        # Display bid history
        bid_history_frame = ctk.CTkFrame(self)
        bid_history_frame.pack(pady=10, fill='x', expand=True)  # Make the bid history frame wider

        bid_history_title = ctk.CTkLabel(bid_history_frame, text="Latest Bids", font=("Arial", 12, "bold"))
        bid_history_title.pack()

        # Container for headers to make them centrally aligned
        bid_headers_frame = ctk.CTkFrame(bid_history_frame)
        bid_headers_frame.pack(fill="x", expand=True)  # Fill and expand to make it wider

        # Headers
        bid_amount_header = ctk.CTkLabel(bid_headers_frame, text="Bid Amount", font=("Arial", 10, "bold"), anchor="center")
        bid_amount_header.pack(side="left", fill='x', expand=True, padx=10)

        time_of_bid_header = ctk.CTkLabel(bid_headers_frame, text="Time of Bid", font=("Arial", 10, "bold"), anchor="center")
        time_of_bid_header.pack(side="left", fill='x', expand=True, padx=10)

        username_header = ctk.CTkLabel(bid_headers_frame, text="Username", font=("Arial", 10, "bold"), anchor="center")
        username_header.pack(side="left", fill='x', expand=True, padx=10)

        # Fetch recent bid history
        # if item is cancelled then no bid history
        recent_bids = ItemHandlerService.fetch_bidding_info(self.item_id)
        if recent_bids: #:
            for index, bid in enumerate(recent_bids):
                bid_frame = ctk.CTkFrame(bid_history_frame)
                bid_frame.pack(fill="x", expand=True)  # Fill and expand to make it wider

                # Data labels, centrally aligned within their respective spaces
                if index == 0 and self.auction_ended:
                    if bid[0] == 0: #Cancelled
                        bid_amount_label = ctk.CTkLabel(bid_frame, text=f"CANCELLED", font=("Arial", 10), anchor="center", fg_color='#FF6347')
                        time_of_bid_label = ctk.CTkLabel(bid_frame, text=bid[1], font=("Arial", 10), anchor="center", fg_color='#FF6347')
                        username_label = ctk.CTkLabel(bid_frame, text="Administrator", font=("Arial", 10), anchor="center", fg_color='#FF6347')
                    elif bid[0] < min_sale_price: #No winner
                        bid_amount_label = ctk.CTkLabel(bid_frame, text=f"${bid[0]}", font=("Arial", 10), anchor="center", fg_color='#FFFF00')
                        time_of_bid_label = ctk.CTkLabel(bid_frame, text=bid[1], font=("Arial", 10), anchor="center", fg_color='#FFFF00')
                        username_label = ctk.CTkLabel(bid_frame, text=bid[2], font=("Arial", 10), anchor="center", fg_color='#FFFF00')
                    elif bid[0] >= min_sale_price: #Winner
                        bid_amount_label = ctk.CTkLabel(bid_frame, text=f"${bid[0]}", font=("Arial", 10), anchor="center", fg_color='#32CD32')
                        time_of_bid_label = ctk.CTkLabel(bid_frame, text=bid[1], font=("Arial", 10), anchor="center", fg_color='#32CD32')
                        username_label = ctk.CTkLabel(bid_frame, text=bid[2], font=("Arial", 10), anchor="center", fg_color='#32CD32')
                        self.is_winner = self.current_user['username'] == bid[2]

                else:
                    bid_amount_label = ctk.CTkLabel(bid_frame, text=f"${bid[0]}", font=("Arial", 10), anchor="center")
                    time_of_bid_label = ctk.CTkLabel(bid_frame, text=bid[1], font=("Arial", 10), anchor="center")
                    username_label = ctk.CTkLabel(bid_frame, text=bid[2], font=("Arial", 10), anchor="center")

                bid_amount_label.pack(side="left", fill='x', expand=True, padx=10)
                time_of_bid_label.pack(side="left", fill='x', expand=True, padx=10)
                username_label.pack(side="left", fill='x', expand=True, padx=10)


        else:
            no_bid_label = ctk.CTkLabel(bid_history_frame, text="No recent bids.", font=("Arial", 10))
            no_bid_label.pack()



        # Check if current user is the seller, if yes, hide bid input
        if self.current_user['username'] == seller_username:
            seller_label = ctk.CTkLabel(self, text="You are the seller of this item.", font=("Arial", 10, "bold"))
            seller_label.pack(pady=10)
        else:
            if self.auction_ended == False:
                # Create a frame to hold the label and entry together in the same row
                bid_frame = ctk.CTkFrame(self)
                bid_frame.pack(pady=10)

                # Display bid input only if the user is not the seller
                your_bid_label = ctk.CTkLabel(bid_frame, text="Your Bid  $", font=("Arial", 12))
                your_bid_label.pack(side="left", padx=(0,10))  # Adjust padding as needed

                self.your_bid_entry = ctk.CTkEntry(bid_frame)
                self.your_bid_entry.pack(side="left")

                # Add a label next to the entry to display the minimum bid
                minimum_bid_label = ctk.CTkLabel(bid_frame, text=f"(Minimum bid $ {self.minimum_bid})", font=("Arial", 12))
                minimum_bid_label.pack(side="left", padx=(10,0))  # Add some padding for spacing

        # Add buttons aligned to the right at the bottom
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="bottom", pady=10, fill="x")

        # Close button
        close_button = ctk.CTkButton(button_frame, text="Close", command=self.close_window)
        close_button.pack(side="right", padx=10)

        # Cancel button -- only admin can see
        # if auction cancelled then cancel button cannot click
        if if_admin and not self.item_info["Cancellation Reason"] and self.auction_ended == False:
            # admin and not canceled and not ended
            cancel_button = ctk.CTkButton(button_frame, text="Cancel this Item", command=self.cancel_item)
            cancel_button.pack(side="right", padx=10)

        # Bid button (conditionally added if not a seller, as per your previous logic, not shown here for brevity)
        if not self.item_info["Cancellation Reason"] and self.current_user['username'] != seller_username and not self.auction_ended:
            bid_button = ctk.CTkButton(button_frame, text="Bid On this Item", command=self.place_bid, state="normal")
            bid_button.pack(side="right", padx=5)

    def refresh_content(self):
        # Destroy existing widgets in the window
        for widget in self.winfo_children():
            widget.destroy()

        # Reinitialize UI components
        self.load_item_information()

    def place_bid(self):

        # Fetch the current user's username, item ID, and bid amount
        username = self.current_user['username']
        item_id = self.item_id

        try:
            bid_amount = float(self.your_bid_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bid amount.")
            return

        # Fetch current highest bid and get it now price
        highest_bid, get_it_now_price = ItemHandlerService.check_bid_price(item_id)

        # Validate the bid amount
        if bid_amount < self.minimum_bid:
            messagebox.showerror("Invalid Bid", "Your bid must be higher than the current highest bid.")
        elif get_it_now_price != None and bid_amount >= get_it_now_price:
            messagebox.showerror("Invalid Bid", "Your bid must be less than the Get It Now price.")
        else:
            # Insert the bid
            try:
                ItemHandlerService.bid_on_item(username, item_id, bid_amount)
                messagebox.showinfo("Success", f"Bid of ${bid_amount} placed successfully.")
                self.refresh_content() # Refresh the window with updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to place bid. Error: {str(e)}")

    def buy_item(self):
        # Here you would implement the functionality to buy the item immediately

        # self.current_user
        item_info_result = ItemHandlerService.fetch_item_info(self.item_id)
        if item_info_result:
            get_it_now_price = item_info_result[0][6]

            # Attempt to immediately buy the item
            buy_item_result = ItemHandlerService.get_it_now(self.current_user['username'], self.item_id, get_it_now_price)

            if buy_item_result:
                # If the bid placement and any other operations were successful, show the success message
                messagebox.showinfo("Success", "Item purchased successfully.")
                self.refresh_content() # Refresh the window with updated data
            else:
                # If the operation failed, show an error message
                messagebox.showerror("Error", "Failed to purchase the item.")
        else:
            # If fetching item information failed, show an error message
            messagebox.showerror("Error", "Failed to fetch item information.")

    def close_window(self):
        self.destroy()
        if self.parent_window:
            self.parent_window.refresh_search_results()

    def cancel_item(self):
        # Prompt for a cancellation reason
        reason = simpledialog.askstring("Cancel Item", "Enter a cancellation reason:", parent=self)
        if reason is None:  # The dialog was canceled
            return  # Do not proceed with cancellation

        cancellation_reason = reason if reason.strip() else "Cancelled by Admin"

        # Assuming you have a method in ItemHandlerService to cancel an item
        try:
            ItemHandlerService.cancel_item(self.item_id, cancellation_reason, self.current_user['username'])
            messagebox.showinfo("Cancelled", "The item has been successfully canceled.")
            #self.load_item_information()  # Refresh item details to reflect cancellation
            self.destroy()
            if self.parent_window:
                self.parent_window.refresh_search_results()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel the item: {str(e)}")

    def view_ratings(self):
        ratings_window = RateItemWindow(self.current_user, self.item_id, self.is_winner)

    def update_description(self, new_description):
        # Assuming text_description is the Text widget for displaying the item description
        if self.text_description:
            self.text_description.config(state="normal")  # Enable text widget for editing
            self.text_description.delete("1.0", tk.END)  # Clear existing content
            self.text_description.insert("1.0", new_description)  # Insert new description
            self.text_description.config(state="disabled")  # Optionally make it read-only again

    def edit_description(self):
        # Here you would implement the functionality to edit description
        current_description = ItemHandlerService.fetch_item_info(self.item_id)[0][2]
        edit_window = EditDescriptionWindow(self, self.item_id, current_description)
        edit_window.grab_set()  # Optional: Makes the edit window modal


class EditDescriptionWindow(ctk.CTkToplevel):
    def __init__(self, master, item_id, current_description):
        super().__init__(master)
        self.title("Edit Item Description")
        self.geometry("400x300")
        self.focus_force()
        self.item_id = item_id
        self.current_description = current_description

        # Description Text Field
        self.description_text = tk.Text(self, height=10, wrap="word")
        self.description_text.insert("1.0", self.current_description)
        self.description_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Save Button
        save_button = ctk.CTkButton(self, text="Save", command=self.save_description)
        save_button.pack(side="left", padx=10, pady=10)

        # Cancel Button
        cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=10, pady=10)

    def save_description(self):
        new_description = self.description_text.get("1.0", "end-1c")
        # Assuming ItemHandlerService.update_item_description method exists and works correctly
        ItemHandlerService.update_item_description(self.item_id, new_description)
        # Notify the master (ViewItemWindow) to refresh the item information
        self.master.update_description(new_description)
        # Close the edit window
        self.destroy()
        messagebox.showinfo("Edit Description", "Description saved!")


class RateItemWindow(ctk.CTkToplevel):
    def __init__(self, current_user, item_id, is_winner):
        super().__init__()
        self.title("Rate Item")
        self.geometry("800x600+250+250")
        #self.configure(bg="#D3D3D3")  # Light grey color
        self.focus_force()

        self.current_user = current_user
        self.item_id = item_id
        self.is_winner = is_winner
        self.can_create_rating = self.is_winner and not ItemHandlerService.has_user_rated(self.item_id, self.current_user['username'])

        self.setup_ui()

        self.item_info = {}  # Define the item_info dictionary

        self.load_item_information()

        self.selected_rating = 0

    def setup_ui(self):

        # Setup labels for item information

        self.value_item_id = ctk.CTkLabel(self, text="")
        self.value_item_id.pack(fill="x", padx=10, pady=2, anchor="w")  # Align content to the left

        self.value_item_name = ctk.CTkLabel(self, text="")
        self.value_item_name.pack(fill="x", padx=10, pady=2, anchor="w")  # Align content to the left

        # Average rating display
        self.average_rating_label = ctk.CTkLabel(self, text="Average Rating")
        self.average_rating_label.pack(fill="x", padx=10, pady=2, anchor="w")  # Align content to the left

        # Container for rating entries
        self.ratings_container_frame = ctk.CTkFrame(self)
        self.ratings_container_frame.pack(fill="both", expand=True, padx=2, pady=2)


        # Rating submission area
        if self.can_create_rating:
            self.my_rating_frame = ctk.CTkFrame(self)
            self.my_rating_frame.pack(fill='x', padx=20, pady=(10, 0))

            my_rating_label = ctk.CTkLabel(self.my_rating_frame, text="My Rating: ")
            my_rating_label.pack(side="left")

            self.star_rating_frame = ctk.CTkFrame(self.my_rating_frame)
            self.star_rating_frame.pack(side="left", padx=10)

            # Using tk.Label for stars
            self.star_labels = []
            for i in range(5):
                label = tk.Label(self.star_rating_frame, text="☆", cursor="hand2")
                label.bind("<Button-1>", lambda e, i=i: self.set_rating(i+1))
                label.pack(side="left", padx=0)  # Adjust padding as needed
                self.star_labels.append(label)

            # Adding a title for the comment box
            self.comment_title = ctk.CTkLabel(self, text="Comments:")
            self.comment_title.pack(side="left", fill='x', padx=20, pady=(10, 2))

            # Add a frame for the comment box for better layout management
            self.comment_frame = ctk.CTkFrame(self)
            self.comment_frame.pack(fill='both', expand=True, padx=20, pady=2)

            self.comment_text = tk.Text(self.comment_frame, height=3)  # Adjusted height to 3
            self.comment_text.pack(fill='both', expand=True)

            # Buttons to submit rating or close window
            self.submit_button = ctk.CTkButton(self, text="Rate This Item", command=self.submit_rating)
            self.submit_button.pack(side="right", fill='x', padx=10, pady=10)

            self.close_button = ctk.CTkButton(self, text="Close", command=self.close_window)
            self.close_button.pack(side="right", fill='x', padx=10, pady=10)
        else:
            self.close_button = ctk.CTkButton(self, text="Close", command=self.close_window)
            self.close_button.place(relx=0.98, rely=0.98, anchor='se')

    
    def set_rating(self, rating):
        # print('Rating set to:', rating)
        
        self.selected_rating = rating
        for i in range(5):
            if i < rating:
                self.star_labels[i].configure(text="★")
            else:
                self.star_labels[i].configure(text="☆")

    def submit_rating(self):
        comment = self.comment_text.get("1.0", "end-1c").strip()
        if not self.selected_rating:
            rating = 0
        else:
            rating = self.selected_rating
        # print('Rating:',rating)
        # print('Comments:',comment)
        # Ensure a rating has been selected; None indicates no selection
        
        success = ItemHandlerService.submit_rating(self.item_id, rating, comment)
        if success:
            messagebox.showinfo("Success", "Your rating has been submitted.")
            self.destroy()  # Refresh the window after submission
            rate_item_window = RateItemWindow(self.current_user, self.item_id, self.is_winner)
        else:
            messagebox.showerror("Error", "There was an issue submitting your rating.")
        

    def close_window(self):
        # Close the rate item window
        self.destroy()

    def load_item_information(self):
        # Fetch item information
        item_info_result = ItemHandlerService.fetch_item_info(self.item_id)

        if item_info_result:
            self.item_info = {
                "Item ID": item_info_result[0][0],
                "Item Name": item_info_result[0][1],
                "Description": item_info_result[0][2],
                "Category": item_info_result[0][3],
                "Condition": item_info_result[0][4],
                "Returns Accepted?": item_info_result[0][5],
                "Get It Now Price": item_info_result[0][6],
                "Auction Ends": item_info_result[0][7]
            }

            # Update labels with the fetched information
            self.value_item_id.configure(text=f"Item ID: {self.item_info['Item ID']}", anchor="w")
            self.value_item_name.configure(text=f"Item Name: {self.item_info['Item Name']}", anchor="w")

        else:
            messagebox.showerror("Error", "Item not found.")
            self.item_info = {}  # Reset to empty dict if not found
            return
        
        # fetch avg rating score
        item_name = self.item_info.get("Item Name", "Unknown Item")
        average_rating_result = ItemHandlerService.fetch_average_rating(item_name)
        if average_rating_result:
            # Assuming the result is a float, format it to show one decimal place
            average_rating = f"{average_rating_result[0][0]:.1f}"
        else:
            average_rating = "No ratings yet"

        # Update the average rating label
        self.average_rating_label.configure(text=f"Average Rating: {average_rating}", anchor="w")

        self.display_ratings()

    def display_ratings(self):
        # Clear previous ratings from the container frame
        for widget in self.ratings_container_frame.winfo_children():
            widget.destroy()
        self.ratings_container_frame.pack_configure(padx=5, pady=5, expand=False)

        # Fetch the rating history
        item_name = self.item_info.get("Item Name", "Unknown Item")
        user_ratings_result = ItemHandlerService.fetch_user_ratings(item_name)

        # User ratings section: directly create UI elements in the container
        # Limit to 3 if the user can bid, otherwise 5
        for i in range(min(3 if self.can_create_rating else 5, len(user_ratings_result))):
            self.create_rating_entry(user_ratings_result[i], self.ratings_container_frame)
    
    def create_rating_entry(self, rating, parent_frame):
        username, stars, comment, rating_date, rating_item_id = rating
        date_str = rating_date.strftime('%Y-%m-%d %H:%M:%S')

        rating_frame = ctk.CTkFrame(parent_frame, corner_radius=5)  # Reduced corner radius
        rating_frame.pack(fill="x", expand=True, pady=1)

        top_frame = ctk.CTkFrame(rating_frame)
        top_frame.pack(fill="x", expand=True, pady=2)

        # "Rated by" label
        user_label = ctk.CTkLabel(top_frame, text=f"Rated by: {username}")
        user_label.grid(row=0, column=0, sticky="w", padx=5)

        # Stars label
        stars_label = ctk.CTkLabel(top_frame, text='★' * stars + '☆' * (5 - stars), fg_color="gold")
        stars_label.grid(row=0, column=1, padx=5)

        # Date label, now inside top_frame, aligned to the right
        date_label = ctk.CTkLabel(top_frame, text=f"Date: {date_str}")
        # Assuming you want it to the far right, we can use column=2 and stick to the east (right)
        # Use columnspan to ensure it does not conflict with other elements
        date_label.grid(row=0, column=2, sticky="e", padx=5)

        # Check if the current user is the user who rated, and if so, add a delete button
        if self.current_user['user_type'] == 'Admin' or username == self.current_user['username']:
            delete_button = ctk.CTkButton(top_frame, text="Delete Rating", command=lambda: self.delete_rating(rating_item_id))
            if username == self.current_user['username']:  # Adjust this condition based on your user identification logic
                delete_button = ctk.CTkButton(top_frame, text="Delete My Rating", command=lambda: self.delete_rating(rating_item_id))
            delete_button.grid(row=0, column=3, padx=5)

        comment_frame = ctk.CTkFrame(rating_frame, corner_radius=10)
        comment_frame.pack(fill="x", expand=True, pady=2)

        comment_label = ctk.CTkLabel(comment_frame, text=comment if comment else "No comments", wraplength=500)
        comment_label.pack(padx=10, pady=5, fill="both", expand=True)


    def delete_rating(self, rating_item_id):
        # Implement the logic to delete the current user's rating for this item
        success = ItemHandlerService.delete_user_rating(rating_item_id)
        messagebox.showinfo("Success", "Your rating has been deleted.")
        self.destroy()  # Refresh the window after submission
        rate_item_window = RateItemWindow(self.current_user, self.item_id, self.is_winner)
        
