from webbrowser import get

import pytest
from scripts.helpful_scipts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, getAccount
from scripts.deploy import deploy_fund_me
from brownie import accounts, network, exceptions


def test_can_fund_and_withdraw():
    account = getAccount()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account = getAccount()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(Exception):
        fund_me.withdraw({"from": bad_actor})
