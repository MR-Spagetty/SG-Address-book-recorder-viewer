package address_book;

import java.nio.file.Path;
/**
 * a simple glyph class for use as stargate or transport ring glyphs
 */
public class Glyph implements Comparable<Glyph> {
    public final String name;
    public final Integer id;
    public final Path imgPath;

    /**
     * a simple glyph for use in stargate or transport ring addresses
     *
     * @param name    the name of the glyph
     * @param id      the id of the glyph in it's system
     * @param imgPath the path to the image file to display for this glyph
     */
    public Glyph(String name, int id, Path imgPath) {
        this.name = name;
        this.id = id;
        this.imgPath = imgPath;
    }

    /**
     * compares two glyph objects and returns the position the other glyph should be
     * relative to this one
     *
     * @param other the glyph to compare this glyph to
     * @return the relative position it should be compared to this glyph
     */
    public int compareTo(Glyph other) {
        int idComp = this.id.compareTo(other.id);
        if (idComp != 0) {
            return idComp;
        }
        return this.name.compareTo(other.name);
    }

    /**
     * checks if this object and th eother object are equal
     *
     * @param other the object to check against
     * @return whether this object and the other are equal
     */
    @Override
    public boolean equals(Object other) {
        if (other instanceof Glyph) {
            return this.hashCode() == other.hashCode();
        }
        return false;
    }

    /**
     * gets the hashCode of this object
     *
     * @return the hashCode
     */
    @Override
    public int hashCode() { return (this.name + this.id).hashCode(); }
}
