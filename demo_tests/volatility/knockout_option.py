from dataclasses import dataclass
from turing_models.instruments.knockout_option import KnockOutOption
from turing_models.utilities import to_string


@dataclass(repr=False, eq=False, order=False, unsafe_hash=True)
class EqKnockOutOption(KnockOutOption):

    def price(self) -> float:
        print("Hello World")
        v = super().price()
        return v

    def __repr__(self):
        s = super().__repr__()
        s += to_string("Barrier", self.barrier)
        s += to_string("Rebate", self.rebate)
        s += to_string("Knock Out Type", self.knock_out_type)
        return s
