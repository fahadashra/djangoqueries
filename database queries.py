
from django.db import models

class Author(models.Model):
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)
  address = models.CharField(max_length=200, null=True)
  zipcode = models.IntegerField(null=True)
  telephone = models.CharField(max_length=100, null=True)
  recommendedby = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='recommended_authors', related_query_name='recommended_authors', null=True)
  joindate = models.DateField()
  popularity_score = models.IntegerField()
  followers = models.ManyToManyField('User', related_name='followed_authors', related_query_name='followed_authors')
  def __str__(self):
    return self.firstname + ' ' + self.lastname

class Books(models.Model):
  title = models.CharField(max_length=100)
  genre = models.CharField(max_length=200)
  price = models.IntegerField(null=True)
  published_date = models.DateField()
  author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books', related_query_name='books')
  publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, related_name='books', related_query_name='books')
  def __str__(self):
    return self.title

class Publisher(models.Model):
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)
  recommendedby = models.ForeignKey('Publisher', on_delete=models.CASCADE, null=True)
   joindate = models.DateField()
  popularity_score = models.IntegerField()
  def __str__(self):
    return self.firstname + ' ' + self.lastname

class User(models.Model):
  username = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  def __str__(self):
    return self.username
Exercises:
1.Write a Query using Django ORM to fetch all the books objects from your database.
2.Write a Query using Django ORM to fetch title and published_date of all books from the database.
3.Fetch first name and last name of all the new authors ( Authors with popularity_score = 0 are new authors ).
4.Fetch first name and popularity score of all authors whose first name starts with A and popularity score is greater than or equal to 8.
5.Fetch first name of all the authors with aa case insensitive in their first name.
6.Fetch list of all the authors whose ids are in the list = [1, 3, 23, 43, 134, 25].
7.Fetch list of all the publishers who joined after or in September 2012, output list should only contain first name and join date of publisher. Order by join date.
8.Fetch ordered list of first 10 last names of Publishers, list must not contain duplicates.
9.Get the signup date for the last joined Author and Publisher.
10.Get the first name, last name and join date of the last author who joined.
11.Fetch list of all authors who joined after or in year 2013
12.Fetch total price of all the books written by authors with popularity score 7 or higher.
13.Fetch list of titles of all books written by authors whose first name starts with ‘A’. The result should contain a list of the titles of every book. Not a list of tuples.
14.Get total price of all the books written by author with pk in list [1, 3, 4]
15.Produce a list of all the authors along with their recommender.
16.Produce list of all authors who published their book by publisher pk = 1, output list should be ordered by first name.
17.Create three new users and add in the followers of the author with pk = 1.
18.Set the followers list of the author with pk = 2, with only one user.
19.Add new users in followers of the author with pk = 1.
20.Remove one user from the followers of the author with pk = 1.
21.Get first names of all the authors, whose user with pk = 1 is following. ( Without Accessing Author.objects manager )
22.Fetch list of all authors who wrote a book with “tle” as part of Book Title.
23.Fetch the list of authors whose names start with ‘A’ case insensitive, and either their popularity score is greater than 5 or they have joined after 2014. with Q objects.
24.Retrieve a specific object with primary key= 1 from the Author table.
25.Retrieve the first N=10 records from an Author table.
26Retrieve records from a table that match this condition, popularity score = 7. And get the first and last record of that list.
27.Retrieve all authors who joined after or in the year 2012, popularity score greater than or equal to 4, join date after or with date 12, and first name starts with ‘a’ (case insensitive) without using Q objects.
28.Retrieve all authors who did not join in 2012.
29.Retrieve Oldest author, Newest author, Average popularity score of authors, sum of price of all books in database.
30.Retrieve all authors who have no recommender, recommended by field is null.
Retrieve the books that do not have any authors, where the author is null. Also, retrieve the books whose authors are present, but do not have a recommender, where the author is not null and the author’s recommender is null. (Note that if the condition for the author not being null is not specified and only the condition for the recommender being null is mentioned, all books with both author null and author’s recommender null will be retrieved.)
32.Total price of books written by author with primary key = 1. ( Aggregation over related model ), oldest book written by author with pk = 1, latest book written by author with pk = 1.
33.Among the publishers in the Publishers table what is the oldest book any publisher has published.
34.Average price of all the books in the database.
35.Maximum popularity score of publisher among all the publishers who published a book for the author with pk = 1. (Reverse Foreign Key hop)
Count the number of authors who have written a book which contains the phrase ‘ab’ case insensitive.
Get all the authors with followers more than 216.
Get average popularity score of all the authors who joined after 20 September 2014.
Generate a list of books whose author has written more than 10 books.
Get the list of books with duplicate titles.
Note: Combining multiple aggregations with annotation will yield the wrong results because joins are used instead of subqueries. For most aggregates there is no way to avoid this problem. Count aggregate has distinct parameter that may help. Consider inspecting the query property of the QuerySet object. ( Taken from docs of django as key information )

Solutions:

from main.models import *
import datetime
from django.db.models import Count, Avg, Sum, Max, Min
from django.db.models import Q, F
ans1 = Books.objects.all()
ans2 = Books.objects.all().values_list('title', 'published_date')
ans3 = Authors.objects.all().filter(popularity_score=0).values_list('firstname', 'lastname')
ans4 = Authors.objects.all().filter(firstname__startswith='a', popularity_score__gte=8).values_list('firstname', 'popularity_score')
ans5 = Authors.objects.all().filter(firstname__icontains='aa').values_list('firstname')
ans6 = Authors.objects.all().filter(pk__in=[1, 3, 23, 43, 134, 25])
ans7 = Authors.objects.all().filter(joindate__gte=datetime.date(year=2012, month=9, day=1)).order_by('joindate').values_list('firstname', 'joindate')
ans8 = Publishers.objects.all().order_by('lastname').values_list('lastname').distinct()[:10]
ans9 = [Authors.objects.all().order_by('joindate').last(),
Publishers.objects.all().order_by('-joindate').first()]
ans10 = Authors.objects.all().order_by('-joindate').values_list('firstname', 'lastname', 'joindate').first()
ans11 = Authors.objects.all().filter(joindate__year__gte=2013)
ans12 = Books.objects.all().filter(author__popularity_score__gte=7).aggregate(total_book_price=Sum('price'))
ans13 = Books.objects.all().filter(author__firstname__contains='a').values_list('title', flat=True)
ans14 = Books.objects.all().filter(author__pk__in=[1, 3, 4]).aggregate('price')
ans15 = Authors.objects.all().values_list('firstname', 'recommendedby__firstname')
ans16 = Authors.objects.all().filter(books__publisher__pk=1)
user1 = Users.objects.create(username='user1', email='user1@test.com')
user2 = Users.objects.create(username='user2', email='user2@test.com')
user3 = Users.objects.create(username='user3', email='user3@test.com')
ans17 = Authors.objects.get(pk=1).followers.add(user1, user2, user3)
ans18 = Authors.objects.get(pk=2).followers.set(user1)
ans19 = Authors.objects.get(pk=1).followers.add(user1)
ans20 = Authors.objects.get(pk=1).followers.remove(user1)
ans21 = Users.objects.get(pk=1).followed_authors.all().values_list('firstname', flat=True)
ans22 = Authors.objects.all().filter(books__title__icontains='tle')
ans23 = Authors.objects.all().filter(Q(firstname__istartswith='a') and ( Q(popularity_score__gt=5) or Q(joindate__year__gt=2014)))
ans24 = Authors.objects.all().get(pk=1)
ans25 = Authors.objects.all()[:10]
qs = Authors.objects.all().filter(popularity_scre=7)
author1 = qs.first()
author2 = qs.last()
ans26 = [author1, author2]
ans27 = Authors.objects.all().filter(joindate__year__gte=2012, popularity_score__gte=4, joindate__day__gte=12, firstame__istartswith='a')
ans28 = Authors.objects.all().exclude(joindate__year=2012)
oldest_author = Authors.objects.all().aggregate(Min('joindate'))
newest_author = Authors.objects.all().aggregate(Max('joindate'))
avg_pop_score = Authors.objects.all().aggregate(Avg('popularity_score'))
sum_price = Books.objects.all().aggregate(Sum('price'))
ans29 = [oldest_author, newest_author, avg_pop_score, sum_price]
ans30 = Authors.objects.all().filter(recommendedby__isnull=True)
one = Books.objects.all().filter(author__isnull=False)
two = Books.objects.all().filter(author__isnull=False, author__recommender__isnull=True)
ans31 = [one, two]
ans32 = Books.objects.all().filter(author__pk=1).aggregate(Sum('price'))
ans33 = Books.objects.all().order_by('published_date').last().title
ans34 = Books.objects.all().aggregate(Avg('price'))
ans35 = Publishers.objects.filter(books__author__pk=1).aggregate(Max('popularity_score'))
ans36 = Authors.objects.filter(books__title__icontains='ab').count()
ans37 = Authors.objects.annotate(f_count=Count('followers')).filter(f_count__gt=216)
ans38 = Authors.objects.filter(joindate__gt=datetime.date(year=2014, month=9, day=20)).aggregate(Avg('popularity_score'))
ans39 = Books.objects.all().annotate(bk_count=Count('author__books')).filter(bk_count__gt=10).distinct()
ans40 = Books.objects.all().annotate(count_title=Count('title')).filter(count_titl















for find duplicates
    duplicates = User.objects.values().annotate(name_count=Count('first_name')).filter(name_count__gt=1)


for complex queries we use Q
from django.db.models import Q
 queryset = User.objects.filter(Q(first_name__startswith='R') | Q(last_name__startswith='D')

we can also write above query like this
queryset = User.objects.filter(Q(first_name__startswith='R') & Q(last_name__startswith='D')


In [1]: from django.db.models import Max
In [2]: from entities.models import Category
In [3]: import random
In [4]: def get_random2():
   ...:     max_id = Category.objects.all().aggregate(max_id=Max("id"))['max_id']
   ...:     pk = random.randint(1, max_id)
   ...:     return Category.objects.get(pk=pk)


There are conditions when we want to save multiple objects in one go. Say we want to add multiple categories at once and we don’t want to make many queries to the database. We can use bulk_create for creating multiple objects in one shot.
Category.objects.bulk_create(
    [Category(name="God"),
     Category(name="Demi God"),
     Category(name="Mortal")]
)


4. How to order on a field from a related model (with a foreign key)?
Hero.objects.all().order_by(
    'category__name', 'name'
)

5. How to order on an annotated field?
class Category(models.Model):
    name = models.CharField(max_length=100)


class Hero(models.Model):
    # ...
    name = models.CharField(max_length=100)
Category.objects.annotate(hero_count=Count("hero")).order_by("-hero_count")

8. How to filter a queryset with criteria based on comparing their field values
User.objects.filter(first_name__startswith='R')

Now you can find the users where first_name==last_name
User.objects.filter(last_name=F("first_name"))


10. How to perform join operations in django ORM?
a2 = Article.objects.filter(reporter__username='John')



11. Find rows which have duplicate field values
duplicates = User.objects.values('first_name').annotate(name_count=Count('first_name')).filter(name_count__gt=1)

13. How to find distinct field values from queryset?
distinct = User.objects.values('first_name').annotate(name_count=Count('first_name')).filter(name_count=1)



14.bulk create
Category.objects.bulk_create(
    [Category(name="God"),
     Category(name="Demi God"),
     Category(name="Mortal")]
)



15. How to model many to many relationships?
A many-to-many relationship refers to a relationship between tables in a database when a parent row in one table contains several child rows in the second table, and vice versa.
ically have 3 basic things in Twitter, tweets, followers, favourite/unfavourite.

We have two models to make everything work. We are inheriting django’s auth_user.:

class User(AbstractUser):
    tweet = models.ManyToManyField(Tweet, blank=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    pass

class Tweet(models.Model):
    tweet = models.TextField()
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favourite')

    def __unicode__(self):
        return self.tweet

What will the above model be able to do ?

1) User will able to follow/unfollow other users.
2) User will able to see tweets made by other users whom user is following.
3) User is able to favorite/unfavorite tweets.




How to join two models in django-rest-framework



class LevelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Level
        fields = ('__all__')

class LevelProcessSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)

    class Meta:
        model = LevelProcess
        fields = ('__all__')

changes
views.py


class ViewLevelProcessViewSet(viewsets.ModelViewSet):
    processes = LevelProcess.objects.all()
    serializer_class = LevelProcessSerializer(processes, many=True)


aggregation and annotation

aggregating and annotating objects refers to summing up or putting together the values. Annotation of an object creates a separate summary for each object in a queryset. Aggregation of an object is to generate summary values over an entire QuerySet.