"""
File: salary_spliter.py
──────────────────────────
Author: santa
Project: multi_facts_inference_engine
Created: 3/18/26 21:15 
Email: santa.basnet@wiseyak.com
Github: https://github.com/santabasnet
Organization: WiseYak / Integrated ICT
"""

from itertools import pairwise, accumulate
from math import inf
from enum import Enum
from typing import List, Dict


class Literals:
    ANSWER_FIELDS = [
        "parts",
        "tax_parts",
        "progressive_tax",
        "total_tax",
        "annual_payable",
        "monthly_salary"
    ]


class MaritalStatus(Enum):
    UNMARRIED = "Unmarried"
    MARRIED = "Married"


class SalaryConstant:
    SALARY_RANGE_SINGLE: List[float] = [
        0, 500000, 700000, 1000000, 2000000, inf
    ]
    SALARY_RANGE_MARRIED: List[float] = [
        0, 600000, 800000, 1100000, 2000000, inf
    ]

    SALARY_SLABS: Dict[MaritalStatus, List[float]] = {
        MaritalStatus.UNMARRIED: SALARY_RANGE_SINGLE,
        MaritalStatus.MARRIED: SALARY_RANGE_MARRIED,
    }

    SLAB_FACTORS:List[float] = [0.01, 0.10, 0.20, 0.30, 0.36]

    NUMBER_OF_MONTHS: int = 12


class SalaryPayableCalculator:

    def __init__(self, status: MaritalStatus):
        self.status = status
        self.slabs = SalaryConstant.SALARY_SLABS[status]

    # --------------------------------------
    # Split annual income into salary slabs
    # --------------------------------------
    def split_parts(self, income: float):
        return [
            max(0.0, min(income, upper) - lower)
            for lower, upper in pairwise(self.slabs)
        ]

    # Calculate tax parts.
    def tax_parts(self, parts: List[float]) -> List[float]:
        return [
            p * f for p, f in zip(parts, SalaryConstant.SLAB_FACTORS)
        ]

    # ---------------------------------
    # Calculate salary
    # ---------------------------------
    def calculate(self, annual_income: float):
        parts = self.split_parts(annual_income)
        padded_parts = parts + [0] * (len(SalaryConstant.SLAB_FACTORS) - len(parts))
        parts = self.tax_parts(padded_parts)
        progressive_tax = list(accumulate(parts))
        total_tax = progressive_tax[-1] if progressive_tax else 0
        annual_payable = annual_income - total_tax
        monthly_salary = annual_payable / SalaryConstant.NUMBER_OF_MONTHS

        answer_data = [
            padded_parts,
            parts,
            progressive_tax,
            total_tax,
            annual_payable,
            monthly_salary            
        ]

        return dict(zip(Literals.ANSWER_FIELDS, answer_data))


        