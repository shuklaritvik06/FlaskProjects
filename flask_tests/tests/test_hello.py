from flask import session


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About Page" in response.data


def test_contact(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"Contact Us" in response.data


def test_invalid_route(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_request_example(client):
    response = client.get("/posts")
    assert b"<h2>Hello, World!</h2>" in response.data


def test_json_data(client):
    response = client.post(
        "/graphql",
        json={
            "query": """
            query User($id: String!) {
                user(id: $id) {
                    name
                    theme
                    picture_url
                }
            }
        """,
            "variables": {"id": 2},
        },
    )
    assert response.json["data"]["user"]["name"] == "Flask"


def test_logout_redirect(client):
    response = client.get("/logout", follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/index"


def test_access_session(client):
    with client:
        client.post("/auth/login", data={"username": "flask"})
        assert session["user_id"] == 1


def test_modify_session(client):
    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get("/users/me")
    assert response.json["username"] == "flask"


def test_hello_command(runner):
    result = runner.invoke(args="hello")
    assert "World" in result.output

    result = runner.invoke(args=["hello", "--name", "Flask"])
    assert "Flask" in result.output
