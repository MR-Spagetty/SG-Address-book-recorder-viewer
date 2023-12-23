package address_book;

/**
 * Used by: {@link address_book.Address}
 */
public enum DeviceTypes {
    STARGATE (8), TRANSPORT_RINGS (16);


    public final int maxGlyphs;
    DeviceTypes(int maxGlyphs){
        this.maxGlyphs = maxGlyphs;
    }
}
