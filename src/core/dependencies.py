from src.core.roles import UserRole
from src.core.security import get_current_user


require_admin = get_current_user(required_roles=[UserRole.ADMIN])
require_user = get_current_user()
