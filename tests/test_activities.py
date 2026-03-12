from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_activity_dictionary(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]
    assert isinstance(body["Chess Club"]["participants"], list)


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"
    starting_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == starting_count + 1


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = quote("Unknown Activity", safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_already_signed_up_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Soccer Team"
    encoded_activity_name = quote(activity_name, safe="")
    email = "liam@mergington.edu"
    starting_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == starting_count - 1


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = quote("Unknown Activity", safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_signed_up(client):
    # Arrange
    activity_name = "Gym Class"
    encoded_activity_name = quote(activity_name, safe="")
    email = "not.signed.up@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"