"""
Tests for the Claim class.
"""

import pytest
from sst.core.claim import Claim


class TestClaim:
    """Test suite for the Claim class."""

    def test_claim_creation(self):
        """Test basic Claim instantiation."""
        claim = Claim(
            statement="Water boils at 100°C at sea level.",
            label="FACT",
            confidence=95.0,
            sources=["CRC Handbook of Chemistry"]
        )
        assert claim.statement == "Water boils at 100°C at sea level."
        assert claim.label == "FACT"
        assert claim.confidence == 95.0
        assert claim.sources == ["CRC Handbook of Chemistry"]

    def test_claim_with_empty_sources(self):
        """Test Claim with no sources."""
        claim = Claim(
            statement="Some hypothesis",
            label="HYP",
            confidence=50.0,
            sources=[]
        )
        assert claim.sources == []
        assert claim.label == "HYP"

    def test_claim_with_multiple_sources(self):
        """Test Claim with multiple sources."""
        sources = ["Source A", "Source B", "Source C"]
        claim = Claim(
            statement="A well-supported fact",
            label="FACT",
            confidence=90.0,
            sources=sources
        )
        assert len(claim.sources) == 3
        assert "Source B" in claim.sources

    def test_claim_repr(self):
        """Test string representation of Claim."""
        claim = Claim(
            statement="Test statement",
            label="UNK",
            confidence=30.0,
            sources=[]
        )
        repr_str = repr(claim)
        assert "Test statement" in repr_str
        assert "UNK" in repr_str
        assert "30.0" in repr_str

    def test_claim_confidence_range(self):
        """Test Claim with boundary confidence values."""
        # Minimum confidence
        claim_min = Claim("Low confidence", "UNK", 0.0, [])
        assert claim_min.confidence == 0.0

        # Maximum confidence
        claim_max = Claim("High confidence", "FACT", 100.0, ["Strong source"])
        assert claim_max.confidence == 100.0

    def test_claim_labels(self):
        """Test all valid label types."""
        for label in ["FACT", "HYP", "UNK"]:
            claim = Claim("Test", label, 50.0, [])
            assert claim.label == label
