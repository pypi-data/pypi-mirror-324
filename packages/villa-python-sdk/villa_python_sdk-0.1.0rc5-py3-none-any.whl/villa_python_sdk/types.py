from typing import Any, Literal, TypedDict


class Product(TypedDict):
    """Represents a product in the order."""

    cprcode: int
    productName: str
    quantity: int
    branchId: str
    discountFromCoupon: float
    scheduleId: int
    isPreOrder: bool
    usedForCoupon: Any | None
    remark: str
    originalPrice: float
    price: float
    rowTotal: float
    settlementPrice: float
    discountedRowTotal: float
    isControlledProduct: bool


class Schedule(TypedDict, total=False):
    """Represents a delivery schedule. Some fields may be optional."""

    mode: Literal["NATIONWIDE", "EXPRESS"]
    dateTime: str
    scheduleId: int
    deliveryFee: float
    pickingStatus: str | None
    date_slot: str | None
    booking_hour: int | None
    expressFee: float | None
    nationwideConfig: str | None


class Shipping(TypedDict, total=False):
    """Represents shipping details of an order. Some fields may be optional."""

    scheduleList: list[Schedule]
    shippingType: Literal["DELIVERY"]
    shippingPostcode: str | None
    shippingSubDistrict: str | None
    shippingDistrict: str | None  # ✅ Added missing field
    shippingEmail: str | None
    shippingDate: int | None
    shippingPrice: float | None
    shippingLat: float
    shippingLon: float
    shippingAddress: str
    shippingFirstName: str
    shippingLastName: str
    shippingPhone: str
    shippingProvince: str


class DiscountResult(TypedDict):
    """Represents discount details."""

    discounts: list[Any]
    failedCoupons: list[str]
    error: dict[str, str]


class Summary(TypedDict):
    """Represents the summary of an order."""

    subTotal: float
    grandTotal: float
    voucherDiscount: float
    cartDiscount: float
    bogoDiscount: float
    two4Discount: float
    percentageDiscount: float
    shippingDiscount: float
    totalExcludeControlledProducts: float
    expressShippingCost: float
    deliveryFee: float
    discountedDeliveryFee: float
    totalWeight: float
    discountResult: DiscountResult


class Order(TypedDict):
    """Represents the original order input."""

    branchId: str
    couponCodeList: list[str]
    productList: list[Product]
    shipping: Shipping


class CalculatedOrder(TypedDict):
    """Represents the calculated order after processing."""

    productList: list[Product]
    voucherId: list[str]
    basketName: str
    basketId: str
    branchId: str
    orderId: str
    orderDate: int
    ownerId: str
    requestSubstitute: bool
    specialComment: Any | None
    noPlasticBags: bool
    shipping: Shipping
    cartDiscountInfo: list[Any]
    couponCodeList: list[str]
    shippingDiscount: float
    bogoDiscount: float
    voucherDiscount: float
    cartDiscount: float
    subTotal: float
    grandTotal: float
    totalExcludeControlledProducts: float
    validVouchers: list[Any]
    invalidVouchers: list[Any]
    expressShippingCost: float
    totalDiscount: float
    totalWeight: float
    deliveryFee: float
    discountedDeliveryFee: float
    discountResult: DiscountResult
    isFreeShipping: bool
    summary: Summary


class ErrorResponse(TypedDict):
    """Represents an error response returned from the API."""

    error: str
    message: str


# Union type for function returns (either a valid CalculatedOrder or an ErrorResponse)
CalculatedOrderResponse = CalculatedOrder | ErrorResponse  # ✅ Fix for ruff UP007
