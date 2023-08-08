import random

user_number = 0

number = random.randrange(1,10)

print(number)

while user_number != number :

    user_number = int(input("Number: "))

    if user_number > number :

        print("Too high.")

    elif user_number < number :

        print("Too low.")

else :

    print(f"Number is {number}.")
