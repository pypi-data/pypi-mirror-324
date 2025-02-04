from ipaddress import IPv4Address
from csle_cyborg.shared.observation import Observation
from csle_cyborg.shared.actions.concrete_actions.exploit_action import ExploitAction
from csle_cyborg.simulator.host import Host
from csle_cyborg.simulator.process import Process
from csle_cyborg.simulator.state import State


class HTTPSRFI(ExploitAction):
    def __init__(self, session: int, agent: str, ip_address: IPv4Address, target_session: int):
        super().__init__(session, agent, ip_address, target_session)

    def sim_execute(self, state: State) -> Observation:
        return self.sim_exploit(state, 443, 'webserver')

    def test_exploit_works(self, target_host: Host, vuln_proc: Process):
        # check if OS and process information is correct for exploit to work
        return "rfi" in vuln_proc.properties
