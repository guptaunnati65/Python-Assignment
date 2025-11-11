print('Welcome to Daily Calorie Tracker :) !!')
print('This tool helps you to keep track of your daily total calories and compares it with your limit.\n')

n = int(input('Enter the number of meals: '))
limit = float(input('Enter the calorie limit: '))

meal = []
calorie = []

for i in range(n):
    mn = input(f'Enter the name of meal {i+1}: ')
    ca = float(input(f'Enter the calorie amount for {mn}: '))
    meal.append(mn)
    calorie.append(ca)

total_cal_in = sum(calorie)
average_cal_per = total_cal_in / n

if total_cal_in > limit:
    result = '!! Calorie intake greater than daily limit !!'
else:
    result = 'Congrats!! Calorie within daily limit!'

print('\n----------- DAILY SUMMARY REPORT -----------\n')
print(f'{"Meal Name":<20} {"Calories"}')
print('--------------------------------------------')

for i in range(len(meal)):
    print(f'{meal[i]:<20} {calorie[i]}')

print('--------------------------------------------')
print(f'Total:    {total_cal_in}')
print(f'Average:  {average_cal_per:.2f}')
print(f'Status:   {result}')