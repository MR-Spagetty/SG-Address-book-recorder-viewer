package address_book;

import java.util.List;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.Map;
import java.util.HashMap;

public class DataStorage {
    protected static final EnumMap<DeviceTypes, List<Network>> networks = new EnumMap<>(
            DeviceTypes.class);
    protected static final List<BookEntry> contents = new ArrayList<>();

    static void initStorage() {
        List<Network> sgNetworks = new ArrayList<>();
        networks.put(DeviceTypes.STARGATE, sgNetworks);
        for (String network : Config.sgNetworkNames) {
            sgNetworks.add(new Network(DeviceTypes.STARGATE, network));
        }
        List<Network> trNetworks = new ArrayList<>();
        networks.put(DeviceTypes.TRANSPORT_RINGS, trNetworks);
        for (String network : Config.trNetworkNames) {
            trNetworks.add(new Network(DeviceTypes.TRANSPORT_RINGS, network));
        }
    }
}
