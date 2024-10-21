import os

from configparser import ConfigParser as CustomConfigParser

from keys import generate_wireguard_keys

CustomConfigParser.optionxform = staticmethod(lambda option: option)

os.environ["PUID"] = "1000"
os.environ["PGID"] = "1000"
os.environ["TZ"] = "Europe/Moscow"
os.environ["SERVERURL"] = "127.0.0.1"
os.environ["SERVERPORT"] = "51820"
os.environ["PEERS"] = "2"
os.environ["PEERDNS"] = "auto"
os.environ["INTERNAL_SUBNET"] = "10.13.13.0"

class _Interface(object):
    LAST_PEER_ID = 0
    def __init__(self, data: dict):
        self.peer_id = self.LAST_PEER_ID
        self.privatekey = data.get("PrivateKey", "")
        self.listenport = data.get("ListenPort", os.environ.get("SERVERPORT"))

        dns = os.environ.get("INTERNAL_SUBNET").split(".")[:-1] + ["1"]
        self.dns = data.get("dns", ".".join(dns))
        self.address = data.get("Address", ".".join(dns[:-1] + [str(self.peer_id + 1)]))

    def __repr__(self):
        return f"Interface(%s)" % self.__dict__

    def __call__(self):
        return {
            "Address": self.address,
            "PrivateKey": self.privatekey,
            "ListenPort": self.listenport,
            "DNS": self.dns
        }

    @classmethod
    def add_peer(cls) -> int:
        cls.LAST_PEER_ID += 1
        return cls.LAST_PEER_ID

class _Peer(object):
    def __init__(self, data: dict):
        self.publickey = data.get("PublicKey", os.environ.get("PUBLIC_KEY", ""))
        self.presharedkey = data.get("PresharedKey", os.environ.get("PSHARED_KEY", ""))
        self.endpoint = data.get("Endpoint", f'{os.environ.get("SERVERURL")}:{os.environ.get("SERVERPORT")}')
        self.allowedips = data.get("AllowedIPs", "0.0.0.0/0, ::/0")

    def __repr__(self):
        return f"Peer(%s)" % self.__dict__

    def __call__(self):
        return {
            "PublicKey": self.publickey,
            "PresharedKey": self.presharedkey,
            "Endpoint": self.endpoint,
            "AllowedIPs": self.allowedips
        }

class _Config(object):
    def __init__(self, path: str = None):
        self.path = path

        _config = self._parse_config()

        self.peer = _Peer(_config.get("Peer", {}))
        self.interface = _Interface(_config.get("Interface", {}))

        self.interface.add_peer()

    def _get_config(self):
        return {"Peer": self.peer(), "Interface": self.interface()}

    def _parse_config(self) -> dict:
        if self.path is None or not os.path.exists(self.path):
            return {}
        with open(self.path, 'r') as config_file:
            parsed_config = CustomConfigParser()
            parsed_config.read_file(config_file)
        parsed_config_dict = {
            section: dict(parsed_config.items(section))
            for section in parsed_config.sections()
        }
        print(parsed_config_dict)
        return parsed_config_dict

    def __call__(self):
        config_parser = CustomConfigParser()
        config_parser.read_dict(self._get_config())
        with open(self.path, 'w') as config_file:
            config_parser.write(config_file)

    def __repr__(self):
        return f"Config({self._get_config()})"

class Peer(object):
    def __init__(self, peer_id: int, path: str):
        self.id = peer_id
        self.folder_path = path
        self.path = os.path.join(path, f"peer{self.id}", f"peer{self.id}.conf")
        self.config = _Config(self.path)
        self._private_key, self._public_key, self._preshared_key = self._load_keys()

    def to_conf(self):
        peer = ("[Peer]\nPublicKey = {public_key}\n"
                "PresharedKey = {preshared_key}\n"
                "AllowedIPs = {allowed_ips}/32\n")
        return peer.format(
            public_key=self.public_key,
            preshared_key=self.preshared_key,
            allowed_ips=self.config.interface.address
        )

    def _load_keys(self) -> [str, str, str]:
        if not os.path.exists(os.path.join(self.folder_path, f"peer{self.id}")):
            return generate_wireguard_keys()

        public_key_path = os.path.join(self.folder_path, f"peer{self.id}", f"publickey-peer{self.id}")
        with open(public_key_path, 'r') as public_key:
            public_key = public_key.read().strip()
        print(public_key)
        return self.config.interface.privatekey, public_key, self.config.peer.presharedkey

    def __repr__(self):
        return f"peer{self.id}"


    def __hash__(self):
        return hash(self.id)

    @property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value
        self.config.interface.privatekey = value

    @property
    def public_key(self):
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        self._public_key = value

    @property
    def preshared_key(self):
        return self._preshared_key

    @preshared_key.setter
    def preshared_key(self, value):
        self._preshared_key = value
        self.config.peer.presharedkey = value

    def __call__(self):
        os.mkdir(os.path.join(self.folder_path, f"peer{self.config.interface.peer_id}"))

        self.config()
        peer_id = self.config.interface.peer_id

        peer_public_key_path = os.path.join(self.folder_path, f"peer{self.id}", f"publickey-peer{peer_id}")
        peer_private_key_path = os.path.join(self.folder_path, f"peer{self.id}", f"privatekey-peer{peer_id}")
        peer_preshared_key_path = os.path.join(self.folder_path, f"peer{self.id}", f"presharedkey-peer{peer_id}")

        with open(peer_public_key_path, '+w') as public_key_file:
            public_key_file.write(self.public_key)

        with open(peer_private_key_path, '+w') as private_key_file:
            private_key_file.write(self.private_key)

        with open(peer_preshared_key_path, '+w') as preshared_key_file:
            preshared_key_file.write(self.preshared_key)


class ConfigFolder(object):

    SERVER_PUBLIC_KEY: str = ...
    SERVER_PRIVATE_KEY: str = ...

    def __init__(self, path: str):
        self.path = path
        self.peers: set[Peer] = set()

        self._load()
        self._load_server_keys(path)

    def _load(self):
        for folder in os.listdir(self.path):
            if folder.startswith("peer"):
                peer_id = int(folder[4:])
                self.peers.add(Peer(peer_id, self.path))

    def new_peer(self):
        new_peer = Peer(_Interface.add_peer(), self.path)

        new_peer.config.peer.publickey = self.SERVER_PUBLIC_KEY

        self.peers.add(new_peer)
        return new_peer

    @classmethod
    def _load_server_keys(cls, path):
        with open(os.path.join(path, "server", "publickey-server"), 'r') as server_public_key:
            cls.SERVER_PUBLIC_KEY = server_public_key.read().strip()

        with open(os.path.join(path, "server", "privatekey-server"), 'r') as server_private_key:
            cls.SERVER_PRIVATE_KEY = server_private_key.read().strip()

class WG0(ConfigFolder):
    def __init__(self, path: str):
        super().__init__(path)
        self.server_config_path = os.path.join(path, "wg_confs", "wg0.conf")
        self.address = ".".join(os.environ.get("INTERNAL_SUBNET").split(".")[:-1] + ["1"])
        self.listenport = os.environ.get("SERVERPORT")

    def update(self):
        with open(self.server_config_path, 'w') as config_file:
            config_file.write("[Interface]\n")
            config_file.write("Address = %s\n" % self.address)
            config_file.write("ListenPort = %s\n" % self.listenport)
            config_file.write("PrivateKey = %s\n" % self.SERVER_PRIVATE_KEY)
            config_file.write("PostUp = iptables -A FORWARD -i %i -j ACCEPT; "
                              "iptables -A FORWARD -o %i -j ACCEPT; iptables "
                              "-t nat -A POSTROUTING -o eth+ -j MASQUERADE\n")
            config_file.write("PostDown = iptables -D FORWARD -i %i -j ACCEPT; "
                              "iptables -D FORWARD -o %i -j ACCEPT; iptables "
                              "-t nat -D POSTROUTING -o eth+ -j MASQUERADE\n\n")
            for peer in self.peers:
                config_file.write(peer.to_conf())
                config_file.write("\n")

if __name__ == '__main__':
    config = WG0("../config/")
    # print(config.new_peer()())
    config.update()
    # breakpoint()
    # print(config._config)
    # print(config())
    # print(os.path.join("123", "peer1"))
    # print(Peer(1, "../config/")._parce_config())
    # print(inter.dns)
    # print(inter())
    # """
    # """