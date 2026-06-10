package com.spag.sgaddressbook.data.entry;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonSetter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Group implements BookEntry<BookEntry<?>> {
  private String name = "Unnamed group";
  private List<BookEntry<?>> children = new ArrayList<>();

  public Group() {
  }

  public Group(String name) {
    name(name);
  }

  public Group(String name, List<BookEntry<?>> children) {
    this(name);
    children.forEach(this::addChild);
  }

  @Override
  @JsonGetter
  public String name() {
    return name;
  }

  @Override
  @JsonSetter("name")
  public void name(String name) {
    name = name.strip();
    if (name.contains("\n")) {
      throw new IllegalArgumentException("Name cannot contain newlines");
    }
    this.name = name;
  }

  @Override
  @JsonGetter
  public List<BookEntry<?>> children() {
    return Collections.unmodifiableList(children);
  }

  @Override
  public void addChild(BookEntry<?> entry) {
    children.add(entry);
  }

  @Override
  public void removeChild(BookEntry<?> entry) {
    children.remove(entry);
  }

  @Override
  public BookEntry<BookEntry<?>> copy() {
    List<BookEntry<?>> copiedChildren = new ArrayList<>();
    for (BookEntry<?> child : children) {
      copiedChildren.add(child.copy());
    }
    return new Group(name, copiedChildren);
  }

  @Override
  public BookEntry<?> getChild(int index) {
    return children.get(index);
  }

  @Override
  public void removeChild(int index) {
    children.remove(index);
  }

  @Override
  public void addChild(int index, BookEntry<?> entry) {
    children.add(index, entry);
  }
}
