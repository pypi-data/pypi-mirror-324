#!/usr/bin/env python
# File:                Ampel-ZTF/ampel/ztf/t1/ZiT1Combiner.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.03.2020
# Last Modified Date:  23.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable

from ampel.content.DataPoint import DataPoint
from ampel.struct.T1CombineResult import T1CombineResult
from ampel.t1.T1SimpleCombiner import T1SimpleCombiner
from ampel.types import DataPointId


class ZiT1Combiner(T1SimpleCombiner):
    def combine(  # type: ignore[override]
        self, datapoints: Iterable[DataPoint]
    ) -> list[DataPointId] | T1CombineResult:
        """
        :param datapoints: dict instances representing datapoints
        """

        if "ZTF_PRIV" in self.access:
            dps = datapoints
        else:
            dps = [dp for dp in datapoints if dp["body"]["programid"] != 2]
            if len(dps) != len(
                datapoints if isinstance(datapoints, list) else list(datapoints)
            ):
                return T1CombineResult(
                    dps=super().combine(dps), meta={"tag": "HAS_DATARIGHT_EXCLUSION"}
                )

        return super().combine(dps)
