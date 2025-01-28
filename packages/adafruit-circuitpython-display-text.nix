{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_display_text";
  version = "3.2.2";

  runtimeInputs = [];

  src = {
    hash = "sha256-4TKrQidduvg6Z8Lo2pmNyQEE6GXurcChbg+5f702luU=";
  };
}
