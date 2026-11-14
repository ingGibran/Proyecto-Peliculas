from pwdlib import PasswordHash
from pwdlib.exceptions import PwdlibError


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Create a one-way Argon2 password hash."""
    if not password:
        raise ValueError("Password cannot be empty.")
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Safely compare a plaintext password with a stored hash."""
    if not password or not hashed_password:
        return False
    try:
        return password_hash.verify(password, hashed_password)
    except PwdlibError:
        return False


def needs_password_rehash(hashed_password: str) -> bool:
    """Report whether a stored hash uses outdated hashing parameters."""
    if not hashed_password:
        return True
    return password_hash.current_hasher.check_needs_rehash(hashed_password)