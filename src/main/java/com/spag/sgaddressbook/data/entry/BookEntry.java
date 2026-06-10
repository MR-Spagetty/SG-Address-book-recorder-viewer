package com.spag.sgaddressbook.data.entry;

import java.util.List;

public interface BookEntry<T> {

  List<T> children();

  String name();

  /**
   * Changes the name of this entry.
   *
   * @param name
   *               the new name for this entry. Leading and trailing whitespace
   *               will be stripped.
   * @throws IllegalArgumentException
   *                                    if the name contains newlines
   */
  void name(String name);

  /**
   * Adds a child entry to this entry.
   *
   * @param entry
   *                the entry to add as a child of this entry.
   */
  void addChild(T entry);

  /**
   * Adds a child entry to this entry at the specified index.
   *
   * @param index
   *                the index at which to add the child entry.
   * @param entry
   *                the entry to add as a child of this entry.
   * @throws IndexOutOfBoundsException
   *                                     if the index is out of range (index < 0
   *                                     || index > number of children)
   */
  void addChild(int index, T entry);

  /**
   * Removes the child entry at the specified index.
   *
   * @param index
   *                the index of the child entry to remove.
   * @throws IndexOutOfBoundsException
   *                                     if the index is out of range (index < 0
   *                                     || index >= number of children)
   */
  void removeChild(int index);

  /**
   * Removes a child entry from this entry.
   *
   * @param entry
   *                the entry to remove from the children of this entry.
   */
  void removeChild(T entry);

  /**
   * Gets the child entry at the specified index.
   *
   * @param index
   *                the index of the child entry to retrieve.
   * @return the child entry at the specified index.
   * @throws IndexOutOfBoundsException
   *                                     if the index is out of range (index < 0
   *                                     || index >= number of children)
   */
  T getChild(int index);

  /**
   * Creates a deep copy of this entry and all of its children.
   *
   * @return a deep copy of this entry.
   */
  BookEntry<T> copy();
}
