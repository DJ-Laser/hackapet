{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_connectionmanager";
  version = "3.1.3";

  runtimeInputs = [];

  src = {
    hash = "sha256-DxM73t9FTt4MCoZu1gX+FmzIX3XPzqdHWONiKuQD5fk=";
  };
}
