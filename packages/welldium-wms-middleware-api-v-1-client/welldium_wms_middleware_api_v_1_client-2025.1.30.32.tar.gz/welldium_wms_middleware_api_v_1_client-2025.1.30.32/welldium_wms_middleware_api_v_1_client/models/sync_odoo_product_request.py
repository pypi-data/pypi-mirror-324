from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncOdooProductRequest")


@_attrs_define
class SyncOdooProductRequest:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        brand_name (Union[None, Unset, str]):
        barcode (Union[None, Unset, str]):
        sku (Union[None, Unset, str]):
        quantity (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    brand_name: Union[None, Unset, str] = UNSET
    barcode: Union[None, Unset, str] = UNSET
    sku: Union[None, Unset, str] = UNSET
    quantity: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        brand_name: Union[None, Unset, str]
        if isinstance(self.brand_name, Unset):
            brand_name = UNSET
        else:
            brand_name = self.brand_name

        barcode: Union[None, Unset, str]
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        else:
            barcode = self.barcode

        sku: Union[None, Unset, str]
        if isinstance(self.sku, Unset):
            sku = UNSET
        else:
            sku = self.sku

        quantity = self.quantity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if brand_name is not UNSET:
            field_dict["brandName"] = brand_name
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if sku is not UNSET:
            field_dict["sku"] = sku
        if quantity is not UNSET:
            field_dict["quantity"] = quantity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        def _parse_brand_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        brand_name = _parse_brand_name(d.pop("brandName", UNSET))

        def _parse_barcode(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        barcode = _parse_barcode(d.pop("barcode", UNSET))

        def _parse_sku(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sku = _parse_sku(d.pop("sku", UNSET))

        quantity = d.pop("quantity", UNSET)

        sync_odoo_product_request = cls(
            id=id,
            name=name,
            brand_name=brand_name,
            barcode=barcode,
            sku=sku,
            quantity=quantity,
        )

        sync_odoo_product_request.additional_properties = d
        return sync_odoo_product_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
