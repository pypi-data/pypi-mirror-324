class UserData:
    def __init__(self, payload: dict):
        self.user_id = payload.get("user_id")
        self.email = payload.get("email")
        self.full_name = payload.get("full_name")
        self.subscription_id = payload.get("subscription_id")
        self.language = payload.get("language")
        self.roleName = payload.get("roleName")
        self.action_ids = payload.get("action_ids")
        self.permission_ids = payload.get("permission_ids")
        for key, value in payload.items():
            setattr(self, key, value)

    def __repr__(self):
        return (f"<UserData(user_id={self.user_id}, "
                f"email={self.email}, "
                f"full_name={self.full_name}, "
                f"subscription_id={self.subscription_id}, "
                f"language={self.language}, "
                f"roleName={self.roleName}, "
                f"action_ids={self.action_ids}, "
                f"permission_ids={self.permission_ids})>"
                )