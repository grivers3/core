"""Platform for Marta sensor integration."""

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo  # , EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify

from .const import ATTRIBUTION, DEFAULT_NAME, DEVICE_TRAINS_ID, DOMAIN, STATION_NAMES


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    station_entities: list[SensorEntityDescription] = []
    for station_name in STATION_NAMES:
        slug_name = slugify(f"{station_name}")
        station_description = SensorEntityDescription(
            key=slug_name,
            icon="mdi:train",
            # entity_category=EntityCategory.DIAGNOSTIC,
            name=station_name,
            entity_registry_enabled_default=False,
        )
        station_entities.append(station_description)
    async_add_entities(
        [StationSensor(coordinator, description) for description in station_entities],
        False,
    )


class StationSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: DataUpdateCoordinator, description: SensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = description.key
        self.entity_description = description
        self._attr_name = description.name
        self._state: list[str] = []
        self._attib: dict[str, int] = {}

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return DeviceInfo(
            identifiers={(DOMAIN, DEVICE_TRAINS_ID)},
            manufacturer=DEFAULT_NAME,
            name="Trains",
            suggested_area=DEFAULT_NAME,
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        self._attib.clear()
        suffix_list = ["", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8"]
        e_blue_trains = {}
        w_blue_trains = {}
        e_green_trains = {}
        w_green_trains = {}
        n_gold_trains = {}
        s_gold_trains = {}
        n_red_trains = {}
        s_red_trains = {}

        # Group trains by line
        for train in self._state:
            dir_line = f"{train.direction}-{train.line.capitalize()}"
            if dir_line == "E-Blue":
                e_blue_trains[
                    dir_line + suffix_list[len(e_blue_trains)]
                ] = train.waiting_time
            elif dir_line == "W-Blue":
                w_blue_trains[
                    dir_line + suffix_list[len(w_blue_trains)]
                ] = train.waiting_time
            elif dir_line == "E-Green":
                e_green_trains[
                    dir_line + suffix_list[len(e_green_trains)]
                ] = train.waiting_time
            elif dir_line == "W-Green":
                w_green_trains[
                    dir_line + suffix_list[len(w_green_trains)]
                ] = train.waiting_time
            elif dir_line == "N-Gold":
                n_gold_trains[
                    dir_line + suffix_list[len(n_gold_trains)]
                ] = train.waiting_time
            elif dir_line == "S-Gold":
                s_gold_trains[
                    dir_line + suffix_list[len(s_gold_trains)]
                ] = train.waiting_time
            elif dir_line == "N-Red":
                n_red_trains[
                    dir_line + suffix_list[len(n_red_trains)]
                ] = train.waiting_time
            elif dir_line == "S-Red":
                s_red_trains[
                    dir_line + suffix_list[len(s_red_trains)]
                ] = train.waiting_time

        # Combine train lines
        self._attib.update(e_blue_trains)
        self._attib.update(w_blue_trains)
        self._attib.update(e_green_trains)
        self._attib.update(w_green_trains)
        self._attib.update(n_gold_trains)
        self._attib.update(s_gold_trains)
        self._attib.update(n_red_trains)
        self._attib.update(s_red_trains)

        return self._attib

    @property
    def native_value(self):
        """Return the state of the sensor."""

        return_value = "No Trains"
        station_trains = []
        # Gather and sort all trains for this station
        for train in self.coordinator.data:
            if train.station == self._attr_name.upper():
                station_trains.append(train)
        station_trains.sort(key=lambda x: x.next_arrival)
        # station_trains.sort(key=lambda x: x.next_arrival, reverse=True)
        if len(station_trains) > 0:
            # Save trains to _state for use in attributes
            self._state = station_trains
            # State is the next train to arrive
            return_value = f"{station_trains[0].direction}-{station_trains[0].line.capitalize()}: {station_trains[0].waiting_time}"
        # else:
        #     self._attib.clear()
        return return_value

        # self.raw_data = record
        # self.destination = record.get('DESTINATION')
        # self.direction = record.get('DIRECTION')
        # self.last_updated = datetime.strptime(record.get('EVENT_TIME'), '%m/%d/%Y %H:%M:%S %p')
        # self.line = record.get('LINE')
        # self.next_arrival = datetime.strptime(record.get('NEXT_ARR'), '%H:%M:%S %p').time()
        # self.station = record.get('STATION')
        # self.train_id = record.get('TRAIN_ID')
        # self.waiting_seconds = record.get('WAITING_SECONDS')
        # self.waiting_time = record.get('WAITING_TIME')
