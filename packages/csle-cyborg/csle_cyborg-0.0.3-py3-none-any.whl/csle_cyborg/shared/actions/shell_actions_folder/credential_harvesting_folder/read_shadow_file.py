# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.actions.shell_actions_folder.credential_harvesting_folder.credential_harvesting import CredentialHarvesting
from csle_cyborg.shared.enums import OperatingSystemType, Path
from csle_cyborg.shared.observation import Observation


class ReadShadowFile(CredentialHarvesting):
    def __init__(self, session, agent):
        super().__init__(session, agent)

    def sim_execute(self, state):
        obs = Observation()
        obs.set_success(False)
        if self.session not in state.sessions[self.agent]:
            return obs
        session = state.sessions[self.agent][self.session]

        if not session.active:
            return obs

        if session.host.os_type == OperatingSystemType.WINDOWS:
            obs.add_system_info(hostid="0", os_type="windows")
        elif session.host.os_type == OperatingSystemType.LINUX:
            obs.add_system_info(hostid="0", os_type="linux")
            shadow_file = None
            for file in session.host.files:
                if file.name == "shadow" and Path.parse_string(file.path) == Path.ETC:
                    shadow_file = file
                    break
            if shadow_file is not None and shadow_file.check_readable(session.user):
                obs.set_success(True)
                for user in session.host.users:
                    obs.add_user_info(hostid="0", password_hash=user.password_hash,
                                      password_hash_type=user.password_hash_type,
                                      username=user.username)
        return obs
