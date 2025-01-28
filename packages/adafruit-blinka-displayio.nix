{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit,
}:
let
  inherit (adafruit) adafruit-blinka adafruit-circuitpython-typing adafruit-circuitpython-bitmap-font;
in
buildPythonPackage rec {
  pname = "adafruit_blinka_displayio";
  version = "0.11.1";
  format = "wheel";

  propagatedBuildInputs = [adafruit-blinka adafruit-circuitpython-typing adafruit-circuitpython-bitmap-font];

  src = fetchPypi {
    inherit pname version;
    format = "wheel";
    python = "py3";
    dist =  "py3";
    sha256 = "sha256-Y+LyCMVJhk4qvxkWtgPpcSH1x7QctBwmEib/ZG1qBbk=";
  };

  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];
}
