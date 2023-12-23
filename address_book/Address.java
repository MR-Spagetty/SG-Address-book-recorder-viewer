package address_book;

import java.util.HashMap;
import javax.swing.JDialog;
import javax.swing.JLabel;

public class Address {

    /**
     * the type of device this address is for
     *
     * @see address_book.DeviceTypes
     */
    public final DeviceTypes addressType;
    public final String network;
    public final int maxGlyphs;
    private HashMap<Integer, Glyph> glyphs = new HashMap<>();

    /**
     * an address for storing multiple {@link address_book.Glyph Glyph}s in order
     *
     * @param network     the network the address inhabits
     * @param addressType the type of address it is (one of
     *                    {@link address_book.DeviceTypes DeviceTypes})
     * @see #Address(String)
     */
    public Address(String network, DeviceTypes addressType) {
        this.addressType = addressType;
        this.network = network;
        switch (addressType) {
        case STARGATE:
            this.maxGlyphs = 8;
            break;
        case TRANSPORT_RINGS:
            this.maxGlyphs = 16;
            break;
        case null, default:
            throw new IllegalArgumentException(
                    String.format("invalid Address type given:%nyou gave: %s%nvalid values are: %s",
                            addressType, DeviceTypes.values()));
        }
    }

    /**
     * <p>
     * an address for storing multiple Glyphs in order.
     * </p>
     * addressType is assumed to be {@link address_book.DeviceTypes#STARGATE
     * STARGATE}
     *
     * @param network the network the address inhabits
     * @see #Address(String, DeviceTypes)
     */
    public Address(String network) { this(network, DeviceTypes.STARGATE); }

    /**
     * clears the glyphs stored in this address
     *
     * @see #setGlyph(int, Glyph)
     * @see #getGlyph(int)
     */
    public void clear() { this.glyphs.clear(); }

    /**
     * sets the glyph at the specified position in the address to the given glyph if
     * applicable
     * <p>
     * if the given glyph is null clear that position in the address
     * </p>
     * <p>
     * if the glyph is a duplicate when they are not allowed open an error dialog
     * </p>
     *
     * @param pos   the position to change the glyph at
     * @param glyph the glyph ot change it to
     * @see #getGlyph(int)
     * @see #clear()
     */
    public void setGlyph(int pos, Glyph glyph) {
        if (pos < 0 || pos >= this.maxGlyphs) {
            throw new IllegalArgumentException("Invalid position given: " + pos
                    + "\n must be at least 0 and no greater than the maximum size of this address");
        }
        if (!this.glyphs.containsValue(glyph)) {
            if (glyph != null) {
                this.glyphs.put(pos, glyph);
            } else {
                this.glyphs.remove(pos);
            }
        } else {
            // Error dialog if duplicate selected and duplicates not allowed
            JDialog error = new JDialog();
            error.setModal(true);
            error.setTitle("Invalid glyph");
            error.setSize(500, 50);
            error.add(new JLabel(String.format(
                    "You may not have duplicate glyphs in a \"%s\" address", this.addressType)));
            error.setVisible(true);
        }
    }

    /**
     * get the glyph in the address at the specified position
     *
     * @param pos the position to get the glyph from
     * @return the glyph at the position
     * @see #setGlyph(int, Glyph)
     * @see #clear()
     */
    public Glyph getGlyph(int pos) {
        if (pos < 0 || pos >= this.maxGlyphs) {
            throw new IllegalArgumentException("Invalid position given: " + pos
                    + "\n must be at least 0 and no greater than the maximum size of this address");
        }
        return this.glyphs.get(pos);
    }

}
