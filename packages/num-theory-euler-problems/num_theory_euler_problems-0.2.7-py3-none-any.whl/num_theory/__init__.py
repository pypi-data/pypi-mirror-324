# read version from installed package
from importlib.metadata import version
__version__ = version("num_theory_euler_problems")

from num_theory.arithmetic_progression import arithmetic_progression
from num_theory.is_prime import is_prime
from num_theory.prime_factorization import prime_factorization
from num_theory.get_primes import get_primes