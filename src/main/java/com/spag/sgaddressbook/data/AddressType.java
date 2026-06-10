package com.spag.sgaddressbook.data;

/**
 * Valid Address types.
 *
 * @author MR_Spagetty
 */
public enum AddressType {
  Stargate(8, true),
  rings(4, true);

  public final int minGlyphCount;
  public final int maxGlyphCount;
  public final boolean hasPointOfOrigin;

  private AddressType(int glyphCount, boolean hasPointOfOrigin) {
    this(glyphCount, glyphCount, hasPointOfOrigin);
  }

  private AddressType(int minGlyphCount, int maxGlyphCount, boolean hasPointOfOrigin) {
    if (minGlyphCount < 0 || maxGlyphCount < 0) {
      throw new IllegalArgumentException("Glyph counts must be non-negative");
    }
    if (minGlyphCount > maxGlyphCount) {
      throw new IllegalArgumentException("minGlyphCount cannot be greater than maxGlyphCount");
    }
    this.minGlyphCount = minGlyphCount;
    this.maxGlyphCount = maxGlyphCount;
    this.hasPointOfOrigin = hasPointOfOrigin;
  }

}
