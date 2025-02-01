# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry, as_optional_global


class ScalableGroupTagEntry(_ParcelEntry):
    sgt_name: Optional[Global[str]] = Field(default=None, validation_alias="sgtName", serialization_alias="sgtName")
    tag: Optional[Global[str]] = Field(default=None)


class ScalableGroupTagParcel(_ParcelBase):
    type_: Literal["security-scalablegrouptag"] = Field(default="security-scalablegrouptag")
    entries: List[ScalableGroupTagEntry] = Field(validation_alias=AliasPath("data", "entries"), default_factory=list)

    def add_entry(self, sgt_name: Optional[str] = None, tag: Optional[str] = None):
        self.entries.append(
            ScalableGroupTagEntry(
                sgt_name=as_optional_global(sgt_name),
                tag=as_optional_global(tag),
            )
        )
