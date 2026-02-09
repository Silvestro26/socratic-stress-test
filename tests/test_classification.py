"""
Tests for the Classification class.
"""

import pytest
from sst.core.classification import Classification


class TestClassification:
    """Test suite for the Classification class."""

    def test_classification_init(self):
        """Test Classification initialization."""
        clf = Classification()
        assert clf.current_state is None
        assert "FACT" in clf.states
        assert "HYP" in clf.states
        assert "UNK" in clf.states

    def test_set_state_fact(self):
        """Test setting state to FACT."""
        clf = Classification()
        clf.set_state("FACT")
        assert clf.current_state == "FACT"
        assert clf.is_fact() is True
        assert clf.is_hyp() is False
        assert clf.is_unk() is False

    def test_set_state_hyp(self):
        """Test setting state to HYP."""
        clf = Classification()
        clf.set_state("HYP")
        assert clf.current_state == "HYP"
        assert clf.is_fact() is False
        assert clf.is_hyp() is True
        assert clf.is_unk() is False

    def test_set_state_unk(self):
        """Test setting state to UNK."""
        clf = Classification()
        clf.set_state("UNK")
        assert clf.current_state == "UNK"
        assert clf.is_fact() is False
        assert clf.is_hyp() is False
        assert clf.is_unk() is True

    def test_set_invalid_state(self):
        """Test that invalid state raises ValueError."""
        clf = Classification()
        with pytest.raises(ValueError) as excinfo:
            clf.set_state("INVALID")
        assert "Invalid state" in str(excinfo.value)

    def test_downgrade_from_fact(self):
        """Test downgrading from FACT to HYP."""
        clf = Classification()
        clf.set_state("FACT")
        clf.downgrade_state()
        assert clf.current_state == "HYP"

    def test_downgrade_from_hyp(self):
        """Test downgrading from HYP to UNK."""
        clf = Classification()
        clf.set_state("HYP")
        clf.downgrade_state()
        assert clf.current_state == "UNK"

    def test_downgrade_from_unk(self):
        """Test that UNK cannot be downgraded further (stays UNK)."""
        clf = Classification()
        clf.set_state("UNK")
        clf.downgrade_state()  # Should not raise, just stay UNK
        assert clf.current_state == "UNK"

    def test_downgrade_without_state_set(self):
        """Test that downgrading without a state raises ValueError."""
        clf = Classification()
        with pytest.raises(ValueError) as excinfo:
            clf.downgrade_state()
        assert "Current state is not set" in str(excinfo.value)

    def test_full_downgrade_chain(self):
        """Test complete downgrade chain: FACT -> HYP -> UNK."""
        clf = Classification()
        clf.set_state("FACT")
        assert clf.is_fact()

        clf.downgrade_state()
        assert clf.is_hyp()

        clf.downgrade_state()
        assert clf.is_unk()

        # Further downgrade should keep it at UNK
        clf.downgrade_state()
        assert clf.is_unk()

    def test_state_values(self):
        """Test numeric state values."""
        clf = Classification()
        assert clf.states["FACT"] == 1
        assert clf.states["HYP"] == 0
        assert clf.states["UNK"] == -1
