from secretscanner.detectors import DETECTORS, mask_value


def match_any(text: str) -> bool:
    return any(d.pattern.search(text) for d in DETECTORS)


def test_aws_access_key_detected():
    assert match_any("aws_key = AKIAABCDEFGHIJKLMNOP")


def test_github_token_detected():
    assert match_any("token = ghp_1234567890abcdefghij1234567890abcd")


def test_openai_key_detected():
    assert match_any("OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz1234567890")


def test_jwt_detected():
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dQw4w9WgXcQ"
    assert match_any(token)


def test_private_key_block_detected():
    assert match_any("-----BEGIN RSA PRIVATE KEY-----")


def test_generic_secret_assignment_detected():
    assert match_any('PASSWORD="SuperSecret123"')


def test_plain_text_not_flagged():
    assert not match_any("this is just a regular sentence with no secrets")


def test_mask_value_keeps_only_prefix():
    masked = mask_value("AKIAABCDEFGHIJKLMNOP")
    assert masked.startswith("AKIA")
    assert masked.endswith("*")
    assert "ABCDEFGHIJKLMNOP" not in masked
