# Column	Type	Description
# user_id	string	Unique user identifier (abc123)
# region	string	User's geographic region(us, eu, cn)
# tier	string	User subscription tier (free, pro)

from dataclasses import dataclass

@dataclass
class User:
    user_id: str  # Unique user identifier (abc123)
    region: str   # User's geographic region (us, eu, cn)
    tier: str     # User subscription tier (free, pro)


