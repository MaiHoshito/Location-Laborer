import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import requests


root = tk.Tk()
# root.attributes("-fullscreen", True)
root.state("zoomed")
root.option_add("*Font", ("Microsoft YaHei", 15))
root.option_add("*Foreground", "#3E2813")
root.option_add("*Label.background", "#FEFAE0")
root.option_add("*Button.background", "#E7C8A0")
root.configure(bg='#FEFAE0')
root.title('Location Laborer')

suggest_url = 'https://restapi.amap.com/v3/assistant/inputtips?parameters'
geocode_url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
cols = [None] * 3
key = None

def suggestion(address):
    params = {
     'keywords': address,
     'key': key
    }
    response = requests.get(suggest_url, params=params)
    data = response.json()
    if len(data['tips']) > 0:
        return data['tips'][0]
    else:
        return 'Error: Address not found'
    
def geocode(address):
    params = {
     'address': address,
     'key': key
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()
    if data['status'] == '1':
        return data['geocodes'][0]
    else:
        return 'Error: Address not found'

def analyse(address):
    suggest_info = suggestion(address)
    geo_info = geocode(address)
    if type(suggest_info) == str:
        cols[1] = suggest_info
    else:
        district_len = len(suggest_info['district'])
        address_len = len(suggest_info['address'])
        if suggest_info['name'][:district_len] == suggest_info['district']:
            suggest_info['name'] = suggest_info['name'][district_len:]
        if suggest_info['name'][:address_len] == suggest_info['address']:
            suggest_info['name'] = suggest_info['name'][address_len:]
        cols[1] = ''.join([suggest_info[key] for key in ['district', 'address', 'name'] if len(suggest_info[key]) > 0])
           
    if type(geo_info) == str:
        cols[2] = geo_info
    else:
        cols[2] = geocode(address)['formatted_address']
    return cols, suggest_info, geo_info

def on_import():
    global df, current_row

    # Ask the user to select a .csv file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    # Load the data from the .csv file
    df = pd.read_csv(file_path)

    # Check if the DataFrame has the required columns
    if "final_address" in df.columns and "final_lon" in df.columns and "final_lat" in df.columns and "geo_info" in df.columns and "suggest_info" in df.columns:
    # Find the first empty row in these columns
        current_row = df[["final_address", "final_lon", "final_lat", "geo_info", "suggest_info"]].isnull().all(axis=1).idxmax()
    else:
    # Create the required columns
        df["final_address"] = np.nan
        df["final_lon"] = np.nan
        df["final_lat"] = np.nan
        df["geo_info"] = np.nan
        df["suggest_info"] = np.nan
        current_row = 0

    # Create a new window for column selection
    selection_window = tk.Toplevel(root)
    selection_window.configure(bg='#FEFAE0')

    # Create drop-down menus to select the column
    col1_label = tk.Label(selection_window, text="Select original address:")
    col1_label.grid(row=0,column=0)
    col1_var = tk.StringVar(selection_window)
    col1_var.set(df.columns[0])
    col1_menu = tk.OptionMenu(selection_window, col1_var, *df.columns)
    col1_menu.grid(row=1,column=0)

    # Create an input bar for the user to enter a key value
    key_label = tk.Label(selection_window, text="Enter key:")
    key_label.grid(row=2,column=0)
    key_entry = tk.Entry(selection_window)
    key_entry.grid(row=3,column=0)

    def on_submit():
        global cols, key, suggest_info, geo_info

        key = key_entry.get()

        # Get the selected columns and poccessed values
        cols[0] = col1_var.get()
        
        cols, suggest_info, geo_info = analyse(df[cols[0]].iloc[current_row])

        # Update the width of the entry widgets
        # entry1.config(width=len(df[cols[0]].iloc[current_row])*2)
        # entry2.config(width=len(cols[1])*2)
        # entry3.config(width=len(cols[2])*2)

        # Show the first row of the 3 columns
        entry1.config(state='normal')
        entry1.delete(0, tk.END)
        entry1.insert(0, df[cols[0]].iloc[current_row])
        entry1.config(state='readonly')
        
        entry2.config(state='normal')
        entry2.delete(0, tk.END)
        entry2.insert(0, cols[1])
        entry2.config(state='readonly')
        
        entry3.config(state='normal')
        entry3.delete(0, tk.END)
        entry3.insert(0, cols[2])
        entry3.config(state='readonly')
        
        # Set the default text of the entry widget
        entry.delete(0, tk.END)
        entry.insert(0, df[cols[0]].iloc[current_row])

        # Close the selection window
        selection_window.destroy()

    # Create a submit button
    submit_button = tk.Button(selection_window, text="Submit", command=on_submit)
    submit_button.grid(row=2,column=1)

def on_next():
    global current_row, cols, suggest_info, geo_info
    
    if current_row >= len(df) - 1:
        # Create a pop-up window using tkinter's messagebox
        messagebox.showinfo("End of data", "You have reached the end of the data.")
        return
    
    # Increment the current row
    current_row += 1
    
    cols, suggest_info, geo_info = analyse(df[cols[0]].iloc[current_row])

    # Update the width of the entry widgets
    # entry1.config(width=len(df[cols[0]].iloc[current_row])*2)
    # entry2.config(width=len(cols[1])*2)
    # entry3.config(width=len(cols[2])*2)

    # Show the next row of the 3 columns
    entry1.config(state='normal')
    entry1.delete(0, tk.END)
    entry1.insert(0, df[cols[0]].iloc[current_row])
    entry1.config(state='readonly')
    
    entry2.config(state='normal')
    entry2.delete(0, tk.END)
    entry2.insert(0, cols[1])
    entry2.config(state='readonly')
    
    entry3.config(state='normal')
    entry3.delete(0, tk.END)
    entry3.insert(0, cols[2])
    entry3.config(state='readonly')
    
    # Set the default text of the entry widget
    entry.delete(0, tk.END)
    entry.insert(0, df[cols[0]].iloc[current_row])

def on_prev():
    global current_row, cols, suggest_info, geo_info

    # Decrement the current row
    current_row = max(0, current_row - 1)

    # Get the selected columns and poccessed values
    cols, suggest_info, geo_info = analyse(df[cols[0]].iloc[current_row])
    
    # Update the width of the entry widgets
    # entry1.config(width=len(df[cols[0]].iloc[current_row])*2)
    # entry2.config(width=len(cols[1])*2)
    # entry3.config(width=len(cols[2])*2)

    # Show the previous row of the 3 columns
    entry1.config(state='normal')
    entry1.delete(0, tk.END)
    entry1.insert(0, df[cols[0]].iloc[current_row])
    entry1.config(state='readonly')

    entry2.config(state='normal')
    entry2.delete(0, tk.END)
    entry2.insert(0, cols[1])
    entry2.config(state='readonly')

    entry3.config(state='normal')
    entry3.delete(0, tk.END)
    entry3.insert(0, cols[2])
    entry3.config(state='readonly')
    
    # Set the default text of the entry widget
    entry.delete(0, tk.END)
    entry.insert(0, df[cols[0]].iloc[current_row])

def on_retry():
    global cols, suggest_info, geo_info

    modified_string = entry.get()
    
    # Get the selected columns and poccessed values
    cols, suggest_info, geo_info = analyse(modified_string)

    entry2.config(state='normal')
    entry2.delete(0, tk.END)
    entry2.insert(0, cols[1])
    entry2.config(state='readonly')
    
    entry3.config(state='normal')
    entry3.delete(0, tk.END)
    entry3.insert(0, cols[2])
    entry3.config(state='readonly')


def on_button1():
    global current_row, suggest_info, geo_info, cols
    df.at[current_row, 'suggest_info'] = str(suggest_info)
    df.at[current_row, 'geo_info'] = str(geo_info)
    df.at[current_row, 'final_address'] = cols[1]
    df.at[current_row, 'final_lon'] = suggest_info['location'].split(",")[0]
    df.at[current_row, 'final_lat'] = suggest_info['location'].split(",")[1]
    on_next()

def on_button2():
    global current_row, suggest_info, geo_info, cols
    df.at[current_row, 'suggest_info'] = str(suggest_info)
    df.at[current_row, 'geo_info'] = str(geo_info)
    df.at[current_row, 'final_address'] = cols[2]
    df.at[current_row, 'final_lon'] = geo_info['location'].split(",")[0]
    df.at[current_row, 'final_lat'] = geo_info['location'].split(",")[1]
    on_next()

def on_button3():
    global current_row
    df.at[current_row, 'geo_info'] = "Too imprecise"
    df.at[current_row, 'suggest_info'] = "Too imprecise"
    df.at[current_row, 'final_address'] = "Too imprecise"
    df.at[current_row, 'final_lon'] = "Too imprecise"
    df.at[current_row, 'final_lat'] = "Too imprecise"
    on_next()

def on_export():
    # Ask the user to select a location to save the .csv file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    # Save the DataFrame to a .csv file
    df.to_csv(file_path, index=False)


# Create a menu bar
menu_bar = tk.Menu(root)

# Create a "Start" menu and add it to the menu bar
start_menu = tk.Menu(menu_bar, tearoff=0)
start_menu.add_command(label="Import .csv file", command=on_import)
start_menu.add_command(label="Export .csv file", command=on_export)
menu_bar.add_cascade(label="Start", menu=start_menu)

# Set the menu bar as the root window's menu
root.config(menu=menu_bar)

empty_label = tk.Label(root, text="", bg='#FEFAE0')
empty_label.grid(row=0, column=0, padx=40, pady=30)
# Create a button to import a .csv file
# import_button = tk.Button(root, text="Import .csv file", command=on_import)
# import_button.grid(row=0, column=1, padx=20, pady=30)

# Create entrys to show the first row of the 3 columns
entry1_label = tk.Label(root, text="Original address:")
entry1_label.grid(row=1, column=2, sticky='sw')
entry1 = tk.Entry(root, font=("Microsoft YaHei", 17))
entry1.grid(row=2, column=2, sticky='w')
entry1.config(state='readonly', width=70)

entry2_label = tk.Label(root, text="Suggested address:")
entry2_label.grid(row=4, column=1, sticky='e', padx=20)
entry2 = tk.Entry(root, font=("Microsoft YaHei", 17))
entry2.grid(row=4, column=2, sticky='w')
entry2.config(state='readonly', width=70)

entry3_label = tk.Label(root, text="Geocoded address:")
entry3_label.grid(row=6, column=1, sticky='e', padx=20)
entry3 = tk.Entry(root, font=("Microsoft YaHei", 17))
entry3.grid(row=6, column=2, sticky='w')
entry3.config(state='readonly', width=70)

# Create buttons under each column
button1 = tk.Button(root, text="Suggested address (S)", command=on_button1)
button1.grid(row=4, column=3, sticky='w', padx=20, pady=30)
button2 = tk.Button(root, text="Geocoded address (A)", command=on_button2)
button2.grid(row=6, column=3, sticky='w', padx=20, pady=30)
button3 = tk.Button(root, text="Too imprecise (D)", command=on_button3)
button3.grid(row=2, column=3, sticky='w', padx=20, pady=30)

# Create an entry widget to allow the user to modify a string
tk.Label(root, text='If neither the geocoded address nor the suggested address seems correct:', font=("Microsoft YaHei", 12)).grid(row=7, column=2, pady=30)
entry_label = tk.Label(root, text="Modify string:")
entry_label.grid(row=8, column=1, sticky='e', padx=20)
entry = tk.Entry(root, font=("Microsoft YaHei", 17))
entry.config(width=70, bg='#FAEDCD')
entry.grid(row=8, column=2, sticky='w')

# Create a "Retry" button that calls the on_retry function when clicked
retry_button = tk.Button(root, text="Retry (W)", command=on_retry)
retry_button.grid(row=8, column=3, sticky='w', padx=20, pady=30)

# Create a "Previous" button that calls the on_prev function when clicked
prev_button = tk.Button(root, text="Previous row", command=on_prev)
prev_button.grid(row=2, column=1, sticky='e', padx=20, pady=30)

# Create a button to export a .csv file
# export_button = tk.Button(root, text="Export .csv file", command=on_export)
# export_button.grid(row=0, column=3, padx=20, pady=30)

# Bind keyboard shortcuts to the buttons
root.bind("s", lambda event: button1.invoke())
root.bind("a", lambda event: button2.invoke())
root.bind("d", lambda event: button3.invoke())
root.bind("w", lambda event: retry_button.invoke())

root.mainloop()


