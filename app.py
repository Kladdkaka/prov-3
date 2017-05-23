import requests
import datetime
from enum import Enum


class NameOrder(Enum):
    FIRST_THEN_LAST = 0
    LAST_THE_FIRST = 1


class PersonLista:

    def __init__(self, personer=[]):
        self.personer = personer

    def load(self):
        self.personer = self.get_data()
        self.save_data('politiker.txt')
        self.personer = self.open_data('politiker.txt')

    def get_data(self):
        r = requests.get('http://data.riksdagen.se/personlista/?iid=&fnamn=&enamn=&f_ar=&kn=&parti=&valkrets=&rdlstatus=tjanst&org=&utformat=json&termlista=')
        data = r.json()

        people = []

        for person in data['personlista']['person']:
            firstname = person['tilltalsnamn']
            lastname = person['efternamn']
            age = get_current_year() - int(person['fodd_ar'])

            people.append(self.Person(firstname, lastname, age))
        return people

    def save_data(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for person in self.personer:
                f.write('{0},{1},{2}\n'.format(person.firstname, person.lastname, person.age))

    def open_data(self, filename):
        people = []
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            for line in lines:
                p = line.split(',')
                if len(p) > 1:
                    people.append(self.Person(p[0], p[1], int(p[2])))
        return people

    def sort_by_age(self):
        for x in range(len(self.personer)):
            for y in range(len(self.personer) - 1 - x):
                if self.personer[y].age > self.personer[y + 1].age:
                    temp = self.personer[y]
                    self.personer[y] = self.personer[y + 1]
                    self.personer[y + 1] = temp

    def sort_alphabetically(self, order=NameOrder.FIRST_THEN_LAST):
        for x in range(len(self.personer)):
            for y in range(len(self.personer) - 1 - x):
                if (self.personer[y].full_name(order)) > (self.personer[y + 1].full_name(order)):
                    temp = self.personer[y]
                    self.personer[y] = self.personer[y + 1]
                    self.personer[y + 1] = temp

    def search(self, word):
        a = lambda x: word.lower() in (x.full_name()).lower()

        return PersonLista(list(filter(a, self.personer)))

    def __iter__(self):
        for x in self.personer:
            yield x

    def __getitem__(self, item):
        return self.personer[item]

    def __len__(self):
        return len(self.personer)

    def __str__(self):
        return '\n'.join([str(x) for x in self.personer])

    class Person:
        def __init__(self, firstname, lastname, age):
            self.firstname = firstname
            self.lastname = lastname
            self.age = age

        def full_name(self, order=NameOrder.FIRST_THEN_LAST):
            if order == NameOrder.FIRST_THEN_LAST:
                return '{0} {1} {2}'.format(self.firstname, self.lastname, self.age)
            else:
                return '{0} {1} {2}'.format(self.lastname, self.firstname, self.age)

        def __str__(self):
            return '{0} {1} {2}'.format(self.firstname, self.lastname, self.age)


def get_current_year():
    return datetime.datetime.now().year


personer = PersonLista()
personer.load()

print('[Rådata]')
print(personer)
print()

personer.sort_alphabetically()

print('[Sorterat Alfabetiskt Förnamn]')
print(personer)
print()

personer.sort_alphabetically(NameOrder.LAST_THE_FIRST)

print('[Sorterat Alfabetiskt Efternamn]')
print(personer)
print()

personer.sort_by_age()

print('[Sorterat Nummeriskt]')
print(personer)
print()

while True:
    namn = input('Vem vill du söka efter (skriv inget för att avsluta): ')

    if namn == "":
        break

    print('[Sök]')
    print(personer.search(namn))