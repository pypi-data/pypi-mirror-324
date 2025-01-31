from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple

import economic_complexity as ec
import pandas as pd
from tesseract_olap import DataRequest, DataRequestParams

if TYPE_CHECKING:
    from logiclayer_complexity.rca import RcaParameters, RcaSubnationalParameters


@dataclass
class RelatednessParameters:
    rca_params: "RcaParameters"
    cutoff: float = 1
    iterations: int = 20
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.measure} Relatedness"

    # api call to know the hierarchy by location
    def build_request_location(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.location,),
            "measures": (self.rca_params.measure,),
            "cuts_include": {**self.rca_params.cuts},
            "parents": self.rca_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.locale is not None:
            params["locale"] = self.rca_params.locale

        return DataRequest.new(self.rca_params.cube, params)

    # api call to know the hierarchy by activity
    def build_request_activity(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.activity,),
            "measures": (self.rca_params.measure,),
            "cuts_include": {**self.rca_params.cuts},
            "parents": self.rca_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.locale is not None:
            params["locale"] = self.rca_params.locale

        return DataRequest.new(self.rca_params.cube, params)

    def _calculate(self, rca: pd.Series) -> pd.Series:
        df_rca = rca.unstack()
        df_relatd = ec.relatedness(df_rca, cutoff=self.cutoff)
        relatd = df_relatd.stack()
        if not isinstance(relatd, pd.Series):
            msg = "Calculation did not yield a pandas.Series"
            raise TypeError(msg)
        return relatd.rename(self.column_name)

    def calculate(
        self,
        df: pd.DataFrame,
        activity_columns: list,
        location_columns: list,
    ) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        name = self.column_name

        df_pivot = self.rca_params.pivot(df)

        rca = self.rca_params._calculate(df_pivot)
        relatd = self._calculate(rca)

        ds = pd.concat([rca, relatd], axis=1).reset_index()

        if sort_ascending is not None:
            ds = ds.sort_values(by=name, ascending=sort_ascending)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        df_index = df[location_columns].drop_duplicates()
        df_column = df[activity_columns].drop_duplicates()

        # add measure
        df_measure = df[
            [df_pivot.index.name, df_pivot.columns.name, self.rca_params.measure]
        ].merge(ds, how="right", on=[df_pivot.index.name, df_pivot.columns.name])

        # add complementary levels to df
        df_index = df_index.merge(df_measure, how="right", on=df_pivot.index.name)
        df_final = df_column.merge(df_index, how="right", on=df_pivot.columns.name)

        return df_final


@dataclass
class RelatednessSubnationalParameters:
    rca_params: "RcaSubnationalParameters"
    cutoff: float = 1
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.subnat_params.measure} Relatedness"

    # api call to know the hierarchy by location
    def build_request_location(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.subnat_params.location,),
            "measures": (self.rca_params.subnat_params.measure,),
            "cuts_include": {**self.rca_params.subnat_params.cuts},
            "parents": self.rca_params.subnat_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.subnat_params.locale is not None:
            params["locale"] = self.rca_params.subnat_params.locale

        return DataRequest.new(self.rca_params.subnat_params.cube, params)

    # api call to know the hierarchy by activity
    def build_request_activity(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.subnat_params.activity,),
            "measures": (self.rca_params.subnat_params.measure,),
            "cuts_include": {**self.rca_params.subnat_params.cuts},
            "parents": self.rca_params.subnat_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.subnat_params.locale is not None:
            params["locale"] = self.rca_params.subnat_params.locale

        return DataRequest.new(self.rca_params.subnat_params.cube, params)

    def _calculate(self, df_subnat: pd.DataFrame, df_global: pd.DataFrame):
        name = self.column_name
        params = self.rca_params.subnat_params

        location_id = params.location_id
        activity_id = params.activity_id

        df, tbl_global, tbl_rca_subnat = self.rca_params._calculate_subnat(
            df_subnat,
            df_global,
        )
        df_country = ec.rca(tbl_global)

        proximity = ec.proximity(df_country)
        output = ec.relatedness(
            tbl_rca_subnat.reindex(columns=list(proximity)).fillna(0),
            proximities=proximity,
        )
        output = pd.melt(output.reset_index(), id_vars=[location_id], value_name=name)
        output = output.merge(df, on=[location_id, activity_id], how="inner")

        return output

    def calculate(
        self,
        df_subnat: pd.DataFrame,
        df_global: pd.DataFrame,
        activity_columns: List[str],
        location_columns: List[str],
    ) -> pd.DataFrame:
        name = self.column_name
        sort_ascending = self.sort_ascending
        params = self.rca_params.subnat_params

        location_id = params.location_id
        activity_id = params.activity_id

        ds = self._calculate(df_subnat, df_global)

        if sort_ascending is not None:
            ds = ds.sort_values(by=name, ascending=sort_ascending)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        # add measure
        df_measure = ds.merge(
            df_subnat[[location_id, activity_id, params.measure]],
            on=[location_id, activity_id],
            how="left",
        )

        # add complementary levels to df
        df_relatedness = df_measure.merge(
            df_subnat[activity_columns].drop_duplicates(),
            on=activity_id,
            how="left",
        )
        df_relatedness = df_relatedness.merge(
            df_subnat[location_columns].drop_duplicates(),
            on=location_id,
            how="left",
        )

        return df_relatedness


@dataclass
class RelativeRelatednessParameters:
    rca_params: "RcaParameters"
    cutoff: float = 1
    iterations: int = 20
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.measure} Relative Relatedness"

    # api call to know the hierarchy by location
    def build_request_location(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.location,),
            "measures": (self.rca_params.measure,),
            "cuts_include": {**self.rca_params.cuts},
            "parents": self.rca_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.locale is not None:
            params["locale"] = self.rca_params.locale

        return DataRequest.new(self.rca_params.cube, params)

    # api call to know the hierarchy by activity
    def build_request_activity(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.activity,),
            "measures": (self.rca_params.measure,),
            "cuts_include": {**self.rca_params.cuts},
            "parents": self.rca_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.locale is not None:
            params["locale"] = self.rca_params.locale

        return DataRequest.new(self.rca_params.cube, params)

    def _calculate(
        self,
        rca: pd.Series,
        filters: Dict[str, Tuple[str, ...]] = {},
    ) -> pd.Series:
        """Calculate the Relative Relatedness and returns it as a Series with (location, activity) MultiIndex."""
        df_rca = rca.unstack()

        opp = df_rca.copy()

        opp[opp >= self.cutoff] = pd.NA
        opp[opp < self.cutoff] = 1

        wcp = ec.relatedness(df_rca)
        wcp_opp = opp * wcp

        if self.rca_params.location in filters:
            filter_values = filters[self.rca_params.location]
            index_list = pd.Index(filter_values).astype(wcp_opp.index.dtype)
            wcp_opp = wcp_opp.loc[wcp_opp.index.isin(index_list)]

            wcp_mean = wcp_opp.mean(axis=1)
            wcp_std = wcp_opp.std(axis=1)

            df_relatd = wcp.transform(lambda x: (x - wcp_mean) / wcp_std)

        elif self.rca_params.activity in filters:
            filter_values = filters[self.rca_params.activity]
            index_list = pd.Index(filter_values).astype(wcp_opp.columns.dtype)
            wcp_opp = wcp_opp[index_list]

            wcp_mean = wcp_opp.mean(axis=0)
            wcp_std = wcp_opp.std(axis=0)

            df_relatd = (wcp - wcp_mean) / wcp_std

        else:
            wcp_mean = wcp_opp.mean(axis=1)
            wcp_std = wcp_opp.std(axis=1)

            df_relatd = wcp.transform(lambda x: (x - wcp_mean) / wcp_std)

        relatd = df_relatd.stack()

        if not isinstance(relatd, pd.Series):
            msg = "Calculation did not yield a pandas.Series"
            raise TypeError(msg)

        return relatd.rename(self.column_name)

    def calculate(
        self,
        df: pd.DataFrame,
        activity_columns: List[str],
        location_columns: List[str],
        filters: Dict[str, Tuple[str, ...]] = {},
    ) -> pd.DataFrame:
        sort_ascending = self.sort_ascending
        name = self.column_name

        df_pivot = self.rca_params.pivot(df)

        rca = self.rca_params._calculate(df_pivot)
        relatd = self._calculate(rca, filters)

        ds = pd.merge(
            rca,
            relatd,
            on=[f"{self.rca_params.location} ID", f"{self.rca_params.activity} ID"],
        ).reset_index()

        if sort_ascending is not None:
            ds = ds.sort_values(by=name, ascending=sort_ascending)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        df_index = df[location_columns].drop_duplicates()
        df_column = df[activity_columns].drop_duplicates()

        # add measure
        df_measure = df[
            [df_pivot.index.name, df_pivot.columns.name, self.rca_params.measure]
        ].merge(ds, how="right", on=[df_pivot.index.name, df_pivot.columns.name])

        # add complementary levels to df
        df_index = df_index.merge(df_measure, how="right", on=df_pivot.index.name)
        df_final = df_column.merge(df_index, how="right", on=df_pivot.columns.name)

        return df_final


@dataclass
class RelativeRelatednessSubnationalParameters:
    rca_params: "RcaSubnationalParameters"
    cutoff: float = 1
    rank: bool = False
    sort_ascending: Optional[bool] = None

    @property
    def column_name(self):
        return f"{self.rca_params.subnat_params.measure} Relative Relatedness"

    # api call to know the hierarchy by location
    def build_request_location(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.subnat_params.location,),
            "measures": (self.rca_params.subnat_params.measure,),
            "cuts_include": {**self.rca_params.subnat_params.cuts},
            "parents": self.rca_params.subnat_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.subnat_params.locale is not None:
            params["locale"] = self.rca_params.subnat_params.locale

        return DataRequest.new(self.rca_params.subnat_params.cube, params)

    # api call to know the hierarchy by activity
    def build_request_activity(self, roles: Set[str]) -> DataRequest:
        params: DataRequestParams = {
            "drilldowns": (self.rca_params.subnat_params.activity,),
            "measures": (self.rca_params.subnat_params.measure,),
            "cuts_include": {**self.rca_params.subnat_params.cuts},
            "parents": self.rca_params.subnat_params.parents,
            "roles": roles,
            "pagination": (1, 0),
        }

        if self.rca_params.subnat_params.locale is not None:
            params["locale"] = self.rca_params.subnat_params.locale

        return DataRequest.new(self.rca_params.subnat_params.cube, params)

    def _calculate(
        self,
        df_subnat: pd.DataFrame,
        df_global: pd.DataFrame,
        filters: Dict[str, Tuple[str, ...]] = {},
    ):
        name = self.column_name
        params = self.rca_params.subnat_params

        location_id = params.location_id
        activity_id = params.activity_id

        df, tbl_global, tbl_rca_subnat = self.rca_params._calculate_subnat(
            df_subnat,
            df_global,
        )
        df_country = ec.rca(tbl_global)

        proximity = ec.proximity(df_country)

        opp = tbl_rca_subnat.copy()

        opp[opp >= self.cutoff] = pd.NA
        opp[opp < self.cutoff] = 1

        wcp = ec.relatedness(
            tbl_rca_subnat.reindex(columns=list(proximity)).fillna(0),
            proximities=proximity,
        )
        wcp_opp = opp * wcp

        # Ensure labels are kept
        wcp_opp.index.name = location_id
        wcp_opp.columns.name = activity_id

        if params.location in filters:
            filter_values = filters[params.location]
            index_list = pd.Index(filter_values).astype(wcp_opp.index.dtype)
            wcp_opp = wcp_opp.loc[wcp_opp.index.isin(index_list)]

            wcp_mean = wcp_opp.mean(axis=1)
            wcp_std = wcp_opp.std(axis=1)

            output = wcp.transform(lambda x: (x - wcp_mean) / wcp_std)

        elif params.activity in filters:
            filter_values = filters[params.activity]
            index_list = pd.Index(filter_values).astype(wcp_opp.columns.dtype)
            wcp_opp = wcp_opp[index_list]

            wcp_mean = wcp_opp.mean(axis=0)
            wcp_std = wcp_opp.std(axis=0)

            output = (wcp - wcp_mean) / wcp_std

        else:
            wcp_mean = wcp_opp.mean(axis=1)
            wcp_std = wcp_opp.std(axis=1)

            output = wcp.transform(lambda x: (x - wcp_mean) / wcp_std)

        output = pd.melt(output.reset_index(), id_vars=[location_id], value_name=name)
        output = output.merge(df, on=[location_id, activity_id], how="inner")

        return output

    def calculate(
        self,
        df_subnat: pd.DataFrame,
        df_global: pd.DataFrame,
        activity_columns: list,
        location_columns: list,
        filters: Dict[str, Tuple[str, ...]] = {},
    ) -> pd.DataFrame:
        name = self.column_name
        sort_ascending = self.sort_ascending
        params = self.rca_params.subnat_params

        location_id = params.location_id
        activity_id = params.activity_id

        ds = self._calculate(df_subnat, df_global, filters)

        if sort_ascending is not None:
            ds = ds.sort_values(by=name, ascending=sort_ascending)

        if sort_ascending is not None or self.rank:
            ds[f"{name} Ranking"] = (
                ds[name].rank(ascending=False, method="max").astype(int)
            )

        # add measure
        df_measure = ds[ds[name].notna()].merge(
            df_subnat[[location_id, activity_id, params.measure]],
            on=[location_id, activity_id],
            how="left",
        )

        # add complementary levels to df
        df_relatedness = df_measure.merge(
            df_subnat[activity_columns].drop_duplicates(),
            on=activity_id,
            how="left",
        )
        df_relatedness = df_relatedness.merge(
            df_subnat[location_columns].drop_duplicates(),
            on=location_id,
            how="left",
        )

        return df_relatedness
