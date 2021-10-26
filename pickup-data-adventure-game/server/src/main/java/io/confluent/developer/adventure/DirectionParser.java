package io.confluent.developer.adventure;

public class DirectionParser {
  static MovementCommandValue parse(String command) {
    switch (command) {
    case "START":
      return new MovementCommandValue("START");
    case "GO NORTH":
      return new MovementCommandValue("NORTH");
    case "GO SOUTH":
      return new MovementCommandValue("SOUTH");
    case "GO WEST":
      return new MovementCommandValue("WEST");
    case "GO EAST":
      return new MovementCommandValue("EAST");
    default:
      return null;
    }
  }
}