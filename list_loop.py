favourites = ["Family", "Ai automation", "Music"]
print("my favourite things:")
for item in favourites:
    print(f"- {item}")
# Bonus: add user input
new_item = input("business: ")
favourites.append(new_item)
print("\nUpdated List:")
for item in favourites:
    print(f"- {item}")