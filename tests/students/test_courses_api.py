import pytest
from django.urls import reverse
from students.filters import CourseFilter


@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id


@pytest.mark.django_db
def test_retrieve_courses_list(client, course_factory):
    courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_courses_list_filter_by_id(client, course_factory):
    courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    expected_result = CourseFilter(data={'id': courses[0].id})
    response = client.get(url, data={'id': courses[0].id})
    assert response.status_code == 200
    assert response.data[0]['id'] == expected_result.data['id']


@pytest.mark.django_db
def test_courses_list_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    expected_result = CourseFilter(data={'name': courses[0].name})
    response = client.get(url, data={'name': courses[0].name})
    assert response.status_code == 200
    assert response.data[0]['name'] == expected_result.data['name']


@pytest.mark.django_db
def test_create_course(client):
    course = {'name': 'Python-разработчик'}
    url = reverse('courses-list')
    response = client.post(url, course)
    assert response.status_code == 201
    assert response.data['name'] == course['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    update_data = {'name': 'Java-разработчик'}
    url = reverse('courses-detail', args=(course.id, ))
    response = client.put(url, update_data)
    assert response.status_code == 200
    assert response.data['name'] == update_data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id, ))
    response = client.delete(url)
    assert response.status_code == 204
    assert response.data is None


@pytest.mark.parametrize(
    ['num_students', 'status'],
    (
        (10, 201),
        (21, 400)
    )
)
@pytest.mark.django_db
def test_limit_students(client, student_factory, settings, num_students, status):
    settings.MAX_STUDENTS_PER_COURSE = 20
    students = student_factory(_quantity=num_students)
    student_ids = [student.id for student in students]
    course = {'name': 'Python-разработчик', 'students': student_ids}
    url = reverse('courses-list')
    response = client.post(url, course)
    assert response.status_code == status
    assert settings.MAX_STUDENTS_PER_COURSE


