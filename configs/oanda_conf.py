from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountDetails
class ClientConfig:
    def __init__(self, access_token=None, account_id=None, environment='practice'):
        self._provider = "Oanda"
        self._access_token = access_token
        self._account_id = account_id
        self._environment = environment
        self._client_api = None
        self._initialize_client_api()
        self._initial_balance = self.get_current_balance()
    def _initialize_client_api(self):
        if self._access_token and self._environment:
            self._client_api = API(access_token=self._access_token, environment=self._environment, headers={"Accept-Datetime-Format": "RFC3339"})
            self._initial_balance = self.get_current_balance()
    def get_current_balance(self):
        request = AccountDetails(accountID=self.account_id)
        response = self.client_api.request(request)

        if response and 'account' in response:
            account_info = response['account']
            balance = float(account_info['balance'])
            return balance
    @property
    def provider(self):
        return self._provider
    @property
    def access_token(self):
        return self._access_token

    @property
    def account_id(self):
        return self._account_id

    @property
    def environment(self):
        return self._environment

    @property
    def client_api(self):
        return self._client_api

    @property
    def initial_balance(self):
        return self._initial_balance
    
    @property
    def current_balance(self):
        return self.get_current_balance()
    
    @access_token.setter
    def access_token(self, value):
        if value != self._access_token:
            self._access_token = value
            self._initialize_client_api()
            

    @account_id.setter
    def account_id(self, value):
        self._account_id = value  # No need to reinitialize the API client for account_id changes

    @environment.setter
    def environment(self, value):
        if value != self._environment:
            self._environment = value
            self._initialize_client_api()
class TradeConfig:
    def __init__(self, instrument, lookback_count, st_period, lt_period, hurst_period, risk_factor, risk_reward, time_interval, granularity, inposition, bb_window, bb_window_dev):
        self._instrument = instrument
        self._lookback_count = lookback_count
        self._st_period = st_period
        self._lt_period = lt_period
        self._hurst_period = hurst_period
        self._risk_factor = risk_factor
        self._risk_reward = risk_reward
        self._time_interval = time_interval
        self._granularity = granularity
        self._inposition = inposition
        self._bb_window = bb_window
        self._bb_window_dev = bb_window_dev
    @property
    def instrument(self):
        return self._instrument

    @property
    def lookback_count(self):
        return self._lookback_count

    @property
    def st_period(self):
        return self._st_period

    @property
    def lt_period(self):
        return self._lt_period

    @property
    def hurst_period(self):
        return self._hurst_period

    @property
    def risk_factor(self):
        return self._risk_factor

    @property
    def risk_reward(self):
        return self._risk_reward

    @property
    def time_interval(self):
        return self._time_interval

    @property
    def inposition(self):
        return self._inposition
    
    @property
    def granularity(self):
        return self._granularity
    @property
    def bb_window(self):
        return self._bb_window
    @property
    def bb_window_dev(self):
        return self._bb_window_dev
    @instrument.setter
    def instrument(self, value):
        self._instrument = value

    @lookback_count.setter
    def lookback_count(self, value):
        self._lookback_count = value

    @st_period.setter
    def st_period(self, value):
        self._st_period = value

    @lt_period.setter
    def lt_period(self, value):
        self._lt_period = value

    @hurst_period.setter
    def hurst_period(self, value):
        self._hurst_period = value

    @risk_factor.setter
    def risk_factor(self, value):
        self._risk_factor = value

    @risk_reward.setter
    def risk_reward(self, value):
        self._risk_reward = value

    @time_interval.setter
    def time_interval(self, value):
        self._time_interval = value
    @granularity.setter
    def granularity(self, value):
        self._granularity = value
    @inposition.setter
    def inposition(self, value):
        self._inposition = value
    @bb_window.setter
    def bb_window(self, value):
        self._bb_window = value
    @bb_window_dev.setter
    def bb_window_dev(self, value):
        self._bb_window_dev = value
CLIENT_CONFIG = ClientConfig(access_token="9c7349b9a9bd3d17409758cb7e29e53f-7fcbdfe7bc0636788aa51f7e4a95601f",
                                account_id="101-003-28600525-001",
                                environment="practice")
TRADE_CONFIG = TradeConfig(instrument='EUR_USD',
                            lookback_count=200,
                            st_period=5, lt_period=21,
                            hurst_period=200,
                            risk_factor=0.016 / 100,
                            risk_reward=0.75,
                            time_interval=1 * 60,
                            granularity="S5",
                            inposition=False,
                            bb_window=20,
                            bb_window_dev=0.8)


# Client specific configs
# OANDA_ACCESS_TOKEN = "9c7349b9a9bd3d17409758cb7e29e53f-7fcbdfe7bc0636788aa51f7e4a95601f"
# CLIENT_CONFIG.account_id = "101-003-28600525-001"
# OANDA_ACCOUNT_ENV = "practice"
# CLIENT_CONFIG.client_api = API(access_token=OANDA_ACCESS_TOKEN, environment=OANDA_ACCOUNT_ENV)


# # Script specific configs
# INSTRUMENT = 'EUR_USD'
# LOOKBACK_COUNT = 200
# ST_PERIOD = 5
# LT_PERIOD = 21
# HURST_PERIOD = 200
# RISK_FACTOR = 0.016 / 100
# RISK_REWARD = 0.75  # 3/4
# TIME_INTERVAL = 1 * 60