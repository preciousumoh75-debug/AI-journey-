contacts = {}
def add_contacts(name, phone):
    contacts[name] = phone
    print(f"added {name}")
def show_contacts():
    if not contacts:
        print("no contacts yet.")
    else:    
        print("Contacts:")
        for name, phone in contacts.items(): 
            print(f"{name}: {phone}")
# Examples usage
add_contacts("Precious", "09133925016")
add_contacts("Deepseek", "Ai@example.com")
show_contacts()