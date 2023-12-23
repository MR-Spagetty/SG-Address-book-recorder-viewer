package address_book;

import java.util.List;
import java.util.ArrayList;

public class AddressEntry implements BookEntry {
    private String name = "Unnamed";
    public final DeviceTypes type;
    private List<Address> addresses = new ArrayList<>();

    /**
     * @param type
     */
    public AddressEntry(DeviceTypes type) { this.type = type; }

    @Override
    public String getName() { return this.name; }

    @Override
    public void setName(String newName) {
        if (newName.isEmpty()) {
            this.name = "Unnamed";
        } else {
            this.name = newName;
        }
    }

    @Override
    public String toString() {
        StringBuilder out = new StringBuilder("{\"type\": \"Address\",\n[\n");
        for (Address address : this.addresses) {
            out.append(address.toString() + ",\n");
        }
        // TODO get rid of trailing comma in array
        out.append("]\n}");
        return out.toString();
    }
}
