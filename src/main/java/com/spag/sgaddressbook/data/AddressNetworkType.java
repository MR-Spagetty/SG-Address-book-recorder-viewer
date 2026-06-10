package com.spag.sgaddressbook.data;

/**
 * AddressNetworkType.
 *
 * @author MR_Spagetty
 */
public class AddressNetworkType {
  public final AddressType addressType;
  public final String name;

  public AddressNetworkType(AddressType addressType, String name) {
    this.addressType = addressType;
    this.name = name;
  }
}
