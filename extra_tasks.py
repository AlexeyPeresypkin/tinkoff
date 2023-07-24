"""Составь запрос (к таблице users), который считает количество пользователей, рождённых (поле birthday) в каждом году (из тех,
что есть в birthday) по следующим правилам:
 - анализируются только те пользователи, у которых указан год рождения
 - выборка отсортирована по году рождения в прямом порядке"""
"""
select extract(year from birthday) as birth_year, count(*)
from users u
where birthday is not null
group by birth_year
order by birth_year;
"""

"""Составь запрос, который извлекает из базы идентификатор топика и имя автора топика (first_name) по следующим правилам:
 - анализируются топики только тех пользователей, чей емейл находится на домене lannister.com 
 - выборка отсортирована по дате создания топика в прямом порядке"""

"""
select t.id, u.first_name
from topics t
         join users u on t.user_id = u.id
where u.email like '%@lannister.com'
order by t.created_at;
"""

"""Реализовать класс, объекты которого будут соответствовать следующим условиям:
• Наличие более двух полей
• В случае, если у двух объектов одинаковые значения двух полей, объекты равны (проверка через if foo == bar)"""


class FirstObj:
    def __init__(self, attr_1, attr_2, attr_3, attr_4):
        self.attr_1 = attr_1
        self.attr_2 = attr_2
        self.attr_3 = attr_3
        self.attr_4 = attr_4

    def __eq__(self, other):
        count = 0
        other_values = list(other.__dict__.values())
        for attr_value in self.__dict__.values():
            if attr_value in other_values:
                other_values.remove(attr_value)
                count += 1
            if count == 2:
                return True
        return False
