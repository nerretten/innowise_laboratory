def generate_profile(age):
    if age >= 0 and age <= 12:
        return 'Child'
    elif age >= 13 and age <= 19:
        return 'Teenager'
    elif age >= 20:
        return 'Adult'

user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_age = 2025 - birth_year
hobbies = []
while True:
    hobby_input = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby_input.lower() == 'stop':
        break
    hobbies.append(hobby_input)
life_stage = generate_profile(current_age)
user_profile = {
    'name': user_name,
    'age': current_age,
    'stage': life_stage,
    'hobbies': hobbies
}
print('---\nProfile Summary:')
print(f'Name: {user_profile["name"]}\nAge: {user_profile["age"]}\nLife Stage: {user_profile["stage"]}')
if len(user_profile['hobbies']) == 0:
    print("You didn't mention any hobbies.\n---")
else:
    print(f"Favorite Hobbies ({len(user_profile['hobbies'])}):")
    for hobby in user_profile['hobbies']:
        print(f'- {hobby}')
    print('---')