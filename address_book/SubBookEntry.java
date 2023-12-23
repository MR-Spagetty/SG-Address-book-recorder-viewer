package address_book;

import java.util.List;
import java.util.ArrayList;

public class SubBookEntry implements BookEntry {
    private String name = "Unnamed";
    private List<BookEntry> subItems = new ArrayList<>();

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
        // TODO write tostring
        return "";
    }
}
