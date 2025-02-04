
from typing import Optional
from enum import Enum, IntFlag
from pydantic import BaseModel, Field, IPvAnyAddress, model_validator
from ipaddress import IPv4Network, IPv6Network
from pyroute2.netlink.rtnl.ifinfmsg import (
    IFF_UP,
    IFF_BROADCAST,
    IFF_DEBUG,
    IFF_LOOPBACK,
    IFF_POINTOPOINT,
    IFF_NOTRAILERS,
    IFF_RUNNING,
    IFF_NOARP,
    IFF_PROMISC,
    IFF_ALLMULTI,
    IFF_MASTER,
    IFF_SLAVE,
    IFF_MULTICAST,
    IFF_PORTSEL,
    IFF_AUTOMEDIA,
    IFF_DYNAMIC,
    IFF_LOWER_UP,
    IFF_DORMANT,
    IFF_ECHO,
    )
from cyclarity_in_vehicle_sdk.utils.custom_types.enum_by_name import pydantic_enum_by_name


@pydantic_enum_by_name
class EthIfFlags(IntFlag):
    IFF_UP = IFF_UP
    IFF_BROADCAST = IFF_BROADCAST
    IFF_DEBUG = IFF_DEBUG
    IFF_LOOPBACK = IFF_LOOPBACK
    IFF_POINTOPOINT = IFF_POINTOPOINT
    IFF_NOTRAILERS = IFF_NOTRAILERS
    IFF_RUNNING = IFF_RUNNING
    IFF_NOARP = IFF_NOARP
    IFF_PROMISC = IFF_PROMISC
    IFF_ALLMULTI = IFF_ALLMULTI
    IFF_MASTER = IFF_MASTER
    IFF_SLAVE = IFF_SLAVE
    IFF_MULTICAST = IFF_MULTICAST
    IFF_PORTSEL = IFF_PORTSEL
    IFF_AUTOMEDIA = IFF_AUTOMEDIA
    IFF_DYNAMIC = IFF_DYNAMIC
    IFF_LOWER_UP = IFF_LOWER_UP
    IFF_DORMANT = IFF_DORMANT
    IFF_ECHO = IFF_ECHO

    @staticmethod
    def get_flags_from_int(flags: int) -> list:
        ret_flags = []
        for flag in EthIfFlags:
            if flags & flag.value:
                ret_flags.append(flag)

        return ret_flags


class InterfaceState(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def state_from_string(str_state: str):
        if str_state.casefold() == InterfaceState.UP.casefold():
            return InterfaceState.UP
        elif str_state.casefold() == InterfaceState.DOWN.casefold():
            return InterfaceState.DOWN
        else:
            return InterfaceState.UNKNOWN


class IpRoute(BaseModel):
    gateway: Optional[str] = Field(default=None, 
                                   description="Optional parameter the route gateway, none for default gateway")


class CanInterfaceConfiguration(BaseModel):
    channel: str = Field(description="The CAN interface e.g. can0")
    state: InterfaceState = Field(description="The state of the CAN interface - UP/DOWN")
    bitrate: int = Field(description="Bitrate")
    sample_point: float = Field(description="Sample-point")
    cc_len8_dlc: bool = Field(description="cc-len8-dlc flag value")

    def __str__(self):
        return f"CAN channel: {self.channel}, state {self.state.value}, bitrate: {self.bitrate}, sample point: {self.sample_point}, len8-dlc: {self.cc_len8_dlc}"


class IpConfigurationParams(BaseModel):
    interface: str = Field(description="The network interface for the IP to be configured")
    ip: IPvAnyAddress = Field(description="The IP to configure, IPv4/IPv6")
    suffix: int = Field(description="The subnet notation for this IP address")
    route: Optional[IpRoute] = Field(default=None,
                                     description="Optional parameter for setting a route for the IP")

    @model_validator(mode='after')
    def validate_ip_subnet(self):
        ip_subnet = str(self.ip) + '/' + str(self.suffix)
        if self.ip.version == 6:
            IPv6Network(ip_subnet, False)
        else:
            IPv4Network(ip_subnet, False)
        return self
    
    @property
    def cidr_notation(self) -> str:
        return f"{str(self.ip)}/{str(self.suffix)}"
    
    def __str__(self):
        return f"{self.interface} - {self.cidr_notation}"


DEFAULT_ETH_IF_FLAGS = [EthIfFlags.IFF_BROADCAST,
                        EthIfFlags.IFF_MULTICAST,
                        EthIfFlags.IFF_UP,
                        EthIfFlags.IFF_LOWER_UP,
                        EthIfFlags.IFF_RUNNING]


class EthInterfaceParams(BaseModel):
    interface: str = Field(description="The Eth interface to be configured")
    mtu: Optional[int] = Field(default=None, description="MTU (maximum transmission unit)")
    flags: list[EthIfFlags] = Field(default=DEFAULT_ETH_IF_FLAGS, 
                                    description="Flags to apply on the interface")
    state: Optional[InterfaceState] = Field(default=None, description="Interface State to configure")


class EthernetInterfaceConfiguration(BaseModel):
    if_params: EthInterfaceParams
    ip_params: list[IpConfigurationParams]

    def __str__(self):
        return (f"interface: {self.if_params.interface}\n"
                f"MTU: {self.if_params.mtu}, state: {self.if_params.state.value}\n"
                f"Flags: " + ", ".join(flag.name for flag in self.if_params.flags) + "\n"
                f"IPs: " + ", ".join(ip.cidr_notation for ip in self.ip_params)
                )

class WifiDevice(BaseModel):
    ssid: str = Field(description="The SSID of the access point")
    security: str = Field(description="The security access of the access point")
    connected: bool = Field(description="Is the device connected to this access point")

    def __str__(self):
        return f"SSID: {self.ssid}, security: {self.security}, connected: {self.connected}"


class DeviceConfiguration(BaseModel):
    eth_interfaces: list[EthernetInterfaceConfiguration] = []
    can_interfaces: list[CanInterfaceConfiguration] = []
    wifi_devices: dict[str, WifiDevice] = {}

    def __str__(self):
        return (f"Ethernet interfaces:\n"
                +f"\n\n".join(str(eth_if) for eth_if in self.eth_interfaces)
                +f"\nCAN interfaces:\n"
                +f"\n".join(str(can_if) for can_if in self.can_interfaces)
                +f"\nWifi devices:\n"
                +f"\n".join(str(wifi_dev) for wifi_dev in self.wifi_devices.values())
                )
