#!/usr/bin/env python
# File:                Ampel-core/ampel/model/template/PeriodicSummaryT3.py
# License:             BSD-3-Clause
# Author:              Jakob van Santen <jakob.van.santen@desy.de>
# Date:                10.08.2020
# Last Modified Date:  10.08.2020
# Last Modified By:    Jakob van Santen <jakob.van.santen@desy.de>

from collections.abc import Sequence

from ampel.template.PeriodicSummaryT3 import LoaderDirective, PeriodicSummaryT3


class ZTFPeriodicSummaryT3(PeriodicSummaryT3):  # type: ignore[override]
    """
    Periodic summary process with sensible defaults for ZTF.
    """

    tag: dict = {"with": "ZTF", "without": "HAS_ERROR"}
    load: None | Sequence[str | LoaderDirective] = ["TRANSIENT", "T2RECORD"]
