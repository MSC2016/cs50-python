persons = []

with open ('data.csv') as file:
    for line in file:
        Name,Department,Age,Salary = line.rstrip().split(',')
        person_data = {'Name': Name, 'Department': Department, 'Age': Age, 'Salary': Salary}
        persons.append(person_data)

for person in sorted(persons, key=lambda p: p['Name']):
    print(person)