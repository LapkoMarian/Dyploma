from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models, connection
from classroom.models import ClassroomUsers


class Rating(models.IntegerChoices):
    dont_visited = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11
    twelve = 12
    dont_rating = 13


class Journal(models.Model):
    rating = models.IntegerField(choices=Rating.choices)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateField(default=timezone.now)
    classroom_user = models.ForeignKey(ClassroomUsers, on_delete=models.CASCADE)
    topik = models.CharField(max_length=200)

    class Meta:
        unique_together = ('classroom_user', 'created_at')

    @staticmethod
    def get_rating(student_id: int):
        with connection.cursor() as cursor:
            sql_query = f"""
                SELECT j.id , j.rating, j.created_at, j.topik, t.last_name ||' '||t.first_name as teacher, classroom.name
                FROM journal_journal as j
                INNER JOIN auth_user as t
                    ON t.id = j.created_by_id
                INNER JOIN classroom_classroom_users as classroom_users
                    ON classroom_users.id = j.classroom_user_id
                INNER JOIN auth_user as student
                    ON student.id = classroom_users.user_id
                INNER JOIN classroom_classroom as classroom
                    ON classroom.id = classroom_users.classroom_id
                WHERE student.id = {student_id}
            """
            cursor.execute(sql_query)
            results = Journal.dict_fetchall(cursor)
        return results

    def __str__(self):
        return f'{self.classroom_user} -> {self.topik}'

    @staticmethod
    def dict_fetchall(cursor):
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return results
