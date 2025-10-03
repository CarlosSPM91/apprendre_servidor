

from src.domain.objects.token.jwtPayload import JwtPayload


def test_Jwt():
    jwt = JwtPayload(
        user_id=1,
        username="jo",
        name="await",
        last_name="async",
        role = 2
    )
    assert jwt.user_id == 1
    assert jwt.username == "jo"
    assert jwt.name == "await"
    assert jwt.last_name == "async"
    assert jwt.role == 2
    