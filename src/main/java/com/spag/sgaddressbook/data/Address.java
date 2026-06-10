package com.spag.sgaddressbook.data;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;


/**
 * Generic address interface.
 *
 * @author MR_Spagetty
 */
public class Address {

  public final AddressType type;
  public final AddressNetworkType networkType;

  /**
   * Creates a new empty address of the given type.
   *
   * @param type
   *                      the type of address stored in this object
   * @param networkType
   *                      the network type of the address
   * @throws IllegalArgumentException
   *                                    if the network type does not match the
   *                                    address type
   */
  public Address(AddressType type, AddressNetworkType networkType) {
    this.type = type;
    this.networkType = networkType;
    if (networkType.addressType != type) {
      throw new IllegalArgumentException("Network type does not match address type");
    }
    this.glyphs = IntStream.range(0, type.maxGlyphCount + (type.hasPointOfOrigin ? 1 : 0))
        .mapToObj(i -> Optional.<Glyph>empty())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  /**
   * Creates a new address instance with the given glyphs. The number of glyphs
   * must be between the minimum and maximum for the address type, and if the
   * address type has a point of origin, there must be at most one more glyph than
   * the maximum.
   *
   * @param type
   *                      the type of address stored in this object
   * @param networkType
   *                      the network type of the address
   * @param glyphs
   *                      the list of glyphs for the address
   * @throws IllegalArgumentException
   *                                    if the number of glyphs is not valid for
   *                                    the address type
   *                                    or if the network type does not match the
   *                                    address type
   */
  @JsonCreator
  public Address(
      @JsonProperty("type") AddressType type,
      @JsonProperty("networkType") AddressNetworkType networkType,
      @JsonProperty("glyphs") List<Optional<Glyph>> glyphs) {
    this(type, networkType);
    if (glyphs.size() < type.minGlyphCount) {
      throw new IllegalArgumentException("Not enough glyphs for address type");
    } else if (glyphs.size() > type.maxGlyphCount + (type.hasPointOfOrigin ? 1 : 0)) {
      throw new IllegalArgumentException("Too many glyphs for address type");
    }

    for (int i = 0; i < Math.min(glyphs.size(), this.glyphs.size()); i++) {
      setGlyph(i, glyphs.get(i));
    }
  }

  public void setGlyph(int i, Optional<Glyph> optional) {
    // TODO Auto-generated method stub
    throw new UnsupportedOperationException("Unimplemented method 'setGlyph'");
  }

  public void setGlyph(int i, Glyph glyph) {
    setGlyph(i, Optional.of(glyph));
  }

  public Optional<Glyph> getGlyph(int i) {
    return this.glyphs.get(i);
  }

  private final List<Optional<Glyph>> glyphs;

  public List<Optional<Glyph>> glyphs() {
    return glyphs.stream().toList();
  }

  public Address copy() {
    return new Address(type, networkType, glyphs);
  }
}
