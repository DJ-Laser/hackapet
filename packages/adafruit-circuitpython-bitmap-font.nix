{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_bitmap_font";
  version = "2.1.4";

  runtimeInputs = [];

  src = {
    hash = "sha256-ZPJLghM+TdMiFDglJUPHABym6DXHD4+eOzK780SRKUI=";
  };
}
