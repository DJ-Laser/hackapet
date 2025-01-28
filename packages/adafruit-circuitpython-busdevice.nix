{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  adafruit-circuitpython-typing,
  adafruit-blinka,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_busdevice";
  version = "5.2.11";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-qaExC+5wIXA8zCR7s/8E0Ic1c5SKbHvukBY2HNZwenE=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
