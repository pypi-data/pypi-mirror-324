import pandas as pd
import aesoppy.aesop as aesop


class DividendPerShareCy:


    def __init__(self, **kwargs):
        self.dividend_df = kwargs.get('dividend_df', 'error')
        self.frequency = kwargs.get('div_frequency', 4)
        self.lookback = kwargs.get('lookback', 21)
        self.pershare_div_cy_growth_df = self._pershare_div_cy_growth_df()


    def _pershare_div_cy_growth_df(self):
        divgro_cy_df1 = self.dividend_df
        current_year = aesop.aesop_now.year
        lookback = self.lookback

        divgro_cy_df1.index = pd.to_datetime(divgro_cy_df1.index)

        divgro_cy_df2 = divgro_cy_df1.groupby(divgro_cy_df1.index.year).agg(
            dividend_amount_cy=pd.NamedAgg('dividend_amount', aggfunc='sum')
        )

        divgro_cy_df2['divgro_cy'] = divgro_cy_df2['dividend_amount_cy'].pct_change()

        # Reduce Dataframe Index By year
        for index, row in divgro_cy_df2.iterrows():
            if current_year - index >= lookback:
                divgro_cy_df2.drop(index, inplace=True)


        return divgro_cy_df2


class DividendPerShareFy:


    def __init__(self, **kwargs):
        self.pershare_df = kwargs.get('pershare_df', 'error')
        self.frequency = kwargs.get('div_frequency', 4)
        self.lookback = kwargs.get('lookback', 21)
        self.pershare_div_fy_growth_df = self._pershare_div_fy_growth_df()


    def _pershare_div_fy_growth_df(self):
        df1 = self.pershare_df
        divgro_fy_df1 = pd.DataFrame(df1['pershare_dividends'], index=df1.index)
        current_year = aesop.aesop_now.year
        lookback = self.lookback

        divgro_fy_df1['divgro_fy'] = divgro_fy_df1['pershare_dividends'].pct_change()

        # Reduce Dataframe Index By year
        for index, row in divgro_fy_df1.iterrows():
            if current_year - index >= lookback:
                divgro_fy_df1.drop(index, inplace=True)


        return divgro_fy_df1


class DividendTotalCashFy:


    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.frequency = kwargs.get('div_frequency', 4)
        self.lookback = kwargs.get('lookback', 21)
        self.dividend_paid_fy_df = self._dividend_cash_fy_df()


    def _dividend_cash_fy_df(self):
        df1 = self.fin_df
        divgro_df1 = pd.DataFrame(abs(df1['cash_for_dividends']), index=df1.index)
        current_year = aesop.aesop_now.year
        lookback = self.lookback

        divgro_df1['divgro'] = divgro_df1['cash_for_dividends'].pct_change()

        # Reduce Dataframe Index By year
        for index, row in divgro_df1.iterrows():
            if current_year - index >= lookback:
                divgro_df1.drop(index, inplace=True)


        return divgro_df1

