name = input("Enter your name: ")
color = input("Enter your favourite color: ")
# Write to file
with open("user_data.txt", "w") as file:
    file.write(f"Name: {"name"}\n")
    file.write(f"favourite color {"color"}\n" )
# Read from file
print("\nData saved in file:")
with open("user_data.txt", "r") as file:
    content = file.read()
    print(content)