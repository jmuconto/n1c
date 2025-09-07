# n1c_core/anchor.py

from typing import Dict, Optional
from n1c_core.models import Anchor


class AnchorManager:
    """
    Manages anchor nodes in the N1C network.
    Anchors facilitate transactions, apply spreads/fees, and optionally validate transactions.
    """

    def __init__(self):
        # Anchor storage: anchor_id -> Anchor object
        self.anchors: Dict[str, Anchor] = {}

    # ---------------------------
    # Anchor Registration
    # ---------------------------
    def register_anchor(self, anchor_id: str, spread: float = 2.0, tax_rate: float = 0.0) -> Anchor:
        """
        Register a new anchor node.
        """
        if anchor_id in self.anchors:
            raise ValueError(f"Anchor {anchor_id} already exists")

        if not (0 <= spread <= 7):
            raise ValueError("Spread must be between 0% and 7%")

        if not (0 <= tax_rate <= 100):
            raise ValueError("Tax rate must be between 0% and 100%")

        anchor = Anchor(anchor_id=anchor_id, spread=spread, tax_rate=tax_rate)
        self.anchors[anchor_id] = anchor
        return anchor

    # ---------------------------
    # Anchor Retrieval
    # ---------------------------
    def get_anchor(self, anchor_id: str) -> Optional[Anchor]:
        """
        Retrieve anchor by ID.
        """
        return self.anchors.get(anchor_id)

    def get_all_anchors(self):
        """
        Retrieve all registered anchors.
        """
        return list(self.anchors.values())

    # ---------------------------
    # Fee & Tax Calculation
    # ---------------------------
    def calculate_fee(self, anchor_id: str, amount: float) -> float:
        """
        Calculate fee based on anchor spread.
        """
        anchor = self.get_anchor(anchor_id)
        if not anchor:
            return 0.0
        return amount * (anchor.spread / 100)

    def calculate_tax(self, anchor_id: str, amount: float) -> float:
        """
        Calculate tax based on anchor tax rate.
        """
        anchor = self.get_anchor(anchor_id)
        if not anchor:
            return 0.0
        return amount * (anchor.tax_rate / 100)
