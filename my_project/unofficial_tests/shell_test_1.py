# Import the necessary models
from courses.models import Course, CourseStatus
from uni_prof.models import University, Professor
from reviews.models import Review, ReviewStatus
from users.models import ExtendedUser
from django.contrib.auth.models import User

# Create a default user instance
default_user = User.objects.create(username='new_unique_user', password='password123')

# Create an extended user instance
ext_user = ExtendedUser.objects.create(user=default_user, public_username='test_user')

# Create a university instance
uni = University.objects.create(uni_name='Complex University')

# Create professor instances
prof1 = Professor.objects.create(first_name='Alice', last_name='Johnson')
prof2 = Professor.objects.create(first_name='Bob', last_name='Smith')

# Link professors to the university
prof1.universities.add(uni)
prof2.universities.add(uni)

# Create courses and associate with the university and professors
course_cs = Course.objects.create(course_name='Advanced CS', university=uni, course_status=CourseStatus.OK)
course_math = Course.objects.create(course_name='Mathematics', university=uni, course_status=CourseStatus.UNDER_REVIEW)

course_cs.professors.add(prof1)
course_math.professors.add(prof2)

# Create review instances for courses
review1 = Review.objects.create(
    title='Great Course',
    body='I learned a lot!',
    rating_left=5,
    user=ext_user,
    course=course_cs,
    review_status=ReviewStatus.PASSED_REVIEW
)

review2 = Review.objects.create(
    title='Challenging but Rewarding',
    body='Tough course but worth it.',
    rating_left=4,
    user=ext_user,
    course=course_math,
    review_status=ReviewStatus.UNDER_REVIEW
)

# Print and verify the associations
print(f"University: {uni.uni_name}")
print(f"Professors at {uni.uni_name}: {[prof.first_name + ' ' + prof.last_name for prof in uni.professors.all()]}")
print(f"Courses at {uni.uni_name}: {[course.course_name for course in uni.courses.all()]}")
print(f"Professors for course 'Advanced CS': {[prof.first_name for prof in course_cs.professors.all()]}")
print(f"Professors for course 'Mathematics': {[prof.first_name for prof in course_math.professors.all()]}")
print(f"Reviews for course 'Advanced CS': {[review.title for review in course_cs.reviews.all()]}")
print(f"Reviews for course 'Mathematics': {[review.title for review in course_math.reviews.all()]}")

# Verify data
courses = Course.objects.all()
for course in courses:
    print(f"Course: {course.course_name}, Status: {course.course_status}")

reviews = Review.objects.filter(course=course_cs)
for review in reviews:
    print(f"Review: {review.title}, Rating: {review.rating_left}")

professors = University.objects.get(uni_name='Complex University').professors.all()
for prof in professors:
    print(f"Professor: {prof.first_name} {prof.last_name}")


# Delete all records from models
Course.objects.all().delete()
Review.objects.all().delete()
ExtendedUser.objects.all().delete()
User.objects.all().delete()
University.objects.all().delete()
Professor.objects.all().delete()
