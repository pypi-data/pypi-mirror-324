#!/usr/bin/env python

from .yfc_dat import Period, Interval, AmbiguousComparisonException
from .yfc_ticker import Ticker, verify_cached_tickers_prices
from .yfc_multi import download
from .yfc_logging import EnableLogging, DisableLogging
from .yfc_cache_manager import _option_manager as options

from .yfc_upgrade import _init_options, _reset_cached_cals, _fix_dt_types_in_divs_splits
_init_options()
_reset_cached_cals()
_fix_dt_types_in_divs_splits()

from .yfc_upgrade import _sort_release_dates, _init_history_metadata
_sort_release_dates()
_init_history_metadata()

from .yfc_upgrade import _tidy_upgrade_history, _fix_prices_inconsistencies
_tidy_upgrade_history()
_fix_prices_inconsistencies()

from .yfc_upgrade import _add_xcal_to_options
_add_xcal_to_options()

from .yfc_upgrade import _add_options_max_age_to_options
_add_options_max_age_to_options()

from .yfc_upgrade import _upgrade_calendar_to_df, _add_holdings_analysis_to_options
_upgrade_calendar_to_df()
_add_holdings_analysis_to_options()

from .yfc_upgrade import _fix_prices_final_again, _reset_cached_cals_again, _reset_CCY_cal
_fix_prices_final_again()
_reset_cached_cals_again()
_reset_CCY_cal()

from .yfc_upgrade import _add_repaired_to_cached_divs
_add_repaired_to_cached_divs()

from .yfc_upgrade import _fix_24_hour_prices_final
_fix_24_hour_prices_final()
