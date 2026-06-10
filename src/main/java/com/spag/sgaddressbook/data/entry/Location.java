package com.spag.sgaddressbook.data.entry;

import com.spag.sgaddressbook.data.Address;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Location entry, which contains addresses and any notes about the location.
 * This is the lowest level of entry in the address book, and cannot contain any
 * child entries.
 *
 * @author MR_Spagetty
 */
public class Location implements BookEntry<Address> {
  private String name;
  private List<Address> addresses = new ArrayList<>();

  private String notes = "";

  public String notes() {
    return notes;
  }

  public void notes(String notes) {
    this.notes = notes;
  }

  public Location() {
    this.name = "Unnamed location";
  }

  public Location(String name) {
    name(name);
  }

  public Location(String name, List<Address> addresses) {
    this(name);
    addresses.forEach(this::addChild);
  }

  @Override
  public List<Address> children() {
    return Collections.unmodifiableList(addresses);
  }

  @Override
  public String name() {
    return name;
  }

  @Override
  public void name(String name) {
    name = name.strip();
    if (name.contains("\n")) {
      throw new IllegalArgumentException("Name cannot contain newlines");
    }
    this.name = name;
  }

  @Override
  public void addChild(Address entry) {
    addresses.add(entry);
  }

  @Override
  public void addChild(int index, Address entry) {
    addresses.add(index, entry);
  }

  @Override
  public void removeChild(Address entry) {
    addresses.remove(entry);
  }

  @Override
  public void removeChild(int index) {
    addresses.remove(index);
  }

  @Override
  public BookEntry<Address> copy() {
    List<Address> copiedAddresses = new ArrayList<>();
    for (Address address : addresses) {
      copiedAddresses.add(address.copy());
    }
    return new Location(name, copiedAddresses);
  }

  @Override
  public Address getChild(int index) {
    return addresses.get(index);
  }

}
