# Ask for name and age 
name = input("Enter your name: ")
age = int(input("Enter your age"))
# Determine age group
if age <= 12:
    group = "child"
elif age <= 19:
    group = "teenager"
elif age <=64:
    group = "adult"
else:
    group = "senior"
# Print (group) 
print(f"Hello {name}, you are a {group}.")