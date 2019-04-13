import os
import glob
import random

import fund_standardization

file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
KOSPI_TICKER = []
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])

FEE_RATE = 0.000015
TAX_RATE = 0.003
RISK_FREE_RATE = 0.02
INITIAL_FUNDS = 100000000
STOCK_SELCTION_RATE = 0.2

class Chromosome:
    # a candidate solution
    def __init__(self, days, stock_prices):
        self._genes = []
        for i in range(len(KOSPI_TICKER)):
            if random.random() <= STOCK_SELCTION_RATE:
                self._genes.append(1)
            else:
                self._genes.append(0)
        self._days = days
        self._stock_prices = stock_prices
        self._ticker = KOSPI_TICKER

        self._num_of_selected_stocks = 0
        self._allocated_fund_amount = 0
        self._allocated_fund = []
        self._remainder_of_pf = 0
        self._share = []
        self._handling_fee = []
        self._remainder_of_stock = []
        self._return = []
        self._securities_transaction_tax = []
        self._funds_standardization = []
        self._pf_funds_standardization = []
        self._roi = 0
        self._risk = 0
        self._fitness = 0

    def get_tickers(self):
        return self._ticker

    def get_genes(self):
        return self._genes

    def get_fitness(self):
        _num_of_stocks = len(KOSPI_TICKER)
        _num_of_selected_stocks = fund_standardization.num_of_selected_stocks(self._genes, _num_of_stocks)
        self._num_of_selected_stocks = _num_of_selected_stocks
        _allocated_fund_amount = 0
        if _num_of_selected_stocks != 0:
            _allocated_fund_amount = INITIAL_FUNDS // _num_of_selected_stocks
        else:
            _fitness = 0.0
            _allocated_fund_amount = 0
            _remainder_of_pf = INITIAL_FUNDS

        _allocated_fund = fund_standardization.allocated_funds(self._genes, _allocated_fund_amount, _num_of_stocks)
        self._allocated_fund = _allocated_fund
        # print("_allocated_fund", _allocated_fund)
        _remainder_of_pf = fund_standardization.remainder_of_pfs(INITIAL_FUNDS, _allocated_fund_amount, _num_of_selected_stocks)
        self._remainder_of_pf = _remainder_of_pf
        # print("_remainder_of_pf", _remainder_of_pf)
        # print("self._days", self._days)
        # print("_stock_price", _stock_price)
        _share = fund_standardization.shares(self._genes, _num_of_stocks, _allocated_fund, self._stock_prices, FEE_RATE)
        self._share = _share
        # print("_share", _share)
        _handling_fee = fund_standardization.handling_fees(self._genes, self._days, _num_of_stocks, _share, self._stock_prices, FEE_RATE)
        self._handling_fee = _handling_fee
        # print("_handling_fee", _handling_fee)
        _remainder_of_stock = fund_standardization.remainder_of_stocks(self._genes, _num_of_stocks, _allocated_fund, self._stock_prices, _share, _handling_fee)
        self.__remainder_of_stock = _remainder_of_stock
        # print("_remainder_of_stock", _remainder_of_stock)
        _return = fund_standardization.returns(self._genes, self._days, _num_of_stocks, _share, self._stock_prices)
        self._return = _return
        # print("_return", _return)
        _securities_transaction_tax = fund_standardization.securities_transaction_taxes(self._genes, self._days, _num_of_stocks, _share, self._stock_prices, TAX_RATE)
        self._securities_transaction_tax = _securities_transaction_tax
        # print("_securities_transaction_tax", _securities_transaction_tax)
        _funds_standardization = fund_standardization.funds_standardizations(self._genes, _num_of_stocks, self._days, _allocated_fund, _handling_fee, _return, _securities_transaction_tax, _remainder_of_stock)
        self._funds_standardization = _funds_standardization
        # print("_funds_standardization", _funds_standardization)
        _pf_funds_standardization = fund_standardization.pf_funds_standardizations(self._days, _num_of_stocks, _funds_standardization, _remainder_of_pf)
        self._pf_funds_standardization = _pf_funds_standardization
        # print("_pf_funds_standardization", _pf_funds_standardization)
        _roi = fund_standardization.rois(_pf_funds_standardization, INITIAL_FUNDS)
        self._roi = _roi
        # print("_roi", _roi)
        _risk = fund_standardization.risks(self._days, _pf_funds_standardization)
        self._risk = _risk
        # print("_risk", _risk)
        _fitness = fund_standardization.fitnesses(_roi, _risk, RISK_FREE_RATE)
        self._fitness = _fitness
        # print("Fitness: ", self._fitness)
        return _fitness

    def get_num_of_selected_stocks(self):
        return self._num_of_selected_stocks

    def get_allocated_fund_amount(self):
        return self._allocated_fund_amount

    def get_funds_standardization(self):
        return self._funds_standardization

    def get_pf_funds_standardization(self):
        return self._pf_funds_standardization

    def get_roi(self):
        return self._roi

    def get_risk(self):
        return self._risk

    def get_days(self):
        return self._days

    def __str__(self):
        return self._genes.__str__()