import typing as t

from opendigger_pycli.datatypes import IndicatorQuery


class QueryParser:
    def _try_parse_month(self, item: str) -> t.Optional[t.Set[int]]:
        if "~" in item:
            try:
                start_str, end_str = item.split("~", 1)
                start = int(start_str)
                end = int(end_str)
                if start > end:
                    return None
                if start < 1 or end > 12:
                    return None
                return set(range(start, end + 1))
            except ValueError:
                return None
        else:
            try:
                month = int(item)
                if month < 1 or month > 12:
                    return None
                return {month}
            except ValueError:
                return None

    def _try_parse_year(self, item: str) -> t.Optional[t.Set[int]]:
        if "~" in item:
            try:
                start_str, end_str = item.split("~", 1)
                start = int(start_str)
                end = int(end_str)
                if start > end:
                    return None
                if start < 1970 or end > 2100:
                    return None
                return set(range(start, end + 1))
            except ValueError:
                return None
        else:
            try:
                year = int(item)
                if year < 1970 or year > 2100:
                    return None
                return {year}
            except ValueError:
                return None

    def _try_parse_year_month_range(
        self, item: str
    ) -> t.Optional[t.Set[t.Tuple[int, int]]]:
        try:
            start_str, end_str = item.split("~", 1)
            start_year_str, start_month_str = start_str.split("-", 1)
            end_year_str, end_month_str = end_str.split("-", 1)
            start_year = int(start_year_str)
            start_month = int(start_month_str)
            end_year = int(end_year_str)
            end_month = int(end_month_str)
            if start_year > end_year:
                return None
            if start_year < 1970 or end_year > 2100:
                return None
            if start_month > end_month and not start_year < end_year:
                return None
            if start_month < 1 or end_month > 12:
                return None

            result = set()
            current_year = start_year
            current_month = start_month
            while (current_year, current_month) <= (end_year, end_month):
                result.add((current_year, current_month))
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1
            return result

        except ValueError:
            return None

    def _try_parse_year_month(self, item: str) -> t.Optional[t.Set[t.Tuple[int, int]]]:
        if "~" not in item:
            try:
                year_str, month_str = item.split("-", 1)
                year = int(year_str)
                month = int(month_str)
                if year < 1970 or year > 2100:
                    return None
                if month < 1 or month > 12:
                    return None
                return {(year, month)}
            except ValueError:
                return None
        return self._try_parse_year_month_range(item)

    def try_parse_indicator_query(
        self, indicator_query: str
    ) -> t.Optional[IndicatorQuery]:
        all_months = set()
        all_years = set()
        all_year_months = set()

        indicator_query = indicator_query.strip()
        items = indicator_query.split(",")
        for item in items:
            months = self._try_parse_month(item)
            if months is not None:
                all_months.update(months)
                continue
            years = self._try_parse_year(item)
            if years is not None:
                all_years.update(years)
                continue
            year_months = self._try_parse_year_month(item)
            if year_months is not None:
                all_year_months.update(year_months)
                continue
            if not months and not years and not year_months:
                return None
        if not all_months and not all_years and not all_year_months:
            return None

        return IndicatorQuery(
            months=frozenset(all_months),
            years=frozenset(all_years),
            year_months=frozenset(all_year_months),
        )
