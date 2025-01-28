{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_bitmap_font";
  version = "2.1.4";

  propagatedBuildInputs = [];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-ZPJLghM+TdMiFDglJUPHABym6DXHD4+eOzK780SRKUI=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
