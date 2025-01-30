from .tennant import TennantMethod
from .lowflow import LowFlowQ90
from .fdc import FlowDurationCurve
from .gefc import GEFCMethod
from .sevenq10 import SevenQ10Method

# Define what is available when users import from eflowpy.hydrological
__all__ = ["TennantMethod", "LowFlowQ90", "FlowDurationCurve", "GEFCMethod", "SevenQ10Method"]
