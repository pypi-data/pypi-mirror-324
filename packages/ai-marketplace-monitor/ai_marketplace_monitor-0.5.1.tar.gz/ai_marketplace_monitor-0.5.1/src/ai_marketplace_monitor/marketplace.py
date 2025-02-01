import time
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Generator, Generic, List, Type, TypeVar

from playwright.sync_api import Browser, Page

from .item import SearchedItem
from .utils import DataClassWithHandleFunc, convert_to_seconds, hilight


@dataclass
class MarketItemCommonConfig(DataClassWithHandleFunc):
    """Item options that can be specified in market (non-marketplace specifc)

    This class defines and processes options that can be specified
    in both marketplace and item sections, generic to all marketplaces
    """

    exclude_sellers: List[str] | None = None
    max_search_interval: int | None = None
    notify: List[str] | None = None
    search_city: List[str] | None = None
    # radius must be processed after search_city
    radius: List[int] | None = None
    search_interval: int | None = None
    search_region: List[str] | None = None
    max_price: int | None = None
    min_price: int | None = None

    def handle_exclude_sellers(self: "MarketItemCommonConfig") -> None:
        if self.exclude_sellers is None:
            return

        if isinstance(self.exclude_sellers, str):
            self.exclude_sellers = [self.exclude_sellers]
        if not isinstance(self.exclude_sellers, list) or not all(
            isinstance(x, str) for x in self.exclude_sellers
        ):
            raise ValueError(f"Item {hilight(self.name, "name")} exclude_sellers must be a list.")

    def handle_max_search_interval(self: "MarketItemCommonConfig") -> None:
        if self.max_search_interval is None:
            return

        if isinstance(self.max_search_interval, str):
            try:
                self.max_search_interval = convert_to_seconds(self.max_search_interval)
            except Exception as e:
                raise ValueError(
                    f"Marketplace {self.name} max_search_interval {self.max_search_interval} is not recognized."
                ) from e
        if not isinstance(self.max_search_interval, int) or self.max_search_interval < 1:
            raise ValueError(
                f"Item {hilight(self.name, "name")} max_search_interval must be at least 1 second."
            )

    def handle_notify(self: "MarketItemCommonConfig") -> None:
        if self.notify is None:
            return

        if isinstance(self.notify, str):
            self.notify = [self.notify]
        if not all(isinstance(x, str) for x in self.notify):
            raise ValueError(
                f"Item {hilight(self.name, "name")} notify must be a string or list of string."
            )

    def handle_radius(self: "MarketItemCommonConfig") -> None:
        if self.radius is None:
            return

        if self.search_city is None:
            raise ValueError(
                f"Item {hilight(self.name, "name")} radius must be None if search_city is None."
            )

        if isinstance(self.radius, int):
            self.radius = [self.radius]

        if not all(isinstance(x, int) for x in self.radius):
            raise ValueError(
                f"Item {hilight(self.name, "name")} radius must be one or a list of integers."
            )

        if len(self.radius) != len(self.search_city):
            raise ValueError(
                f"Item {hilight(self.name, "name")} radius must be the same length as search_city."
            )

    def handle_search_city(self: "MarketItemCommonConfig") -> None:
        if self.search_city is None:
            return

        if isinstance(self.search_city, str):
            self.search_city = [self.search_city]
        if not isinstance(self.search_city, list) or not all(
            isinstance(x, str) for x in self.search_city
        ):
            raise ValueError(
                f"Item {hilight(self.name, "name")} search_city must be a string or list of string."
            )

    def handle_search_interval(self: "MarketItemCommonConfig") -> None:
        if self.search_interval is None:
            return

        if isinstance(self.search_interval, str):
            try:
                self.search_interval = convert_to_seconds(self.search_interval)
            except Exception as e:
                raise ValueError(
                    f"Marketplace {self.name} search_interval {self.search_interval} is not recognized."
                ) from e
        if not isinstance(self.search_interval, int) or self.search_interval < 1:
            raise ValueError(
                f"Item {hilight(self.name, "name")} search_interval must be at least 1 second."
            )

    def handle_search_region(self: "MarketItemCommonConfig") -> None:
        if self.search_region is None:
            return

        if isinstance(self.search_region, str):
            self.search_region = [self.search_region]

        if not isinstance(self.search_region, list) or not all(
            isinstance(x, str) for x in self.search_region
        ):
            raise ValueError(
                f"Item {hilight(self.name, "name")} search_region must be one or a list of string."
            )

    def handle_max_price(self: "MarketItemCommonConfig") -> None:
        if self.max_price is None:
            return
        if not isinstance(self.max_price, int):
            raise ValueError(f"Item {hilight(self.name, "name")} max_price must be an integer.")

    def handle_min_price(self: "MarketItemCommonConfig") -> None:
        if self.min_price is None:
            return

        if not isinstance(self.min_price, int):
            raise ValueError(f"Item {hilight(self.name, "name")} min_price must be an integer.")


@dataclass
class MarketplaceConfig(MarketItemCommonConfig):
    """Generic marketplace config"""

    pass


@dataclass
class ItemConfig(MarketItemCommonConfig):
    """This class defined options that can only be specified for items."""

    # keywords is required, all others are optional
    keywords: List[str] = field(default_factory=list)
    exclude_keywords: List[str] | None = None
    exclude_by_description: List[str] | None = None
    description: str | None = None
    enabled: bool | None = None
    marketplace: str | None = None

    def handle_keywords(self: "ItemConfig") -> None:
        if isinstance(self.keywords, str):
            self.keywords = [self.keywords]

        if not isinstance(self.keywords, list) or not all(
            isinstance(x, str) for x in self.keywords
        ):
            raise ValueError(f"Item {hilight(self.name, "name")} keywords must be a list.")
        if len(self.keywords) == 0:
            raise ValueError(f"Item {hilight(self.name, "name")} keywords list is empty.")

    def handle_description(self: "ItemConfig") -> None:
        if self.description is None:
            return
        if not isinstance(self.description, str):
            raise ValueError(f"Item {hilight(self.name, "name")} description must be a string.")

    def handle_enabled(self: "ItemConfig") -> None:
        if self.enabled is None:
            return
        if not isinstance(self.enabled, bool):
            raise ValueError(f"Item {hilight(self.name, "name")} enabled must be a boolean.")

    def handle_exclude_by_description(self: "ItemConfig") -> None:
        if self.exclude_by_description is None:
            return
        if isinstance(self.exclude_by_description, str):
            self.exclude_by_description = [self.exclude_by_description]
        if not isinstance(self.exclude_by_description, list) or not all(
            isinstance(x, str) for x in self.exclude_by_description
        ):
            raise ValueError(
                f"Item {hilight(self.name, "name")} exclude_by_description must be a list."
            )


TMarketplaceConfig = TypeVar("TMarketplaceConfig", bound=MarketplaceConfig)
TItemConfig = TypeVar("TItemConfig", bound=ItemConfig)


class Marketplace(Generic[TMarketplaceConfig, TItemConfig]):

    def __init__(self: "Marketplace", name: str, browser: Browser | None, logger: Logger) -> None:
        self.name = name
        self.browser = browser
        self.logger = logger
        self.page: Page | None = None

    @classmethod
    def get_config(cls: Type["Marketplace"], **kwargs: Any) -> TMarketplaceConfig:
        raise NotImplementedError("get_config method must be implemented by subclasses.")

    @classmethod
    def get_item_config(cls: Type["Marketplace"], **kwargs: Any) -> TItemConfig:
        raise NotImplementedError("get_config method must be implemented by subclasses.")

    def configure(self: "Marketplace", config: TMarketplaceConfig) -> None:
        self.config = config

    def set_browser(self: "Marketplace", browser: Browser) -> None:
        self.browser = browser
        self.page = None

    def stop(self: "Marketplace") -> None:
        if self.browser is not None:
            self.browser.close()
            self.browser = None
            self.page = None

    def goto_url(self: "Marketplace", url: str, attempt: int = 0) -> None:
        try:
            assert self.page is not None
            self.page.goto(url, timeout=0)
            self.page.wait_for_load_state("domcontentloaded")
        except Exception as e:
            if attempt == 10:
                raise RuntimeError(f"Failed to navigate to {url} after 10 attempts. {e}") from e
            time.sleep(5)
            self.goto_url(url, attempt + 1)
        except KeyboardInterrupt:
            raise

    def search(self: "Marketplace", item: TItemConfig) -> Generator[SearchedItem, None, None]:
        raise NotImplementedError("Search method must be implemented by subclasses.")
