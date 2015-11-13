import json

class SlackUser:

    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.verifyUserData(self.userData)

        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']

    @staticmethod
    def verifyUserData(userData):
        if "ok" in userData and userData["ok"] == False:
            if "error" in userData:
                if userData["error"] == "user_not_found":
                    raise ValueError()
                else:
                    raise RuntimeError(userData["error"])
            else:
                raise RuntimeError("Unknown error from Slack server")