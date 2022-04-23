from cryptosploit.cprint import Printer
from cryptosploit.exceptions import ModuleError
from cryptosploit_modules import BaseModule
from os.path import join, dirname
from pkg_resources import require, DistributionNotFound, VersionConflict


class RsaCtfToolModule(BaseModule):
    tool_path = join(dirname(__file__), "RsaCtfTool")
    allowed_attack_methods = {
        "brent",
        "fermat_numbers_gcd",
        "comfact_cn",
        "wiener",
        "factordb",
        "smallq",
        "pollard_rho",
        "euler",
        "z3_solver",
        "neca",
        "cm_factor",
        "mersenne_pm1_gcd",
        "SQUFOF",
        "small_crt_exp",
        "fibonacci_gcd",
        "smallfraction",
        "boneh_durfee",
        "roca",
        "fermat",
        "londahl",
        "mersenne_primes",
        "partial_q",
        "siqs",
        "noveltyprimes",
        "binary_polinomial_factoring",
        "primorial_pm1_gcd",
        "pollard_p_1",
        "ecm2",
        "cube_root",
        "system_primes_gcd",
        "dixon",
        "ecm",
        "pastctfprimes",
        "qicheng",
        "wolframalpha",
        "hastads",
        "same_n_huge_e",
        "commonfactors",
        "pisano_period",
        "nsif",
        "all",
    }

    def __init__(self):
        super().__init__()
        self.env.check_var = self.check_var

    @staticmethod
    def check_var(name, value):
        match name:
            case "mode":
                if value in RsaCtfToolModule.allowed_attack_methods:
                    return True, ""
                return False, "No such attack mode"
            case "publickey":
                if "*" in value or RsaCtfToolModule.check_file(value):
                    return True, ""
                return False, "No such file"
            case "n" | "p" | "q" | "e":
                try:
                    int(value)
                except ValueError:
                    try:
                        if value.startswith("0x"):
                            int(value, 16)
                        else:
                            return False, "Value must be int or 0xhex"
                    except ValueError:
                        return False, "Value must be int or 0xhex"
                return True, ""
            case _:
                return True, ""

    def check_reqs(self):
        reqs_path = join(self.tool_path, "requirements.txt")
        with open(reqs_path) as f:
            pkgs = f.read()
        try:
            require(pkgs)
        except DistributionNotFound:
            Printer.positive("Install requirements for RsaCtfTool")
            self.command_exec(f"pip install -r {reqs_path}")
            self.command_exec(
                f"pip install -r {join(self.tool_path, 'optional-requirements.txt')}"
            )
        except VersionConflict:
            Printer.negative(
                "Cannot install requirements for RsaCtfTool because of conflict"
            )
            Printer.info("We recommend you to install cryptosploit in venv")

    def run(self):
        self.check_reqs()
        flags = set(iter(self.env)) - {"extra_flags"}
        flags = filter(
            lambda x: x[1], zip(flags, map(lambda x: self.env.get_var(x).value, flags))
        )
        flags = " ".join(
            map(lambda x: f"{'--' if len(x[0]) > 1 else '-'}{x[0]} {x[1]}", flags)
        )
        if extra_flags := self.env.get_var("extra_flags").value:
            flags = " ".join([flags, extra_flags])
        self.command_exec(f'python {join(self.tool_path, "RsaCtfTool.py")} {flags}')


module = RsaCtfToolModule()
